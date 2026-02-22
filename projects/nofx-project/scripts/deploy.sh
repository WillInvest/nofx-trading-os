#!/bin/bash
# Safe deploy: git commit → backup → build → smoke test → deploy → smoke test
# Usage: ./deploy.sh "description of changes"

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

DEPLOY_DESC="${1:-manual deploy}"

echo "=========================================="
echo "🚀 NOFX Platform Deploy"
echo "=========================================="
echo -e "Description: ${YELLOW}$DEPLOY_DESC${NC}"
echo ""

# Step 1: Git commit
echo -e "${BLUE}📝 Step 1: Git commit changes...${NC}"
cd /home/openclaw/.openclaw/workspace/projects/nofx-project/nofx
git add -A
git commit -m "pre-deploy: $DEPLOY_DESC" --allow-empty
echo -e "${GREEN}✓ Git commit complete${NC}"
echo ""

# Step 2: Backup Docker images
echo -e "${BLUE}📦 Step 2: Backing up Docker images...${NC}"
BACKUP_TAG="backup-$(date +%Y%m%d-%H%M)"
docker tag nofx-nofx:latest nofx-nofx:$BACKUP_TAG 2>/dev/null || true
docker tag nofx-frontend:latest nofx-frontend:$BACKUP_TAG 2>/dev/null || true
echo -e "${GREEN}✓ Backup created: $BACKUP_TAG${NC}"
echo ""

# Step 3: Build frontend
echo -e "${BLUE}🔨 Step 3: Building frontend...${NC}"
cd /home/openclaw/.openclaw/workspace/projects/nofx-project/nofx/web
npm run build
cd ..
echo -e "${GREEN}✓ Frontend build complete${NC}"
echo ""

# Step 4: Build Docker images
echo -e "${BLUE}🐳 Step 4: Building Docker images...${NC}"
docker compose build --no-cache nofx nofx-frontend
echo -e "${GREEN}✓ Docker images built${NC}"
echo ""

# Step 5: Deploy containers
echo -e "${BLUE}🚀 Step 5: Deploying containers...${NC}"
docker compose up -d
echo -e "${GREEN}✓ Containers deployed${NC}"
echo ""

# Step 6: Wait for services
echo -e "${BLUE}⏳ Step 6: Waiting for services to start...${NC}"
sleep 5
echo ""

# Step 7: Run smoke tests
echo -e "${BLUE}🧪 Step 7: Running smoke tests...${NC}"
if ../scripts/smoke-test.sh; then
    echo ""
    echo "=========================================="
    echo -e "${GREEN}✅ DEPLOY SUCCESSFUL!${NC}"
    echo "=========================================="
    echo "Your changes are live!"
    exit 0
else
    echo ""
    echo "=========================================="
    echo -e "${RED}❌ SMOKE TESTS FAILED${NC}"
    echo "=========================================="
    echo ""
    echo -e "${YELLOW}⚠️  ROLLBACK INSTRUCTIONS:${NC}"
    echo "To rollback to the backup, run:"
    echo ""
    echo "  docker stop \$(docker ps -q -f name=nofx)"
    echo "  docker tag nofx-nofx:$BACKUP_TAG nofx-nofx:latest"
    echo "  docker tag nofx-frontend:$BACKUP_TAG nofx-frontend:latest"
    echo "  docker compose up -d"
    echo ""
    echo "Or use the rollback script:"
    echo "  ./scripts/rollback.sh"
    exit 1
fi
