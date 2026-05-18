# 🔐 Seal Verification API Guide

## Overview

This API provides endpoints for verifying seal authenticity using advanced image comparison and feature matching techniques. It uses the same verification algorithm from `verifier.py` but exposes it as a RESTful web service.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API

**Using PowerShell:**
```powershell
.\run_api.ps1
```

**Using Command Prompt:**
```cmd
run_api.bat
```

**Using Direct Python:**
```bash
python api.py
```

The API will start on `http://localhost:8000`

### 3. Access API Documentation

- **Swagger UI (Interactive)**: http://localhost:8000/docs
- **ReDoc (Beautiful Docs)**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## API Endpoints

### 1. Health Check
Check if the API is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

**Example with cURL:**
```bash
curl http://localhost:8000/health
```

---

### 2. Verify Seal (Main Endpoint)
Verify seal authenticity by comparing two images.

**Endpoint:** `POST /verify-seal`

**Parameters:**
- `original_image` (File) - Original/Reference seal image
- `test_image` (File) - Test/Sample seal image to verify

**Response:**
```json
{
  "match_percent": 85.5,
  "verdict": "GENUINE SEAL",
  "output_image": "output/result.jpg",
  "message": "Seal verification completed successfully",
  "original_image": "original_seal.jpg",
  "test_image": "test_seal.jpg"
}
```

**Verdict Types:**
- `GENUINE SEAL` - Match > 70%
- `SUSPICIOUS SEAL` - Match between 50-70%
- `TAMPERED SEAL` - Match < 50%

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/verify-seal" \
  -F "original_image=@path/to/original.jpg" \
  -F "test_image=@path/to/test.jpg"
```

**Example with Python:**
```python
import requests

files = {
    'original_image': open('original_seal.jpg', 'rb'),
    'test_image': open('test_seal.jpg', 'rb'),
}

response = requests.post(
    'http://localhost:8000/verify-seal',
    files=files
)

print(response.json())
```

**Example with JavaScript (Fetch API):**
```javascript
const formData = new FormData();
formData.append('original_image', originalImageFile);
formData.append('test_image', testImageFile);

fetch('http://localhost:8000/verify-seal', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### 3. Get Result Image
Download the last generated result image with feature matches highlighted.

**Endpoint:** `GET /result-image`

**Response:** Binary image file (JPEG)

**Example with cURL:**
```bash
curl http://localhost:8000/result-image --output result.jpg
```

---

## Testing the API

### Using the Python Test Script

```bash
python test_api.py
```

This script will:
1. Check API health
2. Run verification on test images in the `input` folder
3. Retrieve the result image
4. Display comprehensive test results

### Using Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click on the "Try it out" button for each endpoint
3. Upload files and submit requests directly from the browser

### Using Postman

1. Open Postman
2. Create a new POST request to `http://localhost:8000/verify-seal`
3. Go to Body → form-data
4. Add two file fields:
   - Key: `original_image` (File type)
   - Key: `test_image` (File type)
5. Select your test images and send

---

## File Structure

```
SealVerification/
├── api.py                  # FastAPI application
├── verifier.py             # Core verification logic
├── test_api.py             # API test script
├── swagger.html            # Standalone Swagger UI
├── run_api.bat             # Windows batch startup script
├── run_api.ps1             # PowerShell startup script
├── requirements.txt        # Python dependencies
├── input/                  # Input images directory
├── output/                 # Output results directory
└── README.md              # Documentation
```

---

## Algorithm Details

The verification process uses:

1. **Image Loading & Preprocessing**
   - Convert to grayscale
   - Gaussian blur (5x5 kernel)
   - Histogram equalization

2. **Feature Detection**
   - ORB (Oriented FAST and Rotated BRIEF) detection
   - 5000 features extracted per image

3. **Feature Matching**
   - BFMatcher with NORM_HAMMING distance
   - Lowe's ratio test (0.75 threshold)

4. **Scoring**
   - Raw match score: (good_matches / total_features) × 100
   - Homography validation with RANSAC
   - Combined score: 0.7 × raw_score + 0.3 × homography_score
   - Normalized score: (raw_score / 45) × 100

5. **Verdict**
   - GENUINE SEAL: > 70%
   - SUSPICIOUS SEAL: 50-70%
   - TAMPERED SEAL: < 50%

---

## Error Handling

### Common Errors and Solutions

**Error: "Verification failed"**
- Ensure both images are valid image files
- Try larger, clearer images
- Supported formats: JPG, PNG, BMP

**Error: "Connection refused"**
- Make sure the API is running: `python api.py`
- Check port 8000 is not in use
- Try: `lsof -i :8000` (Mac/Linux) or `netstat -ano | findstr :8000` (Windows)

**Error: 422 Unprocessable Entity**
- Check that both file fields are provided
- Ensure field names are correct: `original_image`, `test_image`

---

## Performance Tips

1. **Image Size**
   - Optimal: 800x600 resolution
   - Larger images = more processing time
   - API auto-resizes to 800x600

2. **Image Quality**
   - Use clear, well-lit images
   - Avoid compression artifacts
   - Consistent lighting between original and test

3. **Processing Time**
   - Average: 2-5 seconds per verification
   - Depends on system performance and image quality

---

## API Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid images) |
| 404 | Result image not found |
| 422 | Missing required fields |
| 500 | Server error |

---

## CORS Configuration

The API has CORS enabled to accept requests from any origin. To modify CORS settings, edit `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],  # Specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Deployment

### Running on a Different Port

```bash
# Edit api.py or run directly
python -c "from api import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=5000)"
```

### Production Deployment

For production, use a production server like Gunicorn with Uvicorn workers:

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
```

---

## Troubleshooting

### API Won't Start
```bash
# Check Python version
python --version  # Should be 3.7+

# Verify dependencies
pip list | grep -i fastapi

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Image Processing Issues
- Ensure OpenCV is installed: `pip install opencv-python`
- Check image file permissions
- Verify image is not corrupted

---

## Support

For issues or questions:
1. Check the error message carefully
2. Review this guide
3. Run the test script: `python test_api.py`
4. Check console output for detailed error messages

---

**Last Updated:** 2026-05-15
**Version:** 1.0.0
**Status:** Production Ready ✓
