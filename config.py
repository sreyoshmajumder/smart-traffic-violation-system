# src/config.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODELS_DIR = os.path.join(BASE_DIR, "models")
UPLOAD_VIDEO_DIR = os.path.join(BASE_DIR, "uploads", "videos")
EVIDENCE_IMG_DIR = os.path.join(BASE_DIR, "evidence", "images")
CHALLAN_DIR = os.path.join(BASE_DIR, "evidence", "challans")
DB_DIR = os.path.join(BASE_DIR, "data", "db")
DB_PATH = os.path.join(DB_DIR, "traffic.db")

# Simple detection constants (you can tune later)
LOCATION_NAME = "Kolkata Junction 1"
SPEED_LIMIT_KMPH = 50.0

# ensure folders exist
for d in [UPLOAD_VIDEO_DIR, EVIDENCE_IMG_DIR, CHALLAN_DIR, DB_DIR, MODELS_DIR]:
    os.makedirs(d, exist_ok=True)
