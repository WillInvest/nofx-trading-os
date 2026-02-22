#!/bin/bash
# Rollback to last backup Docker images
# Usage: ./rollback.sh

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "=========================================="
echo "🔄 NOFX Platform Rollback"
echo "=========================================="
echo ""

# Step 1: Find latest backup
echo -e "${BLUE}🔍 Step 1: Finding latest backup tag...${NC}"
BACKUP_TAG=$(docker images nofx-nofx --format '{{.Tag}}' | grep backup | sort -r | head -1)

if [ -z "$BACKUP_TAG" ]; then
    echo -e "${RED}❌ No backup images found!${NC}"
    echo "Cannot rollback - no backup tags available."
    exit 1
fi

echo -e "${GREEN}✓ Found backup: $BACKUP_TAG${NC}"
echo ""

# Step 2: Stop containers
echo -e "${BLUE}🛑 Step 2: Stopping containers...${NC}"
cd /home/openclaw/.openclaw/workspace/projects/nofx-project/nofx
docker compose stop
echo -e "${GREEN}✓ Containers stopped${NC}"
echo ""

# Step 3: Retag backup as latest
echo -e "${BLUE}🏷️  Step 3: Restoring backup images...${NC}"
docker tag nofx-nofx:$BACKUP_TAG nofx-nofx:latest
docker tag nofx-frontend:$BACKUP_TAG nofx-frontend:latest
echo -e "${GREEN}✓ Images restored from $BACKUP_TAG${NC}"
echo ""

# Step 4: Start containers
echo -e "${BLUE}🚀 Step 4: Starting containers...${NC}"
docker compose up -d
echo -e "${GREEN}✓ Containers started${NC}"
echo ""

# Step 5: Wait for services
echo -e "${BLUE}⏳ Step 5: Waiting for services...${NC}"
sleep 5
echo ""

# Step 6: Run smoke tests
echo -e "${BLUE}🧪 Step 6: Running smoke tests...${NC}"
if ../scripts/smoke-test.sh; then
    echo ""
    echo "=========================================="
    echo -e "${GREEN}✅ ROLLBACK SUCCESSFUL!${NC}"
    echo "=========================================="
    echo "Restored to backup: $BACKUP_TAG"
    exit 0
else
    echo ""
    echo "=========================================="
    echo -e "${RED}❌ ROLLBACK FAILED - SMOKE TESTS FAILED${NC}"
    echo "=========================================="
    echo "The rollback was applied but smoke tests still fail."
    echo "Manual intervention required."
    exit 1
fi
