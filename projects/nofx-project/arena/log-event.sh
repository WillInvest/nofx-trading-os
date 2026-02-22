#!/bin/bash
# log-event.sh — Log agent events to NOFX backend
# Usage: log-event.sh <type> <model> <message> [task] [tokens_in] [tokens_out] [cost] [duration]
# Example: log-event.sh thinking opus 'Analyzing market conditions' hourly-scan
#          log-event.sh dispatch minimax 'Fetching market data' fetch-data 1200 450 0.00066 2.3
#          log-event.sh result deepseek 'Debate completed' debate-btc 15000 8500 0.02835 15.1

set -euo pipefail

# Configuration
API_URL="${API_URL:-http://localhost:8090}"
JWT_SECRET="Fm9Dd/bc2ix30BkhbC22lKy2m/0CDjedaX/TAwkQMGc="
USER_ID="34dd0d3b-bf61-4a6a-82fc-0f0af42355c1"
EMAIL="willinvest11@gmail.com"

# Parse arguments
if [ $# -lt 3 ]; then
    echo "Usage: $0 <type> <model> <message> [task] [tokens_in] [tokens_out] [cost] [duration]"
    echo "Example: $0 dispatch opus 'Starting hourly scan' hourly-scan"
    exit 1
fi

TYPE="$1"
MODEL="$2"
MESSAGE="$3"
TASK="${4:-}"
TOKENS_IN="${5:-0}"
TOKENS_OUT="${6:-0}"
COST="${7:-0}"
DURATION="${8:-0}"

# Generate JWT token using Python
generate_jwt() {
    python3 -c "
import jwt
import time

secret = '$JWT_SECRET'
payload = {
    'user_id': '$USER_ID',
    'email': '$EMAIL',
    'exp': int(time.time()) + 3600  # 1 hour expiry
}
token = jwt.encode(payload, secret, algorithm='HS256')
print(token)
"
}

# Get JWT token
JWT_TOKEN=$(generate_jwt)

# Build JSON payload
PAYLOAD=$(cat <<EOF
{
  "type": "$TYPE",
  "model": "$MODEL",
  "message": "$MESSAGE",
  "task": "$TASK",
  "status": "completed",
  "tokens_in": $TOKENS_IN,
  "tokens_out": $TOKENS_OUT,
  "cost_usd": $COST,
  "duration_s": $DURATION
}
EOF
)

# Make the API request
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/agents/events" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $JWT_TOKEN" \
    -d "$PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "201" ] || [ "$HTTP_CODE" = "200" ]; then
    echo "✓ Event logged: $TYPE $MODEL - $MESSAGE"
    exit 0
else
    echo "✗ Failed to log event (HTTP $HTTP_CODE): $BODY"
    exit 1
fi
