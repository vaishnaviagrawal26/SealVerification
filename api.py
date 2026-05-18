from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from pathlib import Path

from verifier import verify_seal

# ==========================================
# CREATE FASTAPI APP
# ==========================================

app = FastAPI(
    title="Seal Verification API",
    description="API for verifying seal authenticity using image comparison and feature matching",
    version="1.0.0"
)

# ==========================================
# ADD CORS MIDDLEWARE
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# HEALTH CHECK ENDPOINT
# ==========================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Check if the API is running"""
    return {"status": "healthy"}

# ==========================================
# SEAL VERIFICATION ENDPOINT
# ==========================================

@app.post("/verify-seal", tags=["Verification"])
async def verify_seal_endpoint(
    original_image: UploadFile = File(..., description="Original/Reference seal image"),
    test_image: UploadFile = File(..., description="Test/Sample seal image to verify")
):
    """
    Verify seal authenticity by comparing two images.
    
    Returns:
    - match_percent: Similarity percentage (0-100)
    - verdict: Classification result (GENUINE SEAL, SUSPICIOUS SEAL, or TAMPERED SEAL)
    - output_image: Path to the result image with feature matches highlighted
    """
    
    try:
        # Ensure input directory exists
        input_dir = Path("input")
        input_dir.mkdir(exist_ok=True)
        
        # Ensure output directory exists
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Save uploaded files temporarily
        original_path = f"input/original_{original_image.filename}"
        test_path = f"input/test_{test_image.filename}"
        
        # Save original image
        with open(original_path, "wb") as buffer:
            shutil.copyfileobj(original_image.file, buffer)
        
        # Save test image
        with open(test_path, "wb") as buffer:
            shutil.copyfileobj(test_image.file, buffer)
        
        # Verify seal
        result = verify_seal(original_path, test_path)
        
        if result is None:
            raise HTTPException(
                status_code=400,
                detail="Verification failed. Please ensure both images are valid and in proper format."
            )
        
        # Return result with additional metadata
        return {
            **result,
            "message": "Seal verification completed successfully",
            "original_image": original_image.filename,
            "test_image": test_image.filename
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during verification: {str(e)}"
        )
    finally:
        # Cleanup uploaded files
        try:
            if os.path.exists(original_path):
                os.remove(original_path)
            if os.path.exists(test_path):
                os.remove(test_path)
        except:
            pass

# ==========================================
# GET RESULT IMAGE ENDPOINT
# ==========================================

@app.get("/result-image", tags=["Results"])
async def get_result_image():
    """Download the last generated result image with feature matches"""
    result_path = "output/result.jpg"
    
    if not os.path.exists(result_path):
        raise HTTPException(
            status_code=404,
            detail="No result image available. Please run verification first."
        )
    
    return FileResponse(result_path, media_type="image/jpeg")

# ==========================================
# SWAGGER UI CUSTOMIZATION
# ==========================================

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ==========================================
    SEAL VERIFICATION API
    ==========================================
    
    API Running at: http://localhost:8000
    Swagger Docs: http://localhost:8000/docs
    ReDoc Docs: http://localhost:8000/redoc
    
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
