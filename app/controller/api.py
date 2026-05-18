import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
import cv2
import numpy as np

from app.model.verifier import verify_seal

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
    
    original_path = None
    
    try:
        # Create directories
        os.makedirs("input", exist_ok=True)
        os.makedirs("output", exist_ok=True)
        
        # Save original image to disk (for verification/comparison)
        original_path = f"input/original_{original_image.filename}"
        with open(original_path, "wb") as buffer:
            shutil.copyfileobj(original_image.file, buffer)
        
        print(f"Original image saved: {original_path}")
        
        # Read test image directly into memory as numpy array (no disk save)
        test_bytes = await test_image.read()
        test_image_np = cv2.imdecode(np.frombuffer(test_bytes, np.uint8), cv2.IMREAD_COLOR)
        
        print(f"Test image loaded to memory. Shape: {test_image_np.shape if test_image_np is not None else 'None'}")
        
        if test_image_np is None:
            raise Exception("Test image could not be decoded. Invalid image format.")
        
        # Verify seal
        print(f"Starting verification...")
        result = verify_seal(original_path, test_image_np)
        
        print(f"Verification result: {result}")
        
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
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=f"Error: {str(e)}"
        )
    finally:
        # Note: Original image is kept in input/ folder for later verification
        # Only cleanup if there was an error
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
