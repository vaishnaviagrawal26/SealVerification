Seal Verification System

A computer vision–based project for verifying security seals and detecting tampering using image processing and feature-matching techniques.

The system compares an original seal image with a test image and generates a verification score based on visual similarity.

Features

- Seal image verification
- ORB feature matching
- Lighting normalization
- Angle-tolerant comparison
- Match percentage generation
- Tamper detection
- Streamlit-based UI

Tech Stack

- Python
- OpenCV
- NumPy
- Streamlit

Run the Project

git clone https://github.com/vaishnaviagrawal26/SealVerification.git

cd SealVerification

pip install -r requirements.txt

streamlit run app.py

Future Improvements

- Signature verification
- Hole detection
- PDF report generation
- AI-based seal verification