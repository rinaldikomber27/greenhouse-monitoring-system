#!/bin/bash

# Startup script for MQTT Environmental Monitoring System
# Distributed System with Edge Computing + Event-Driven Architecture

echo "════════════════════════════════════════════════════════════════════"
echo "  🌍 MQTT Environmental Monitoring - Distributed System"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose found${NC}"
echo ""

# Clean up previous containers (optional)
echo -e "${YELLOW}🧹 Cleaning up previous containers...${NC}"
docker-compose down 2>/dev/null
echo ""

# Build and start containers
echo -e "${BLUE}🔨 Building and starting distributed system...${NC}"
echo ""
docker-compose up --build -d

# Wait for services to start
echo ""
echo -e "${YELLOW}⏳ Waiting for services to initialize...${NC}"
sleep 10

# Check service status
echo ""
echo -e "${BLUE}📊 Service Status:${NC}"
echo "─────────────────────────────────────────────────────────────────────"
docker-compose ps
echo "─────────────────────────────────────────────────────────────────────"

echo ""
echo -e "${GREEN}✅ Distributed system is running!${NC}"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo -e "${BLUE}📍 Access Points:${NC}"
echo "═══════════════════════════════════════════════════════════════════"
echo -e "  🌐 Dashboard:        ${GREEN}http://localhost:3000${NC}"
echo -e "  📡 MQTT Broker:      ${GREEN}mqtt://localhost:1883${NC}"
echo -e "  📊 MongoDB:          ${GREEN}mongodb://localhost:27017${NC}"
echo "═══════════════════════════════════════════════════════════════════"

echo ""
echo -e "${BLUE}📝 Useful Commands:${NC}"
echo "─────────────────────────────────────────────────────────────────────"
echo "  View all logs:           docker-compose logs -f"
echo "  View edge node logs:     docker-compose logs -f sensor-edge-1"
echo "  View dashboard logs:     docker-compose logs -f monitoring-dashboard"
echo "  View MQTT messages:      docker exec -it mqtt-broker mosquitto_sub -t 'env/#' -v"
echo "  Stop system:             docker-compose down"
echo "  Restart system:          docker-compose restart"
echo "─────────────────────────────────────────────────────────────────────"

echo ""
echo -e "${GREEN}🚀 Open http://localhost:3000 in your browser to see the dashboard!${NC}"
echo ""
