#!/usr/bin/env python3
"""
ETH Trading Data Validator
Validates trading context data quality and freshness
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
ARENA_DIR = Path("/home/openclaw/.openclaw/workspace/projects/nofx-project/arena")

# Add executor to path for Hyperliquid verification
sys.path.insert(0, str(SCRIPT_DIR / "executor"))


def load_json_file(filepath: Path, default=None):
    """Load JSON file."""
    try:
        if filepath.exists():
            with open(filepath) as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
    return default


def check_file_freshness(filepath: Path, max_age_minutes: int) -> Tuple[bool, str]:
    """Check if file was updated within max_age_minutes."""
    if not filepath.exists():
        return False, "File does not exist"
    
    try:
        mtime = datetime.fromtimestamp(filepath.stat().st_mtime, tz=timezone.utc)
        age = datetime.now(timezone.utc) - mtime
        age_minutes = age.total_seconds() / 60
        
        if age_minutes > max_age_minutes:
            return False, f"File is {age_minutes:.1f} minutes old (max: {max_age_minutes})"
        return True, f"File is {age_minutes:.1f} minutes old"
    except Exception as e:
        return False, f"Error checking file age: {e}"


def validate_trading_context() -> Tuple[bool, List[str]]:
    """Validate trading-context.json."""
    issues = []
    success = True
    
    ctx_file = DATA_DIR / "trading-context.json"
    
    # Check file exists and freshness
    fresh, msg = check_file_freshness(ctx_file, 20)
    if not fresh:
        issues.append(f"trading-context.json: {msg}")
        success = False
    else:
        issues.append(f"trading-context.json: {msg}")
    
    # Load and validate contents
    ctx = load_json_file(ctx_file)
    if not ctx:
        issues.append("trading-context.json: Cannot load JSON")
        return False, issues
    
    # Check ETH price
    eth_price = ctx.get("eth_price", 0)
    if eth_price < 100 or eth_price > 100000:
        issues.append(f"ETH price {eth_price} is outside reasonable range (100-100000)")
        success = False
    else:
        issues.append(f"ETH price: ${eth_price}")
    
    # Check candles
    candles_1h = ctx.get("candles_1h", [])
    if len(candles_1h) < 50:
        issues.append(f"1H candles: Only {len(candles_1h)} (need 50+)")
        success = False
    else:
        # Check if last candle is recent (within 2 hours)
        if candles_1h:
            last_candle_time = datetime.fromtimestamp(candles_1h[-1].get("t", 0) / 1000, tz=timezone.utc)
            age = datetime.now(timezone.utc) - last_candle_time
            if age.total_seconds() > 7200:  # 2 hours
                issues.append(f"1H candles: Last candle is {age.total_seconds()/3600:.1f} hours old")
                success = False
            else:
                issues.append(f"1H candles: {len(candles_1h)} candles, last {age.total_seconds()/60:.1f} min ago")
    
    # Check indicators
    ind_1h = ctx.get("indicators_1h", {})
    if not ind_1h:
        issues.append("1H indicators: Missing")
        success = False
    else:
        # Check RSI range
        rsi = ind_1h.get("rsi_14", 50)
        if rsi < 0 or rsi > 100:
            issues.append(f"RSI {rsi} is outside valid range (0-100)")
            success = False
        else:
            issues.append(f"RSI: {rsi}")
        
        # Check EMA values exist
        if not ind_1h.get("ema_12"):
            issues.append("EMA 12: Missing")
            success = False
        if not ind_1h.get("ema_26"):
            issues.append("EMA 26: Missing")
            success = False
    
    # Check position data
    position = ctx.get("position")
    balance = ctx.get("balance", {})
    if not balance:
        issues.append("Balance: Missing")
    else:
        issues.append(f"Balance: ${balance.get('equity', 0):.2f}")
    
    # Check market data
    market_data = ctx.get("market_data", {})
    if not market_data:
        issues.append("Market data: Missing")
    else:
        issues.append(f"Market data: {list(market_data.keys())[:3]}...")
    
    return success, issues


def validate_arena_data() -> Tuple[bool, List[str]]:
    """Validate arena data files."""
    issues = []
    success = True
    
    # Check market-live.json
    market_file = ARENA_DIR / "market-live.json"
    fresh, msg = check_file_freshness(market_file, 5)
    if fresh:
        issues.append(f"market-live.json: {msg}")
    else:
        issues.append(f"market-live.json: {msg} (warning)")
    
    # Check onchain-hourly.json
    onchain_file = ARENA_DIR / "onchain-hourly.json"
    fresh, msg = check_file_freshness(onchain_file, 60)
    if fresh:
        issues.append(f"onchain-hourly.json: {msg}")
    else:
        issues.append(f"onchain-hourly.json: {msg} (warning)")
    
    # Check protocol-hourly.json
    protocol_file = ARENA_DIR / "protocol-hourly.json"
    fresh, msg = check_file_freshness(protocol_file, 60)
    if fresh:
        issues.append(f"protocol-hourly.json: {msg}")
    else:
        issues.append(f"protocol-hourly.json: {msg} (warning)")
    
    # Check news-summary.json
    news_file = ARENA_DIR / "news-summary.json"
    fresh, msg = check_file_freshness(news_file, 60)
    if fresh:
        issues.append(f"news-summary.json: {msg}")
    else:
        issues.append(f"news-summary.json: {msg} (warning)")
    
    return success, issues


def validate_position_state() -> Tuple[bool, List[str]]:
    """Validate position-state.json."""
    issues = []
    success = True
    
    pos_file = DATA_DIR / "position-state.json"
    
    # Check file exists
    if not pos_file.exists():
        issues.append("position-state.json: Missing")
        return False, issues
    
    # Check freshness
    fresh, msg = check_file_freshness(pos_file, 20)
    if not fresh:
        issues.append(f"position-state.json: {msg}")
        success = False
    else:
        issues.append(f"position-state.json: {msg}")
    
    # Validate contents
    state = load_json_file(pos_file)
    if state:
        position = state.get("position")
        balance = state.get("balance", {})
        
        if balance:
            issues.append(f"Position state balance: ${balance.get('equity', 0):.2f}")
        
        if position:
            issues.append(f"Position: {position.get('side')} {position.get('size_usd', 0):.2f} @ {position.get('entry_price', 0)}")
        else:
            issues.append("Position: Flat")
    else:
        issues.append("position-state.json: Cannot parse")
        success = False
    
    return success, issues


def main():
    """Main validation function."""
    print("=== ETH Trading Data Validator ===\n")
    
    all_issues = []
    has_critical = False
    
    # Validate trading context
    print("--- Trading Context ---")
    success, issues = validate_trading_context()
    all_issues.extend(issues)
    has_critical = has_critical or not success
    for issue in issues:
        status = "✓" if "Missing" not in issue and "warning" not in issue.lower() else "⚠"
        print(f"  {status} {issue}")
    
    # Validate arena data
    print("\n--- Arena Data ---")
    success, issues = validate_arena_data()
    all_issues.extend(issues)
    for issue in issues:
        status = "✓" if "warning" not in issue.lower() else "⚠"
        print(f"  {status} {issue}")
    
    # Validate position state
    print("\n--- Position State ---")
    success, issues = validate_position_state()
    all_issues.extend(issues)
    has_critical = has_critical or not success
    for issue in issues:
        status = "✓" if "Missing" not in issue else "✗"
        print(f"  {status} {issue}")
    
    # Write validation report
    validation_report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "has_critical": has_critical,
        "issues": all_issues
    }
    
    report_file = DATA_DIR / "validation.json"
    with open(report_file, "w") as f:
        json.dump(validation_report, f, indent=2)
    print(f"\nValidation report written to {report_file}")
    
    # Exit code
    print("\n=== Summary ===")
    if has_critical:
        print("✗ CRITICAL ISSUES FOUND")
        sys.exit(2)
    else:
        print("✓ All checks passed")
        sys.exit(0)


if __name__ == "__main__":
    main()
