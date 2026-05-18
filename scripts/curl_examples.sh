#!/bin/bash
# ==========================================
# SEAL VERIFICATION API - cURL EXAMPLES
# ==========================================

echo "Seal Verification API - cURL Examples"
echo "======================================"
echo ""

# Configuration
API_URL="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ==========================================
# 1. HEALTH CHECK
# ==========================================

echo -e "${BLUE}1. Health Check${NC}"
echo "Command:"
echo "curl -X GET '$API_URL/health'"
echo ""
echo "Request:"
curl -X GET "$API_URL/health" -H "Content-Type: application/json" -s | json_pp 2>/dev/null || curl -X GET "$API_URL/health" -s
echo ""
echo ""

# ==========================================
# 2. VERIFY SEAL (with file upload)
# ==========================================

echo -e "${BLUE}2. Verify Seal (File Upload)${NC}"
echo "Command:"
echo "curl -X POST '$API_URL/verify-seal' \\"
echo "  -F 'original_image=@path/to/original.jpg' \\"
echo "  -F 'test_image=@path/to/test.jpg'"
echo ""
echo "Example (replace with your image paths):"
echo "curl -X POST '$API_URL/verify-seal' \\"
echo "  -F 'original_image=@input/seal_original.jpg' \\"
echo "  -F 'test_image=@input/seal_test.jpg'"
echo ""
echo ""

# ==========================================
# 3. GET RESULT IMAGE
# ==========================================

echo -e "${BLUE}3. Get Result Image${NC}"
echo "Command:"
echo "curl -X GET '$API_URL/result-image' --output result.jpg"
echo ""
echo "Response: Downloads JPEG image to result.jpg"
echo ""
echo ""

# ==========================================
# 4. VERBOSE REQUEST WITH HEADERS
# ==========================================

echo -e "${BLUE}4. Health Check (Verbose with Headers)${NC}"
echo "Command:"
echo "curl -v -X GET '$API_URL/health'"
echo ""
echo ""

# ==========================================
# 5. SAVE RESPONSE TO FILE
# ==========================================

echo -e "${BLUE}5. Save Verification Response to File${NC}"
echo "Command:"
echo "curl -X POST '$API_URL/verify-seal' \\"
echo "  -F 'original_image=@input/seal_original.jpg' \\"
echo "  -F 'test_image=@input/seal_test.jpg' \\"
echo "  > response.json"
echo ""
echo ""

# ==========================================
# 6. PRETTY PRINT JSON RESPONSE
# ==========================================

echo -e "${BLUE}6. Pretty Print JSON Response${NC}"
echo "Command:"
echo "curl -s -X POST '$API_URL/verify-seal' \\"
echo "  -F 'original_image=@input/seal_original.jpg' \\"
echo "  -F 'test_image=@input/seal_test.jpg' | json_pp"
echo ""
echo ""

# ==========================================
# 7. EXTRACT SPECIFIC FIELD
# ==========================================

echo -e "${BLUE}7. Extract Verdict Only (using jq)${NC}"
echo "Command:"
echo "curl -s -X POST '$API_URL/verify-seal' \\"
echo "  -F 'original_image=@input/seal_original.jpg' \\"
echo "  -F 'test_image=@input/seal_test.jpg' | jq '.verdict'"
echo ""
echo ""

# ==========================================
# 8. TIMEOUT AND ERROR HANDLING
# ==========================================

echo -e "${BLUE}8. Request with Timeout${NC}"
echo "Command:"
echo "curl -X POST '$API_URL/verify-seal' \\"
echo "  -m 30 \\"
echo "  -F 'original_image=@input/seal_original.jpg' \\"
echo "  -F 'test_image=@input/seal_test.jpg'"
echo ""
echo "Parameters:"
echo "  -m 30 : 30 seconds timeout"
echo ""
echo ""

# ==========================================
# 9. BATCH REQUEST EXAMPLE
# ==========================================

echo -e "${BLUE}9. Batch Processing Script Example${NC}"
echo "#!/bin/bash"
echo "for image_pair in input/batch/*; do"
echo "  original=\$image_pair/original.jpg"
echo "  test=\$image_pair/test.jpg"
echo "  curl -s -X POST '$API_URL/verify-seal' \\"
echo "    -F \"original_image=@\$original\" \\"
echo "    -F \"test_image=@\$test\" | jq '.verdict'"
echo "done"
echo ""
echo ""

# ==========================================
# 10. AUTHENTICATION EXAMPLE (if needed)
# ==========================================

echo -e "${BLUE}10. Request with Custom Headers${NC}"
echo "Command:"
echo "curl -X POST '$API_URL/verify-seal' \\"
echo "  -H 'Authorization: Bearer YOUR_TOKEN' \\"
echo "  -H 'X-Custom-Header: value' \\"
echo "  -F 'original_image=@input/seal_original.jpg' \\"
echo "  -F 'test_image=@input/seal_test.jpg'"
echo ""
echo ""

# ==========================================
# HELPFUL TIPS
# ==========================================

echo -e "${YELLOW}============================================${NC}"
echo -e "${YELLOW}HELPFUL TIPS${NC}"
echo -e "${YELLOW}============================================${NC}"
echo ""
echo "1. Check if API is running:"
echo "   curl -X GET '$API_URL/health'"
echo ""
echo "2. Common cURL flags:"
echo "   -X GET/POST/PUT/DELETE  : HTTP method"
echo "   -H 'Header: value'      : Add header"
echo "   -d '{json}'             : Send JSON data"
echo "   -F 'field=@file'        : Upload file"
echo "   -o filename             : Save output to file"
echo "   -s                       : Silent mode"
echo "   -v                       : Verbose mode"
echo "   -m seconds              : Timeout"
echo ""
echo "3. Pretty print JSON (install jq):"
echo "   brew install jq         (macOS)"
echo "   apt install jq          (Ubuntu/Debian)"
echo "   choco install jq        (Windows)"
echo ""
echo "4. Test with Windows (PowerShell):"
echo "   Invoke-WebRequest -Uri '$API_URL/health' -Method GET"
echo ""
echo "5. View API Swagger UI:"
echo "   Open browser: $API_URL/docs"
echo ""
