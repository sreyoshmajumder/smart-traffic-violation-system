# src/detection.py
# src/detection.py
import os
import time
from dataclasses import dataclass
import cv2
import numpy as np
import pandas as pd  # ← this was missing
import joblib
import pytesseract

from config import (
    MODELS_DIR,
    EVIDENCE_IMG_DIR,
    LOCATION_NAME,
    SPEED_LIMIT_KMPH,
)

# set Tesseract path after install
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

MODEL_PATH = os.path.join(MODELS_DIR, "violation_rf.pkl")
print(pytesseract.get_tesseract_version())
# rest of your code continues below...



@dataclass
class ViolationResult:
    vehicle_no: str
    violation_type: str
    reason: str
    speed_kmph: float
    timestamp: str
    location: str
    fine_amount: float
    evidence_filename: str


# try loading ML model (optional)
clf = None
feature_columns = None
if os.path.exists(MODEL_PATH):
    store = joblib.load(MODEL_PATH)
    if isinstance(store, dict) and "model" in store:
        clf = store["model"]
        feature_columns = store.get("feature_columns")


#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" # assumes in PATH


def simple_plate_crop(frame):
    h, w, _ = frame.shape
    x1, x2 = int(w * 0.3), int(w * 0.7)
    y1, y2 = int(h * 0.6), int(h * 0.9)
    return frame[y1:y2, x1:x2]


def read_plate(plate_img):
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(
        th,
        config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    )
    return "".join(ch for ch in text if ch.isalnum()).upper()


def analyze_video(video_path: str):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    frame_interval = int(max(1, fps // 2))  # sample ~2 frames per second

    any_violation = False
    evidence_frame = None
    approx_speed = 0.0

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1
        if frame_idx % frame_interval != 0:
            continue

        # fake feature extraction: use brightness and position as simple signals
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_intensity = float(gray.mean())
        height, width = gray.shape

        # fake speed estimate (just for demo) based on change in intensity
        approx_speed = 30.0 + (mean_intensity % 25)  # 30–55 km/h approx

        # fake red/green pattern using time
        t = frame_idx / fps
        signal_is_red = (int(t) % 10) < 5  # 5s red / 5s green

        violation_flag = False

        if clf is not None and feature_columns is not None:
            import pandas as pd

            features = {
                "junction_id": 1,
                "camera_id": 1,
                "speed_kmph": approx_speed,
                "speed_limit_kmph": SPEED_LIMIT_KMPH,
                "lane_count": 2,
                "is_peak_hour": 1,
                "vehicle_type_car": 1,
                "vehicle_type_truck": 0,
                "signal_state_green": 0,
                "signal_state_red": 1 if signal_is_red else 0,
            }
            X = pd.DataFrame([features])
            for col in feature_columns:
                if col not in X.columns:
                    X[col] = 0
            X = X[feature_columns]
            prob = clf.predict_proba(X)[:, 1]
            violation_flag = prob >= 0.5
        else:
            # simple rule fallback
            if signal_is_red and approx_speed > 5:
                violation_flag = True
            elif approx_speed > SPEED_LIMIT_KMPH + 5:
                violation_flag = True

        if violation_flag:
            any_violation = True
            evidence_frame = frame.copy()
            break

    cap.release()

    if not any_violation or evidence_frame is None:
        return []

    # ANPR on evidence frame
    plate_img = simple_plate_crop(evidence_frame)
    plate_no = read_plate(plate_img) or "WB01AB1234"

    # save evidence image
    ts_str = time.strftime("%Y%m%d_%H%M%S")
    img_name = f"evidence_{ts_str}_{plate_no}.jpg"
    img_path = os.path.join(EVIDENCE_IMG_DIR, img_name)
    cv2.imwrite(img_path, evidence_frame)

    # basic reason and fine
    reasons = []
    fine = 0
    if approx_speed > SPEED_LIMIT_KMPH + 5:
        reasons.append("Overspeeding")
        fine += 500
    if approx_speed <= SPEED_LIMIT_KMPH + 5:
        reasons.append("Red light violation (approx)")
        fine += 1000

    if not reasons:
        reasons.append("General traffic violation")
        fine = 300

    violation_type = " + ".join(reasons)

    result = ViolationResult(
        vehicle_no=plate_no,
        violation_type=violation_type,
        reason=", ".join(reasons),
        speed_kmph=float(f"{approx_speed:.1f}"),
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        location=LOCATION_NAME,
        fine_amount=float(fine),
        evidence_filename=img_name,
    )

    return [result]
