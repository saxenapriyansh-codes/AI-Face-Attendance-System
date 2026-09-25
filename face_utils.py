import cv2
import os
import numpy as np


# ==========================================
# Project Paths
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

YUNET_MODEL = os.path.join(
    BASE_DIR,
    "face_detection_yunet_2023mar.onnx"
)

SFACE_MODEL = os.path.join(
    BASE_DIR,
    "face_recognition_sface_2021dec.onnx"
)


# ==========================================
# Load YuNet Face Detector
# ==========================================

face_detector = cv2.FaceDetectorYN_create(
    YUNET_MODEL,
    "",
    (320, 320),
    0.9,
    0.3,
    5000
)


# ==========================================
# Load SFace Recognizer
# ==========================================

face_recognizer = cv2.FaceRecognizerSF_create(
    SFACE_MODEL,
    ""
)


# ==========================================
# Detect Face
# ==========================================

def detect_face(image):

    height, width = image.shape[:2]

    face_detector.setInputSize(
        (width, height)
    )

    _, faces = face_detector.detect(image)

    if faces is None or len(faces) == 0:
        return False, None

    return True, faces


# ==========================================
# Get Best Face
# ==========================================

def get_best_face(image):

    found, faces = detect_face(image)

    if not found:
        return None

    # Face format:
    # x, y, width, height,
    # left_eye_x, left_eye_y,
    # right_eye_x, right_eye_y,
    # nose_x, nose_y,
    # mouth_left_x, mouth_left_y,
    # mouth_right_x, mouth_right_y,
    # confidence

    best_face = max(
        faces,
        key=lambda face: face[14]
    )

    return best_face


# ==========================================
# Create SFace Embedding
# ==========================================

def get_face_embedding(image):

    face = get_best_face(image)

    if face is None:
        return None

    # Align face
    aligned_face = face_recognizer.alignCrop(
        image,
        face
    )

    # Generate face feature / embedding
    feature = face_recognizer.feature(
        aligned_face
    )

    return feature.astype(
        np.float32
    )


# ==========================================
# Convert Embedding → Database Bytes
# ==========================================

def embedding_to_bytes(embedding):

    if embedding is None:
        return None

    return embedding.astype(
        np.float32
    ).tobytes()


# ==========================================
# Convert Database Bytes → Embedding
# ==========================================

def bytes_to_embedding(face_data):

    if face_data is None:
        return None

    try:

        array = np.frombuffer(
            face_data,
            dtype=np.float32
        )

        # SFace embedding should contain
        # 128 floating-point values.
        if array.size != 128:
            return None

        return array.reshape(
            1,
            128
        )

    except Exception:

        return None


# ==========================================
# Compare Two Faces
# ==========================================

def compare_faces(
    embedding1,
    embedding2
):

    if embedding1 is None:
        return 0.0

    if embedding2 is None:
        return 0.0

    similarity = face_recognizer.match(
        embedding1,
        embedding2,
        cv2.FaceRecognizerSF_FR_COSINE
    )

    return float(similarity)