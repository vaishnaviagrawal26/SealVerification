import cv2
import numpy as np


# ==========================================
# HELPER FUNCTION: DOWNLOAD IMAGE FROM S3 OR LOAD FROM LOCAL PATH
# ==========================================

def get_image_data(image_source):
    """
    Get image data from either an S3 URL or a local file path.
    
    Args:
        image_source: Either an S3 URL (http/https) or a local file path
        
    Returns:
        numpy array of the image
    """
    try:
        if isinstance(image_source, str) and (image_source.startswith("http://") or image_source.startswith("https://")):
            # Download from S3 URL (lazy import)
            import httpx
            print(f"Downloading image from S3: {image_source}")
            response = httpx.get(image_source)
            response.raise_for_status()
            img = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
            print(f"Image downloaded successfully. Shape: {img.shape if img is not None else 'None'}")
            return img
        else:
            # Load from local file path
            print(f"Loading image from local path: {image_source}")
            img = cv2.imread(image_source)
            return img
    except Exception as e:
        print(f"Error loading image from {image_source}: {e}")
        raise


# ==========================================
# VERIFY SEAL
# ==========================================

def verify_seal(original_source, test_image_np):

    try:
        # Load original image from S3 URL or local path
        img1 = get_image_data(original_source)
        img2 = test_image_np
        
        if img1 is None:
            raise Exception(f"Original image could not be read from: {original_source}")
        
        if img2 is None:
            raise Exception("Test image is None")
        
        # Ensure arrays are proper numpy arrays with correct dtype
        img1 = np.asarray(img1, dtype=np.uint8)
        img2 = np.asarray(img2, dtype=np.uint8)
        
        if img1.size == 0 or img2.size == 0:
            raise Exception("One or both images are empty")

        # ==========================================
        # RESIZE IMAGES
        # ==========================================

        size = (800, 600)

        img1 = cv2.resize(img1, size)
        img2 = cv2.resize(img2, size)

        # ==========================================
        # CONVERT TO GRAYSCALE
        # ==========================================

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # ==========================================
        # PREPROCESSING
        # ==========================================

        gray1 = cv2.GaussianBlur(gray1, (5, 5), 0)
        gray2 = cv2.GaussianBlur(gray2, (5, 5), 0)

        gray1 = cv2.equalizeHist(gray1)
        gray2 = cv2.equalizeHist(gray2)

        # ==========================================
        # ORB FEATURE DETECTION
        # ==========================================

        orb = cv2.ORB_create(5000)

        kp1, des1 = orb.detectAndCompute(gray1, None)
        kp2, des2 = orb.detectAndCompute(gray2, None)

        if des1 is None or des2 is None:
            return None

        # ==========================================
        # FEATURE MATCHING
        # ==========================================

        bf = cv2.BFMatcher(cv2.NORM_HAMMING)

        matches = bf.knnMatch(des1, des2, k=2)

        good_matches = []

        for m, n in matches:

            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        # ==========================================
        # RAW MATCH SCORE
        # ==========================================

        total_features = min(len(kp1), len(kp2))

        if total_features == 0:

            raw_score = 0

        else:

            raw_score = (
                len(good_matches) / total_features
            ) * 100

        raw_score = min(raw_score, 100)

        # ==========================================
        # HOMOGRAPHY VALIDATION
        # ==========================================

        if len(good_matches) > 10:

            src_pts = np.float32([
                kp1[m.queryIdx].pt
                for m in good_matches
            ]).reshape(-1, 1, 2)

            dst_pts = np.float32([
                kp2[m.trainIdx].pt
                for m in good_matches
            ]).reshape(-1, 1, 2)

            H, mask = cv2.findHomography(
                src_pts,
                dst_pts,
                cv2.RANSAC,
                5.0
            )

            if mask is not None:

                inliers = np.sum(mask)

                homography_score = (
                    inliers / len(good_matches)
                ) * 100

                raw_score = (
                    0.7 * raw_score
                    +
                    0.3 * homography_score
                )

        # ==========================================
        # NORMALIZED USER SCORE
        # ==========================================

        normalized_score = min(
            100,
            max(
                0,
                (raw_score / 45) * 100
            )
        )

        # ==========================================
        # DRAW MATCHES
        # ==========================================

        result = cv2.drawMatches(
            img1,
            kp1,
            img2,
            kp2,
            good_matches[:50],
            None,
            flags=2
        )

        # ==========================================
        # FINAL VERDICT
        # ==========================================

        if normalized_score > 70:
            verdict = "GENUINE SEAL"

        elif normalized_score > 50:
            verdict = "SUSPICIOUS SEAL"

        else:
            verdict = "TAMPERED SEAL"

        # ==========================================
        # SAVE OUTPUT IMAGE
        # ==========================================

        output_path = "output/result.jpg"

        cv2.imwrite(output_path, result)

        # ==========================================
        # RETURN RESULTS
        # ==========================================

        return {
            "match_percent": round(normalized_score, 2),
            "verdict": verdict,
            "output_image": output_path
        }

    except Exception as e:
        print(f"Verifier Error: {e}")
        import traceback
        traceback.print_exc()
        raise