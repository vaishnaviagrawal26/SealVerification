import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
from app.model.verifier import verify_seal
from PIL import Image
import os

st.set_page_config(
    page_title="Seal Verification System",
    layout="wide"
)

st.title("Seal Verification System")

st.write("Upload Original and Test Seal Images")

# Upload images
original_file = st.file_uploader(
    "Upload Original Seal",
    type=["jpg", "png", "jpeg"]
)

test_file = st.file_uploader(
    "Upload Test Seal",
    type=["jpg", "png", "jpeg"]
)

if st.button("Verify Seal"):

    if original_file and test_file:

        # Create folders
        os.makedirs("input", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        original_path = "input/original.jpg"
        test_path = "input/test.jpg"

        # Save uploaded files
        from PIL import Image

        # Save original image properly
        original_image = Image.open(original_file)
        original_image.save(original_path)

        # Save test image properly
        test_image = Image.open(test_file)
        test_image.save(test_path)

        # Verify
        result = verify_seal(
            original_path,
            test_path
        )

        if result:

            st.success("Verification Completed")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Match Percentage")
                st.metric(
                    "Similarity",
                    f"{result['match_percent']}%"
                )

            with col2:
                st.subheader("Final Verdict")
                st.write(result["verdict"])

            st.subheader("Detected Differences")

            output_img = Image.open(
                result["output_image"]
            )

            st.image(output_img)

        else:
            st.error("Error processing images")

    else:
        st.warning("Please upload both images")