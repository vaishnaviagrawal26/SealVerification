import requests
import os
from pathlib import Path

# ==========================================
# API TEST SCRIPT
# ==========================================

API_URL = "http://localhost:8000"
VERIFY_ENDPOINT = f"{API_URL}/verify-seal"
HEALTH_ENDPOINT = f"{API_URL}/health"
RESULT_IMAGE_ENDPOINT = f"{API_URL}/result-image"

def test_api():
    """Test the Seal Verification API"""
    
    print("=" * 50)
    print("SEAL VERIFICATION API - TEST SCRIPT")
    print("=" * 50)
    
    # ==========================================
    # TEST 1: HEALTH CHECK
    # ==========================================
    
    print("\n1. Testing Health Check Endpoint...")
    try:
        response = requests.get(HEALTH_ENDPOINT)
        if response.status_code == 200:
            print(f"✓ Health Check Passed: {response.json()}")
        else:
            print(f"✗ Health Check Failed: {response.status_code}")
            return
    except Exception as e:
        print(f"✗ Error: {e}")
        print("Make sure the API is running on http://localhost:8000")
        return
    
    # ==========================================
    # TEST 2: SEAL VERIFICATION
    # ==========================================
    
    print("\n2. Testing Seal Verification Endpoint...")
    
    # Look for test images in the input directory
    input_dir = Path("input")
    
    if not input_dir.exists():
        print("✗ Input directory not found. Please create test images in 'input' folder.")
        return
    
    # Find image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    images = []
    
    for ext in image_extensions:
        images.extend(list(input_dir.glob(f"*{ext}")))
        images.extend(list(input_dir.glob(f"*{ext.upper()}")))
    
    if len(images) < 2:
        print(f"✗ Need at least 2 test images in 'input' folder. Found {len(images)}")
        print("   Example images: original_seal.jpg, test_seal.jpg")
        return
    
    # Use first two images
    original_image = str(images[0])
    test_image = str(images[1])
    
    print(f"   Using images:")
    print(f"   - Original: {original_image}")
    print(f"   - Test: {test_image}")
    
    try:
        with open(original_image, 'rb') as orig_file, open(test_image, 'rb') as test_file:
            files = {
                'original_image': (Path(original_image).name, orig_file, 'image/jpeg'),
                'test_image': (Path(test_image).name, test_file, 'image/jpeg'),
            }
            
            response = requests.post(VERIFY_ENDPOINT, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ Verification Successful!")
            print(f"   Match Percent: {result.get('match_percent')}%")
            print(f"   Verdict: {result.get('verdict')}")
            print(f"   Output Image: {result.get('output_image')}")
            print(f"\nFull Response:")
            for key, value in result.items():
                print(f"   {key}: {value}")
        else:
            print(f"✗ Verification Failed: {response.status_code}")
            print(f"   Error: {response.json()}")
    
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # ==========================================
    # TEST 3: GET RESULT IMAGE
    # ==========================================
    
    print("\n3. Testing Get Result Image Endpoint...")
    try:
        response = requests.get(RESULT_IMAGE_ENDPOINT)
        if response.status_code == 200:
            print("✓ Result Image Retrieved Successfully")
            print(f"   Content-Type: {response.headers.get('content-type')}")
            print(f"   Image Size: {len(response.content)} bytes")
        else:
            print(f"✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # ==========================================
    # SUMMARY
    # ==========================================
    
    print("\n" + "=" * 50)
    print("API ENDPOINTS AVAILABLE:")
    print("=" * 50)
    print(f"Health Check: GET {HEALTH_ENDPOINT}")
    print(f"Verify Seal: POST {VERIFY_ENDPOINT}")
    print(f"Get Result: GET {RESULT_IMAGE_ENDPOINT}")
    print("\nSwagger UI: http://localhost:8000/docs")
    print("ReDoc UI: http://localhost:8000/redoc")
    print("=" * 50)

if __name__ == "__main__":
    test_api()
