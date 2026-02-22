#!/usr/bin/env python3
"""
NOFX System Readiness Test
===========================
Lightweight test that verifies all 10 coins have proper data,
the debate engine can receive context, and decisions can be written.
Does NOT run actual LLM debates (no API cost).

Tests:
1. Arena context data completeness (all 10 coins, all required fields)
2. Coin profiles completeness 
3. Data freshness (timestamp checks)
4. Hyperliquid symbol mapping (PEPE → kPEPE)
5. API endpoints reachable (arena context, debate list, agent events)
6. Decision write test (POST agent event)
7. Strategy existence
8. AI model configuration (DeepSeek V3 + R1 enabled)
"""

import json
import time
import sys
import os
import jwt
import requests
from datetime import datetime, timezone

# ─── Config ───
API_BASE = "http://localhost:8090/api"
JWT_SECRET = "Fm9Dd/bc2ix30BkhbC22lKy2m/0CDjedaX/TAwkQMGc="
USER_ID = "34dd0d3b-bf61-4a6a-82fc-0f0af42355c1"
ARENA_DIR = os.path.dirname(os.path.abspath(__file__))
CONTEXT_FILE = os.path.join(ARENA_DIR, "debate-context.json")
PROFILES_FILE = os.path.join(ARENA_DIR, "coin-profiles.json")

EXPECTED_COINS = ["ETH", "AAVE", "LINK", "ZRO", "ENA", "UNI", "LDO", "CRV", "PENDLE", "ARB"]
REQUIRED_COIN_FIELDS = [
    "funding_rate", "funding_signal", "orderbook_imbalance", "orderbook_signal",
    "oi_usd", "oi_change_pct", "oi_signal", "cvd", "cvd_signal", "price", "profile"
]
REQUIRED_SHARED_FIELDS = [
    "fear_greed", "options", "aave", "curve_3pool", "exchange_eth_reserves"
]
REQUIRED_PROFILE_FIELDS = ["what_it_is", "on_chain_relevance", "key_debate_angles"]

# Hyperliquid symbol mapping (LDO replaced PEPE — no special mapping needed)
HL_SYMBOL_MAP = {}

# ─── Helpers ───
passed = 0
failed = 0
warnings = 0

def ok(msg):
    global passed
    passed += 1
    print(f"  ✅ {msg}")

def fail(msg):
    global failed
    failed += 1
    print(f"  ❌ {msg}")

def warn(msg):
    global warnings
    warnings += 1
    print(f"  ⚠️  {msg}")

def get_token():
    payload = {"user_id": USER_ID, "exp": int(time.time()) + 3600}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def api_get(path, token):
    try:
        r = requests.get(f"{API_BASE}{path}", headers={"Authorization": f"Bearer {token}"}, timeout=10)
        return r.status_code, r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text
    except Exception as e:
        return 0, str(e)

def api_post(path, token, data):
    try:
        r = requests.post(f"{API_BASE}{path}", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, json=data, timeout=10)
        return r.status_code, r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text
    except Exception as e:
        return 0, str(e)

# ─── Tests ───

def test_local_context_file():
    """Test 1: debate-context.json exists and has all coins"""
    print("\n📋 Test 1: Local debate-context.json")
    
    if not os.path.exists(CONTEXT_FILE):
        fail(f"debate-context.json not found at {CONTEXT_FILE}")
        return None
    ok("debate-context.json exists")
    
    with open(CONTEXT_FILE) as f:
        ctx = json.load(f)
    
    # Check timestamp freshness
    ts_str = ctx.get("timestamp", "")
    if ts_str:
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            age_min = (datetime.now(timezone.utc) - ts).total_seconds() / 60
            if age_min < 120:
                ok(f"Data fresh: {age_min:.0f} min old")
            else:
                warn(f"Data stale: {age_min:.0f} min old (>2h)")
        except:
            warn(f"Could not parse timestamp: {ts_str}")
    else:
        warn("No timestamp in context file")
    
    # Check data sources
    sources = ctx.get("data_sources", {})
    for src in ["onchain", "market", "protocol", "profiles"]:
        if sources.get(src):
            ok(f"Data source '{src}': enabled")
        else:
            fail(f"Data source '{src}': missing or disabled")
    
    # Check per_coin
    per_coin = ctx.get("per_coin", {})
    for coin in EXPECTED_COINS:
        if coin not in per_coin:
            fail(f"Coin {coin}: MISSING from per_coin")
            continue
        
        coin_data = per_coin[coin]
        missing = [f for f in REQUIRED_COIN_FIELDS if f not in coin_data]
        if missing:
            fail(f"Coin {coin}: missing fields: {missing}")
        else:
            # Check for null/zero values
            nulls = [f for f in REQUIRED_COIN_FIELDS if coin_data.get(f) is None]
            if nulls:
                warn(f"Coin {coin}: null fields: {nulls}")
            else:
                ok(f"Coin {coin}: all {len(REQUIRED_COIN_FIELDS)} fields present")
    
    # Check shared intelligence
    shared = ctx.get("shared_intelligence", {})
    for field in REQUIRED_SHARED_FIELDS:
        if field in shared:
            ok(f"Shared data '{field}': present")
        else:
            fail(f"Shared data '{field}': MISSING")
    
    return ctx

def test_coin_profiles():
    """Test 2: coin-profiles.json has all coins with required fields"""
    print("\n📋 Test 2: Coin profiles")
    
    if not os.path.exists(PROFILES_FILE):
        fail(f"coin-profiles.json not found at {PROFILES_FILE}")
        return
    ok("coin-profiles.json exists")
    
    with open(PROFILES_FILE) as f:
        raw = json.load(f)
    profiles = raw.get("profiles", raw)  # Handle nested {"profiles": {...}} or flat
    
    for coin in EXPECTED_COINS:
        if coin not in profiles:
            fail(f"Profile {coin}: MISSING")
            continue
        
        profile = profiles[coin]
        missing = [f for f in REQUIRED_PROFILE_FIELDS if f not in profile]
        if missing:
            fail(f"Profile {coin}: missing fields: {missing}")
        else:
            angles = profile.get("key_debate_angles", [])
            ok(f"Profile {coin}: complete ({len(angles)} debate angles)")

def test_hyperliquid_mapping():
    """Test 3: PEPE → kPEPE mapping for Hyperliquid"""
    print("\n📋 Test 3: Hyperliquid symbol mapping")
    
    for display_name, hl_name in HL_SYMBOL_MAP.items():
        ok(f"Mapping configured: {display_name} → {hl_name}")
    
    # Verify in context data
    with open(CONTEXT_FILE) as f:
        ctx = json.load(f)
    per_coin = ctx.get("per_coin", {})
    
    if "PEPE" in per_coin:
        pepe_data = per_coin["PEPE"]
        if pepe_data.get("price") and pepe_data["price"] > 0:
            ok(f"PEPE has price data: ${pepe_data['price']}")
        else:
            warn(f"PEPE price is {pepe_data.get('price')} (may be issue with kPEPE mapping)")
        
        if pepe_data.get("oi_usd") and pepe_data["oi_usd"] > 0:
            ok(f"PEPE has OI data: ${pepe_data['oi_usd']:,.0f}")
        else:
            warn(f"PEPE OI is {pepe_data.get('oi_usd')}")
    else:
        fail("PEPE not in per_coin data")

def test_api_endpoints():
    """Test 4: API endpoints are reachable"""
    print("\n📋 Test 4: API endpoints")
    
    token = get_token()
    
    # Arena context
    status, data = api_get("/arena/context", token)
    if status == 200:
        coins = list(data.get("per_coin", {}).keys()) if isinstance(data, dict) else []
        ok(f"GET /arena/context: {status} ({len(coins)} coins)")
    else:
        fail(f"GET /arena/context: {status} - {data}")
    
    # Debates list
    status, data = api_get("/debates", token)
    if status == 200:
        count = len(data) if isinstance(data, list) else "?"
        ok(f"GET /debates: {status} ({count} debates)")
    else:
        fail(f"GET /debates: {status} - {data}")
    
    # Agent events
    status, data = api_get("/agents/events?limit=5", token)
    if status == 200:
        count = len(data) if isinstance(data, list) else "?"
        ok(f"GET /agents/events: {status} ({count} events)")
    else:
        fail(f"GET /agents/events: {status} - {data}")
    
    # Agent stats
    status, data = api_get("/agents/stats", token)
    if status == 200:
        ok(f"GET /agents/stats: {status}")
    else:
        fail(f"GET /agents/stats: {status} - {data}")

def test_decision_write():
    """Test 5: Can write a test decision (agent event)"""
    print("\n📋 Test 5: Decision write test")
    
    token = get_token()
    
    test_event = {
        "type": "decision",
        "model": "Opus 4.6",
        "task": "readiness-test",
        "status": "completed",
        "message": "TEST: System readiness check passed",
        "details": f"All {len(EXPECTED_COINS)} coins verified at {datetime.now().isoformat()}",
        "tokens_in": 0,
        "tokens_out": 0,
        "cost_usd": 0,
        "duration_s": 0
    }
    
    status, data = api_post("/agents/events", token, test_event)
    if status == 200 or status == 201:
        ok(f"POST /agents/events: {status} (test event written)")
    else:
        fail(f"POST /agents/events: {status} - {data}")

def test_ai_models():
    """Test 6: DeepSeek V3 + R1 models configured and enabled"""
    print("\n📋 Test 6: AI model configuration")
    
    token = get_token()
    status, data = api_get("/models", token)
    
    if status != 200:
        fail(f"GET /ai-models: {status} - {data}")
        return
    
    if not isinstance(data, list):
        fail(f"Expected list, got {type(data)}")
        return
    
    found_v3 = False
    found_r1 = False
    
    for model in data:
        provider = model.get("provider", "")
        name = model.get("name", "")
        enabled = model.get("enabled", False)
        model_id = model.get("id", "")
        
        if provider == "deepseek":
            if "r1" in model_id.lower() or "reasoner" in model.get("model_name", "").lower():
                found_r1 = True
                if enabled:
                    ok(f"DeepSeek R1: enabled (id={model_id})")
                else:
                    fail(f"DeepSeek R1: DISABLED (id={model_id})")
            else:
                found_v3 = True
                if enabled:
                    ok(f"DeepSeek V3: enabled (id={model_id})")
                else:
                    fail(f"DeepSeek V3: DISABLED (id={model_id})")
    
    if not found_v3:
        fail("DeepSeek V3: NOT CONFIGURED")
    if not found_r1:
        fail("DeepSeek R1: NOT CONFIGURED")
    
    # Show all models
    for model in data:
        status_str = "✓" if model.get("enabled") else "✗"
        print(f"    [{status_str}] {model.get('name', '?')} ({model.get('provider', '?')})")

def test_strategies():
    """Test 7: At least one strategy exists"""
    print("\n📋 Test 7: Strategy configuration")
    
    token = get_token()
    status, data = api_get("/strategies/active", token)
    
    if status == 200 and isinstance(data, dict) and data.get("id"):
        cfg = data.get("config", {})
        ok(f"Active strategy found: id={data['id'][:8]}...")
        print(f"    Language: {cfg.get('language', '?')}")
        print(f"    Coin source: {cfg.get('coin_source', {}).get('source_type', '?')}")
        print(f"    Primary TF: {cfg.get('indicators', {}).get('klines', {}).get('primary_timeframe', '?')}")
    else:
        fail(f"No active strategy: {status} - {data}")

def test_deepseek_balance():
    """Test 8: DeepSeek API balance check"""
    print("\n📋 Test 8: DeepSeek API balance")
    
    # Decrypt key from DB (same method as backend)
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        import base64
        
        enc_key = base64.b64decode("8bIfCLGQH4D+vW6x5A2nkeZuUlJvx3u1yQHujvV0V5o=")
        
        # DeepSeek encrypted key
        enc_value = "ENC:v1:/sLnv0P8/NLjOQED:daD9SSiE0hRnZQWWbrDnT9CA0f9A1ZrecJeCx6nxDGcE0sbwtVMVsDh+5t2UQRk4qMgw"
        parts = enc_value.replace("ENC:v1:", "").split(":")
        nonce = base64.b64decode(parts[0])
        ciphertext = base64.b64decode(parts[1])
        
        aesgcm = AESGCM(enc_key)
        api_key = aesgcm.decrypt(nonce, ciphertext, None).decode()
        
        r = requests.get("https://api.deepseek.com/user/balance", 
                        headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            for bi in data.get("balance_infos", []):
                if bi["currency"] == "CNY":
                    balance = float(bi["total_balance"])
                    if balance > 10:
                        ok(f"DeepSeek balance: ¥{balance:.2f} CNY")
                    elif balance > 0:
                        warn(f"DeepSeek balance LOW: ¥{balance:.2f} CNY")
                    else:
                        fail(f"DeepSeek balance EMPTY: ¥{balance:.2f} CNY")
        else:
            fail(f"DeepSeek balance API: HTTP {r.status_code}")
    except ImportError:
        warn("cryptography package not installed, skipping balance check")
    except Exception as e:
        fail(f"DeepSeek balance check failed: {e}")

def test_data_quality():
    """Test 9: Data quality checks — prices, OI, funding rates make sense"""
    print("\n📋 Test 9: Data quality")
    
    with open(CONTEXT_FILE) as f:
        ctx = json.load(f)
    
    per_coin = ctx.get("per_coin", {})
    
    for coin in EXPECTED_COINS:
        if coin not in per_coin:
            continue
        data = per_coin[coin]
        issues = []
        
        price = data.get("price", 0)
        if price is None or price <= 0:
            issues.append(f"price={price}")
        
        oi = data.get("oi_usd", 0)
        if oi is None or oi <= 0:
            issues.append(f"oi={oi}")
        
        funding = data.get("funding_rate")
        if funding is None:
            issues.append("funding=None")
        elif abs(funding) > 0.1:  # >10% funding rate is suspicious
            issues.append(f"funding={funding} (suspicious)")
        
        if issues:
            warn(f"{coin}: {', '.join(issues)}")
        else:
            ok(f"{coin}: price=${price:.4f}, OI=${oi:,.0f}, funding={funding:.6f}")

# ─── Main ───

if __name__ == "__main__":
    print("=" * 60)
    print("🔬 NOFX System Readiness Test")
    print(f"   Time: {datetime.now().isoformat()}")
    print(f"   Coins: {', '.join(EXPECTED_COINS)}")
    print("=" * 60)
    
    test_local_context_file()
    test_coin_profiles()
    test_hyperliquid_mapping()
    test_api_endpoints()
    test_decision_write()
    test_ai_models()
    test_strategies()
    test_deepseek_balance()
    test_data_quality()
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {passed} passed, {failed} failed, {warnings} warnings")
    print("=" * 60)
    
    if failed > 0:
        print("❌ SYSTEM NOT READY — fix failures above before running debates")
        sys.exit(1)
    elif warnings > 0:
        print("⚠️  SYSTEM READY WITH WARNINGS — review warnings above")
        sys.exit(0)
    else:
        print("✅ SYSTEM FULLY READY — all coins verified, data fresh, APIs working")
        sys.exit(0)
