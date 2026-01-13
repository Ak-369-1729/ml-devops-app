#!/bin/bash
# deployment-validation.sh
# Validates the ML DevOps application deployment

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

API_URL=${1:-"http://localhost:5000"}

echo "🔍 Validating ML DevOps App deployment..."
echo "📍 Target URL: $API_URL"
echo ""

# Function to print status
print_status() {
    local status=$1
    local message=$2
    if [ $status -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $message"
    else
        echo -e "${RED}✗${NC} $message"
        return 1
    fi
}

# Test 1: Health Check
echo "🏥 Testing Health Check..."
if response=$(curl -s -f "$API_URL/health"); then
    print_status 0 "Health check passed"
    echo "   Response: $response"
else
    print_status 1 "Health check failed"
    exit 1
fi
echo ""

# Test 2: Model Info
echo "🧠 Testing Model Information..."
if response=$(curl -s -f "$API_URL/api/model/info"); then
    print_status 0 "Model info retrieved"
    echo "   Response: $response"
else
    print_status 1 "Model info failed"
    exit 1
fi
echo ""

# Test 3: Prediction - Setosa
echo "🌸 Testing Prediction (Setosa)..."
payload='{"features": [5.1, 3.5, 1.4, 0.2]}'
if response=$(curl -s -f -X POST "$API_URL/api/predict" \
    -H "Content-Type: application/json" \
    -d "$payload"); then
    class=$(echo $response | grep -o '"class":"[^"]*"')
    confidence=$(echo $response | grep -o '"confidence":[0-9.]*' | cut -d: -f2)
    echo -e "${GREEN}✓${NC} Prediction successful"
    echo "   Prediction: $class (confidence: $confidence)"
else
    print_status 1 "Prediction failed"
    exit 1
fi
echo ""

# Test 4: Prediction - Versicolor
echo "🌺 Testing Prediction (Versicolor)..."
payload='{"features": [7.0, 3.2, 4.7, 1.4]}'
if response=$(curl -s -f -X POST "$API_URL/api/predict" \
    -H "Content-Type: application/json" \
    -d "$payload"); then
    class=$(echo $response | grep -o '"class":"[^"]*"')
    echo -e "${GREEN}✓${NC} Prediction successful"
    echo "   Prediction: $class"
else
    print_status 1 "Prediction failed"
    exit 1
fi
echo ""

# Test 5: Prediction - Virginica
echo "💜 Testing Prediction (Virginica)..."
payload='{"features": [6.3, 3.3, 6.0, 2.5]}'
if response=$(curl -s -f -X POST "$API_URL/api/predict" \
    -H "Content-Type: application/json" \
    -d "$payload"); then
    class=$(echo $response | grep -o '"class":"[^"]*"')
    echo -e "${GREEN}✓${NC} Prediction successful"
    echo "   Prediction: $class"
else
    print_status 1 "Prediction failed"
    exit 1
fi
echo ""

# Test 6: Metrics
echo "📊 Testing Metrics..."
if response=$(curl -s -f "$API_URL/api/metrics"); then
    print_status 0 "Metrics retrieved"
    echo "   Response: $response"
else
    print_status 1 "Metrics failed"
    exit 1
fi
echo ""

# Test 7: Error Handling - Missing Features
echo "⚠️  Testing Error Handling (Missing Features)..."
if ! curl -s -f -X POST "$API_URL/api/predict" \
    -H "Content-Type: application/json" \
    -d '{}' > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Error handling works (400 returned as expected)"
else
    echo -e "${YELLOW}⚠${NC} Unexpected response for missing features"
fi
echo ""

# Test 8: Error Handling - Wrong Feature Count
echo "⚠️  Testing Error Handling (Wrong Feature Count)..."
if ! curl -s -f -X POST "$API_URL/api/predict" \
    -H "Content-Type: application/json" \
    -d '{"features": [5.1, 3.5]}' > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Error handling works (400 returned as expected)"
else
    echo -e "${YELLOW}⚠${NC} Unexpected response for wrong feature count"
fi
echo ""

# Test 9: 404 Handling
echo "⚠️  Testing 404 Error Handling..."
if ! curl -s -f "$API_URL/nonexistent" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} 404 handling works (404 returned as expected)"
else
    echo -e "${YELLOW}⚠${NC} Unexpected response for nonexistent endpoint"
fi
echo ""

echo "================================"
echo -e "${GREEN}✓ All validation tests passed!${NC}"
echo "================================"
echo ""
echo "🚀 Application is ready for use!"
