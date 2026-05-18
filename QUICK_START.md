# 🔐 Seal Verification API - Quick Reference

## Files Created

✅ **api.py** - FastAPI application with endpoints for seal verification
✅ **swagger.html** - Standalone Swagger UI for testing
✅ **test_api.py** - Python script to test API endpoints
✅ **run_api.bat** - Windows batch script to start API
✅ **run_api.ps1** - PowerShell script to start API
✅ **API_GUIDE.md** - Comprehensive API documentation
✅ **curl_examples.sh** - cURL examples for testing
✅ **requirements.txt** - Updated with FastAPI and uvicorn

---

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start API
```bash
# PowerShell
.\run_api.ps1

# Command Prompt
run_api.bat

# Or directly
python api.py
```

### Step 3: Test API
Open browser: **http://localhost:8000/docs**

---

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Check API status |
| POST | `/verify-seal` | Verify seal authenticity |
| GET | `/result-image` | Download result image |

---

## Verify Seal Request

**URL:** `http://localhost:8000/verify-seal`

**Method:** POST

**Body (form-data):**
```
original_image: [binary file]
test_image: [binary file]
```

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

---

## Verdict Meanings

| Verdict | Match Score | Meaning |
|---------|-------------|---------|
| GENUINE SEAL | > 70% | Authentic seal, good match |
| SUSPICIOUS SEAL | 50-70% | Possibly modified |
| TAMPERED SEAL | < 50% | Likely compromised |

---

## Testing Tools

### 1. Browser Swagger UI
```
http://localhost:8000/docs
```

### 2. Python Test Script
```bash
python test_api.py
```

### 3. cURL Command
```bash
curl -X POST "http://localhost:8000/verify-seal" \
  -F "original_image=@input/original.jpg" \
  -F "test_image=@input/test.jpg"
```

### 4. PowerShell
```powershell
$original = Get-Item "input/original.jpg"
$test = Get-Item "input/test.jpg"

$form = @{
    original_image = $original
    test_image = $test
}

Invoke-WebRequest -Uri "http://localhost:8000/verify-seal" `
    -Method Post -Form $form
```

### 5. Postman
1. Create POST request to `http://localhost:8000/verify-seal`
2. Go to Body → form-data
3. Add `original_image` (File type)
4. Add `test_image` (File type)
5. Send

---

## Documentation Links

- **Full Guide:** [API_GUIDE.md](API_GUIDE.md)
- **cURL Examples:** [curl_examples.sh](curl_examples.sh)
- **Swagger UI:** http://localhost:8000/docs (when running)
- **ReDoc UI:** http://localhost:8000/redoc (when running)

---

## Troubleshooting

**API won't start:**
```bash
# Check port
netstat -ano | findstr :8000

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Import errors:**
```bash
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall packages
pip install fastapi uvicorn python-multipart opencv-python
```

**Connection refused:**
- Make sure API is running: `python api.py`
- Verify port 8000 is accessible
- Check firewall settings

---

## Next Steps

1. ✅ Ensure test images are in the `input/` folder
2. ✅ Start the API: `python api.py`
3. ✅ Open http://localhost:8000/docs in browser
4. ✅ Use "Try it out" button to upload test images
5. ✅ Check results in `output/` folder

---

**Status:** ✅ Ready to use
**Version:** 1.0.0
**Created:** 2026-05-15
