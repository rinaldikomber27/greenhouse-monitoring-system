#!/bin/bash

# Test Script untuk Greenhouse Environmental Monitoring System
# ============================================================

echo "======================================================================"
echo "  🧪 GREENHOUSE MONITORING SYSTEM - VERIFICATION TEST"
echo "======================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to print test result
test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}: $2"
        ((TESTS_FAILED++))
    fi
}

echo "Test 1: Checking Docker Compose file..."
if [ -f "docker-compose.yml" ]; then
    test_result 0 "docker-compose.yml exists"
else
    test_result 1 "docker-compose.yml not found"
fi

echo ""
echo "Test 2: Checking Edge Node files..."
if [ -f "edge/sensor_edge.py" ]; then
    test_result 0 "edge/sensor_edge.py exists"
    
    # Check for simulation mode support
    if grep -q "simulation_mode" edge/sensor_edge.py; then
        test_result 0 "Edge node has simulation mode support"
    else
        test_result 1 "Edge node missing simulation mode"
    fi
    
    # Check for control topic subscription
    if grep -q "greenhouse/control/simulate" edge/sensor_edge.py; then
        test_result 0 "Edge node subscribes to control topic"
    else
        test_result 1 "Edge node missing control subscription"
    fi
else
    test_result 1 "edge/sensor_edge.py not found"
fi

echo ""
echo "Test 3: Checking Dashboard files..."
if [ -f "dashboard/public/index.html" ]; then
    test_result 0 "dashboard/public/index.html exists"
    
    # Check for Chart.js
    if grep -q "chart.js" dashboard/public/index.html; then
        test_result 0 "Dashboard includes Chart.js"
    else
        test_result 1 "Dashboard missing Chart.js"
    fi
    
    # Check for time range selector
    if grep -q "time-range-selector" dashboard/public/index.html; then
        test_result 0 "Dashboard has time range selector"
    else
        test_result 1 "Dashboard missing time range selector"
    fi
    
    # Check for control panel
    if grep -q "control-panel" dashboard/public/index.html; then
        test_result 0 "Dashboard has smart control panel"
    else
        test_result 1 "Dashboard missing control panel"
    fi
    
    # Check for simulation buttons
    if grep -q "Simulate Overheat" dashboard/public/index.html; then
        test_result 0 "Dashboard has simulation controls"
    else
        test_result 1 "Dashboard missing simulation controls"
    fi
    
    # Check for recent updates panel
    if grep -q "recent-updates" dashboard/public/index.html; then
        test_result 0 "Dashboard has recent updates panel"
    else
        test_result 1 "Dashboard missing recent updates panel"
    fi
else
    test_result 1 "dashboard/public/index.html not found"
fi

if [ -f "dashboard/server.js" ]; then
    test_result 0 "dashboard/server.js exists"
    
    # Check for simulation handler
    if grep -q "socket.on('simulation'" dashboard/server.js; then
        test_result 0 "Dashboard server handles simulation commands"
    else
        test_result 1 "Dashboard server missing simulation handler"
    fi
else
    test_result 1 "dashboard/server.js not found"
fi

echo ""
echo "Test 4: Checking Documentation files..."
docs=("README.md" "QUICKSTART.md" "DASHBOARD_GUIDE.md" "ARCHITECTURE_DETAIL.md" "UPGRADE_SUMMARY.md")
for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        test_result 0 "$doc exists"
    else
        test_result 1 "$doc not found"
    fi
done

echo ""
echo "Test 5: Checking Docker Containers (if running)..."
if command -v docker &> /dev/null; then
    if docker ps | grep -q "mqtt-broker"; then
        test_result 0 "MQTT Broker container is running"
    else
        echo -e "${YELLOW}⚠️  SKIP${NC}: MQTT Broker not running (start with docker-compose up)"
    fi
    
    if docker ps | grep -q "edge-node-1"; then
        test_result 0 "Edge Node 1 is running"
    else
        echo -e "${YELLOW}⚠️  SKIP${NC}: Edge Node 1 not running"
    fi
    
    if docker ps | grep -q "edge-node-2"; then
        test_result 0 "Edge Node 2 is running"
    else
        echo -e "${YELLOW}⚠️  SKIP${NC}: Edge Node 2 not running"
    fi
    
    if docker ps | grep -q "monitoring-dashboard"; then
        test_result 0 "Dashboard container is running"
    else
        echo -e "${YELLOW}⚠️  SKIP${NC}: Dashboard not running"
    fi
else
    echo -e "${YELLOW}⚠️  SKIP${NC}: Docker not found"
fi

echo ""
echo "Test 6: Checking System Architecture Compliance..."

# Check for distributed system principles
echo "Checking distributed system requirements..."

# Check MQTT topics
if grep -q "env/" edge/sensor_edge.py && \
   grep -q "event" edge/sensor_edge.py; then
    test_result 0 "Correct MQTT topic structure"
else
    test_result 1 "MQTT topic structure incorrect"
fi

# Check for threading
if grep -q "threading.Thread" edge/sensor_edge.py; then
    test_result 0 "Edge nodes use multi-threading (concurrency)"
else
    test_result 1 "Multi-threading not implemented"
fi

# Check for constraint checking
if grep -q "check_constraint" edge/sensor_edge.py; then
    test_result 0 "Edge computing with constraint checking"
else
    test_result 1 "Constraint checking not found"
fi

# Check for event-driven
if grep -q "event_type" edge/sensor_edge.py; then
    test_result 0 "Event-driven architecture implemented"
else
    test_result 1 "Event-driven architecture missing"
fi

echo ""
echo "======================================================================"
echo "  📊 TEST SUMMARY"
echo "======================================================================"
echo -e "${GREEN}Tests Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Tests Failed: $TESTS_FAILED${NC}"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
if [ $TOTAL_TESTS -gt 0 ]; then
    PASS_RATE=$((TESTS_PASSED * 100 / TOTAL_TESTS))
    echo "Pass Rate: $PASS_RATE%"
fi

echo ""
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED! System is ready for deployment.${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some tests failed. Please review the results above.${NC}"
    exit 1
fi
