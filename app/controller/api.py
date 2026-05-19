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
import uuid

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
# S3 UPLOAD FUNCTION
# ==========================================

async def upload_file_to_s3(file: UploadFile, folder_path: str = "Dairy/upload/files") -> str:
    """
    Upload a file to S3 via the SecuTrak API.
    
    Args:
        file: The file to upload
        folder_path: S3 folder path
        
    Returns:
        S3 URL of the uploaded file
    """
    import httpx
    
    file_name = file.filename
    content_type = file.content_type
    file_bytes = await file.read()

    unique_reference = uuid.uuid4().hex
    filepath = f"{folder_path}/{unique_reference}_{file_name}"

    url = "https://api-py.secutrak.in/api/uploadfiletos3/"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            data={"filepath": filepath},
            files={"file": (file_name, file_bytes, content_type)}
        )
        return response.json()["url"]

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
    
    Workflow:
    1. Upload original image to S3
    2. Download from S3 URL for verification
    3. Load test image into memory
    4. Compare images
    
    Returns:
    - match_percent: Similarity percentage (0-100)
    - verdict: Classification result (GENUINE SEAL, SUSPICIOUS SEAL, or TAMPERED SEAL)
    - output_image: Path to the result image with feature matches highlighted
    - original_image_s3_url: S3 URL of the uploaded original image
    """
    
    original_s3_url = None
    
    try:
        # Create output directory
        os.makedirs("output", exist_ok=True)
        
        print(f"Starting seal verification workflow...")
        
        # Step 1: Upload original image to S3
        print(f"Uploading original image to S3...")
        original_s3_url = await upload_file_to_s3(original_image)
        print(f"Original image uploaded to S3: {original_s3_url}")
        
        # Step 2: Read test image into memory
        test_bytes = await test_image.read()
        test_image_np = cv2.imdecode(np.frombuffer(test_bytes, np.uint8), cv2.IMREAD_COLOR)
        
        print(f"Test image loaded to memory. Shape: {test_image_np.shape if test_image_np is not None else 'None'}")
        
        if test_image_np is None:
            raise Exception("Test image could not be decoded. Invalid image format.")
        
        # Step 3: Verify seal using S3 URL for original image
        print(f"Starting verification with S3 URL: {original_s3_url}")
        result = verify_seal(original_s3_url, test_image_np)
        
        print(f"Verification result: {result}")
        
        # Return result with additional metadata
        return {
            **result,
            "message": "Seal verification completed successfully",
            "original_image": original_image.filename,
            "original_image_s3_url": original_s3_url,
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
