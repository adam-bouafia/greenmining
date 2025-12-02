#!/bin/bash
# Run complete test suite for greenmining

set -e

echo "🧪 Running greenmining Test Suite"
echo "================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo -e "${YELLOW}Warning: No virtual environment found${NC}"
fi

# Install test dependencies
echo -e "${YELLOW}Installing test dependencies...${NC}"
pip install -q pytest pytest-cov pytest-mock

# Run unit tests
echo ""
echo -e "${YELLOW}Running unit tests...${NC}"
if [ -d "tests" ]; then
    python -m pytest tests/ -v --tb=short
elif [ -d "greenmining/tests" ]; then
    python -m pytest greenmining/tests/ -v --tb=short
else
    echo -e "${YELLOW}No tests directory found, skipping tests${NC}"
fi

# Run with coverage
echo ""
echo -e "${YELLOW}Generating coverage report...${NC}"
if [ -d "tests" ]; then
    python -m pytest tests/ \
        --cov=greenmining \
        --cov-report=html \
        --cov-report=term-missing \
        --tb=short
elif [ -d "greenmining/tests" ]; then
    python -m pytest greenmining/tests/ \
        --cov=greenmining \
        --cov-report=html \
        --cov-report=term-missing \
        --tb=short
fi

echo ""
echo -e "${GREEN}✅ Test suite completed!${NC}"
if [ -f "htmlcov/index.html" ]; then
    echo -e "Coverage report: file://$(pwd)/htmlcov/index.html"
fi
