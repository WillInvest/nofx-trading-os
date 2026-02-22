#!/usr/bin/env python3
"""
push-to-nofx.py - Convert MiniMax brain decisions to NOFX Go backend format

This script:
1. Reads /home/openclaw/.openclaw/workspace/projects/eth-engine/data/decision.json (brain output)
2. Generates hourly-plan.json in Fao-friendly format (scan_mode, position_review, new_candidate)
3. Generates hourly-instruction.md with clear execution orders for Fao
4. Writes both to NOFX arena directory and copies to Docker container
"""

import json
import os
import subprocess
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
DECISION_FILE = os.path.join(DATA_DIR, "decision.json")

# NOFX Arena directories
ARENA_DIR_HOST = "/home/openclaw/.openclaw/workspace/projects/nofx-project/nofx/data/arena"
DOCKER_CONTAINER = "nofx-trading"
DOCKER_ARENA_DIR = "/app/data/arena"

HOURLY_PLAN_FILE = "hourly-plan.json"
HOURLY_INSTRUCTION_FILE = "hourly-instruction.md"


def load_decision() -> Dict[str, Any]:
    """Load the MiniMax brain decision from decision.json"""
    if not os.path.exists(DECISION_FILE):
        raise FileNotFoundError(f"Decision file not found: {DECISION_FILE}")

    with open(DECISION_FILE, 'r') as f:
        return json.load(f)


def compute_stop_loss_pct(entry_price: Optional[float], stop_loss: Optional[float]) -> Optional[float]:
    """Compute stop loss percentage from entry price and stop loss level"""
    if entry_price and stop_loss:
        return round(abs(entry_price - stop_loss) / entry_price * 100, 2)
    return None


def map_action_to_fao(decision: Dict[str, Any]) -> str:
    """Map brain strategy to Fao action string"""
    strategy = decision.get("strategy", "open_long")
    direction = decision.get("direction", "long")

    if strategy in ("hold", "wait"):
        return "hold"
    if strategy == "close_all":
        return "close"

    if direction == "long":
        return "open_long"
    elif direction == "short":
        return "open_short"

    # grid_trading is also valid
    if strategy == "grid_trading":
        return "grid"

    return "open_long"  # default


def convert_to_hourly_plan(decision: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MiniMax decision to NOFX hourly-plan.json format (Fao-friendly)"""

    strategy = decision.get("strategy", "open_long")
    direction = decision.get("direction", "long")
    size_usd = decision.get("size_usd", 15)
    leverage = decision.get("leverage", 3)
    entry_price = decision.get("entry_price")
    stop_loss = decision.get("stop_loss")
    take_profit = decision.get("take_profit")
    reasoning = decision.get("reasoning", "")
    confidence = decision.get("confidence", 50)
    timestamp = decision.get("timestamp", datetime.now(timezone.utc).isoformat())

    # Calculate valid_until (1 hour from now)
    now = datetime.now(timezone.utc)
    valid_until = (now + timedelta(hours=1)).isoformat()

    # Map action for Fao
    action = map_action_to_fao(decision)

    # Determine if we have an active position to review
    # For now, assume no existing position - Fao will check itself
    position_review = {
        "symbol": "ETH",
        "action": "hold",  # No existing position
        "confidence": 0,
        "reasoning": "No existing position to review"
    }

    # Build new_candidate (the main trade to execute)
    if action in ("open_long", "open_short", "grid"):
        new_candidate = {
            "symbol": "ETH",
            "action": action,
            "confidence": confidence,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "size_usd": size_usd,
            "leverage": leverage
        }
    else:
        # hold, close, etc - no new candidate
        new_candidate = {
            "symbol": "ETH",
            "action": action,
            "confidence": confidence,
            "entry_price": None,
            "stop_loss": None,
            "take_profit": None,
            "size_usd": 0,
            "leverage": 0
        }

    # Build strategies array (for backward compatibility)
    stop_loss_pct = compute_stop_loss_pct(entry_price, stop_loss)

    strategy_entry = {
        "id": "brain_decision",
        "name": "MiniMax Brain Decision",
        "type": strategy,
        "priority": 1,
        "allocation_pct": 100,
        "allocation_usd": size_usd,
        "description": reasoning[:200] if reasoning else "AI trading decision",
        "symbol": "ETH",
        "params": {
            "direction": direction.upper(),
            "leverage": leverage,
            "entry_price": entry_price,
            "entry_type": "market" if not entry_price else "limit",
            "stop_loss_pct": stop_loss_pct,
            "take_profit_pct": round((take_profit - entry_price) / entry_price * 100, 2) if entry_price and take_profit else None
        },
        "rationale": reasoning,
        "exit_condition": f"SL at ${stop_loss} / TP at ${take_profit}" if stop_loss and take_profit else "Monitor for exit conditions"
    }

    hourly_plan = {
        "scan_mode": False,
        "active_coin": "ETH",
        "timestamp": timestamp,
        "valid_until": valid_until,
        "brain": "MiniMax Trading Brain",
        "position_review": position_review,
        "new_candidate": new_candidate,
        "market_context": reasoning[:500] if reasoning else "AI trading analysis complete",
        "strategies": [strategy_entry]
    }

    return hourly_plan


def convert_to_hourly_instruction(decision: Dict[str, Any]) -> str:
    """Convert MiniMax decision to hourly-instruction.md format (Fao's "Hourly Teaching")"""

    strategy = decision.get("strategy", "open_long")
    direction = decision.get("direction", "long")
    size_usd = decision.get("size_usd", 15)
    leverage = decision.get("leverage", 3)
    entry_price = decision.get("entry_price")
    stop_loss = decision.get("stop_loss")
    take_profit = decision.get("take_profit")
    reasoning = decision.get("reasoning", "")
    confidence = decision.get("confidence", 50)

    timestamp = decision.get("timestamp", datetime.now(timezone.utc).isoformat())
    next_hour = (datetime.now(timezone.utc) + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S %Z")

    # Map action
    action = map_action_to_fao(decision)

    # Format action for display
    action_display = action.replace("_", " ").upper()

    # Entry display
    if entry_price:
        entry_display = f"limit at ${entry_price}"
    else:
        entry_display = "market"

    # Build instruction markdown
    instruction_md = f"""# Hourly Trading Instruction (from MiniMax Brain)

**Time:** {timestamp}
**Valid until:** {next_hour}

## EXECUTE THIS PLAN:
- **Action:** {action_display}
- **Symbol:** ETH
- **Size:** ${size_usd} at {leverage}x leverage
- **Entry:** {entry_display}
- **Stop Loss:** ${stop_loss} (MANDATORY)
- **Take Profit:** ${take_profit}
- **Confidence:** {confidence}%

## WHY:
{reasoning}

## RULES:
- Execute this plan ONCE, then HOLD until next hourly instruction
- Do NOT overtrade - one entry per hour max
- If already in a position matching this direction, HOLD (do not double up)
- If in opposite position, CLOSE first then open new
- SL is non-negotiable. Never remove SL.
"""

    return instruction_md


def write_json_file(data: Dict[str, Any], directory: str, filename: str) -> str:
    """Write JSON data to file, creating directory if needed"""
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    return filepath


def write_md_file(content: str, directory: str, filename: str) -> str:
    """Write markdown data to file, creating directory if needed"""
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath


def copy_to_docker(host_path: str, container_path: str) -> bool:
    """Copy file to Docker container"""
    try:
        result = subprocess.run(
            ["docker", "cp", host_path, f"{DOCKER_CONTAINER}:{container_path}"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"    ✓ Copied to Docker: {container_path}")
            return True
        else:
            print(f"    ⚠ Docker copy failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"    ⚠ Docker copy error: {e}")
        return False


def main():
    print("=" * 60)
    print("push-to-nofx.py - Converting MiniMax decision to NOFX format")
    print("=" * 60)

    # Step 1: Load decision
    print(f"\n[1] Loading decision from {DECISION_FILE}...")
    decision = load_decision()
    print(f"    Strategy: {decision.get('strategy')}")
    print(f"    Direction: {decision.get('direction')}")
    print(f"    Size: ${decision.get('size_usd')}")
    print(f"    Confidence: {decision.get('confidence')}%")

    # Step 2: Convert to hourly-plan format (Fao-friendly)
    print("\n[2] Converting to hourly-plan.json format...")
    hourly_plan = convert_to_hourly_plan(decision)
    print(f"    Active coin: {hourly_plan['active_coin']}")
    print(f"    Action: {hourly_plan['new_candidate']['action']}")
    print(f"    Valid until: {hourly_plan['valid_until']}")

    # Step 3: Convert to hourly-instruction.md
    print("\n[3] Converting to hourly-instruction.md...")
    hourly_instruction = convert_to_hourly_instruction(decision)
    print(f"    Instruction length: {len(hourly_instruction)} chars")

    # Step 4: Write to host directory
    print(f"\n[4] Writing files to host directory: {ARENA_DIR_HOST}")
    hourly_plan_path = write_json_file(hourly_plan, ARENA_DIR_HOST, HOURLY_PLAN_FILE)
    print(f"    ✓ {hourly_plan_path}")

    hourly_instruction_path = write_md_file(hourly_instruction, ARENA_DIR_HOST, HOURLY_INSTRUCTION_FILE)
    print(f"    ✓ {hourly_instruction_path}")

    # Step 5b: Copy brain decision for the API
    print("\n[5b] Copying brain decision for API...")
    try:
        shutil.copy2(DECISION_FILE, os.path.join(ARENA_DIR_HOST, "brain-decision.json"))
        print(f"    ✓ Copied decision.json to brain-decision.json")
    except Exception as e:
        print(f"    ⚠ Failed to copy brain decision: {e}")

    # Step 6: Copy to Docker container
    print(f"\n[6] Copying files to Docker container ({DOCKER_CONTAINER})...")
    copy_to_docker(hourly_plan_path, f"{DOCKER_ARENA_DIR}/{HOURLY_PLAN_FILE}")
    copy_to_docker(hourly_instruction_path, f"{DOCKER_ARENA_DIR}/{HOURLY_INSTRUCTION_FILE}")
    # Also copy brain decision to Docker
    brain_decision_host_path = os.path.join(ARENA_DIR_HOST, "brain-decision.json")
    if os.path.exists(brain_decision_host_path):
        copy_to_docker(brain_decision_host_path, f"{DOCKER_ARENA_DIR}/brain-decision.json")

    print("\n" + "=" * 60)
    print("✓ Conversion complete!")
    print("=" * 60)
    print("\nFiles created:")
    print(f"  - {hourly_plan_path}")
    print(f"  - {hourly_instruction_path}")
    print("\nNext: Fao will read these files and execute the trade.")

    return 0


if __name__ == "__main__":
    exit(main())
