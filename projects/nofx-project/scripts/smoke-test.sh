#!/bin/bash
# Smoke test the NOFX platform after deploy
# Returns exit code 0 if all pass, 1 if any fail

BACKEND="http://localhost:8090"
FRONTEND="http://localhost:3001"
FAIL_LOG="/tmp/smoke-test-fail.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Generate JWT token
JWT=$(python3 -c "import jwt,time; print(jwt.encode({'sub':'admin','exp':int(time.time())+3600}, b'Fm9Dd/bc2ix30BkhbC22lKy2m/0CDjedaX/TAwkQMGc=', algorithm='HS256'))")

# Initialize counters
PASSED=0
FAILED=0

# Clear fail log
> "$FAIL_LOG"

echo "=========================================="
echo "🚀 NOFX Platform Smoke Test"
echo "=========================================="
echo ""

# Test 1: Backend health
echo -n "🔍 Backend health check... "
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND/" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}PASS${NC} (HTTP $HTTP_CODE)"
    ((PASSED++))
else
    echo -e "${RED}FAIL${NC} (HTTP $HTTP_CODE)"
    echo "Backend health check failed: HTTP $HTTP_CODE" >> "$FAIL_LOG"
    ((FAILED++))
fi

# Test 2: Arena context API
echo -n "🔍 Arena context API... "
RESPONSE=$(curl -s -H "Authorization: Bearer $JWT" "$BACKEND/api/arena/context" 2>/dev/null)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $JWT" "$BACKEND/api/arena/context" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ] && echo "$RESPONSE" | grep -q "shared_intelligence"; then
    echo -e "${GREEN}PASS${NC} (HTTP $HTTP_CODE)"
    ((PASSED++))
else
    echo -e "${RED}FAIL${NC} (HTTP $HTTP_CODE)"
    echo "Arena context API failed: HTTP $HTTP_CODE, Response: $RESPONSE" >> "$FAIL_LOG"
    ((FAILED++))
fi

# Test 3: Arena news API
echo -n "🔍 Arena news API... "
RESPONSE=$(curl -s -H "Authorization: Bearer $JWT" "$BACKEND/api/arena/news" 2>/dev/null)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $JWT" "$BACKEND/api/arena/news" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ] && echo "$RESPONSE" | grep -q "articles"; then
    echo -e "${GREEN}PASS${NC} (HTTP $HTTP_CODE)"
    ((PASSED++))
else
    echo -e "${RED}FAIL${NC} (HTTP $HTTP_CODE)"
    echo "Arena news API failed: HTTP $HTTP_CODE, Response: $RESPONSE" >> "$FAIL_LOG"
    ((FAILED++))
fi

# Test 4: Frontend loads
echo -n "🔍 Frontend homepage... "
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND/" 2>/dev/null)
RESPONSE=$(curl -s "$FRONTEND/" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ] && echo "$RESPONSE" | grep -qi "nofx\|<html"; then
    echo -e "${GREEN}PASS${NC} (HTTP $HTTP_CODE)"
    ((PASSED++))
else
    echo -e "${RED}FAIL${NC} (HTTP $HTTP_CODE)"
    echo "Frontend homepage failed: HTTP $HTTP_CODE" >> "$FAIL_LOG"
    ((FAILED++))
fi

# Test 5: Frontend ETH Node page
echo -n "🔍 Frontend ETH Node page... "
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND/eth-node" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}PASS${NC} (HTTP $HTTP_CODE)"
    ((PASSED++))
else
    echo -e "${RED}FAIL${NC} (HTTP $HTTP_CODE)"
    echo "Frontend ETH Node page failed: HTTP $HTTP_CODE" >> "$FAIL_LOG"
    ((FAILED++))
fi

echo ""
echo "=========================================="
echo "📊 Smoke Test Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo "=========================================="

if [ $FAILED -gt 0 ]; then
    echo -e "${RED}❌ SMOKE TESTS FAILED${NC}"
    echo "Failure details logged to: $FAIL_LOG"
    exit 1
else
    echo -e "${GREEN}✅ ALL SMOKE TESTS PASSED${NC}"
    exit 0
fi
