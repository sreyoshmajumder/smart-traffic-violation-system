<!-- HEADER BANNER -->
<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=0:0a0000,40:1a0a00,70:1a1a00,100:0a0a0f&height=240&section=header&text=🚦%20Smart%20Traffic%20Violation%20System&fontSize=34&fontColor=ff2d78&fontAlignY=40&desc=Video%20Upload%20→%20ML%20Analysis%20→%20ANPR%20→%20Auto%20E-Challan%20Generation&descAlignY=62&descColor=ffd700&animation=fadeIn)

<br/>

[![Python](https://img.shields.io/badge/Python-3.8+-0a0a0f?style=for-the-badge&logo=python&logoColor=ffd700)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-0a0a0f?style=for-the-badge&logo=flask&logoColor=ffffff)](https://flask.palletsprojects.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-0a0a0f?style=for-the-badge&logo=opencv&logoColor=ff6347)](https://opencv.org)
[![Tesseract](https://img.shields.io/badge/Tesseract%20OCR-5.x-0a0a0f?style=for-the-badge&logo=google&logoColor=ff2d78)](https://github.com/tesseract-ocr)
[![SQLite](https://img.shields.io/badge/SQLite-3-0a0a0f?style=for-the-badge&logo=sqlite&logoColor=00f5ff)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-0a0a0f?style=for-the-badge&logoColor=ffd700)](LICENSE)

<br/>

> **🚨 An end-to-end AI-powered traffic law enforcement platform — upload CCTV junction footage, let ML detect violations, OCR extract number plates, query the owner database, and auto-generate digital E-Challans with fines and evidence snapshots. Zero manual effort.**

<br/>

![Violations](https://img.shields.io/badge/Detects-Red%20Light%20%7C%20Overspeeding-ff2d78?style=flat-square&labelColor=0a0a0f)
![ANPR](https://img.shields.io/badge/ANPR-Tesseract%20OCR-ffd700?style=flat-square&labelColor=0a0a0f)
![DB](https://img.shields.io/badge/Database-SQLite%20%7C%204%20Tables-00f5ff?style=flat-square&labelColor=0a0a0f)
![Stack](https://img.shields.io/badge/Stack-Flask%20%2B%20OpenCV%20%2B%20ML-39ff14?style=flat-square&labelColor=0a0a0f)

</div>

---

## 📋 Table of Contents

| | Section |
|---|---|
| 🎯 | [Problem Statement](#-problem-statement) |
| ✨ | [Key Features](#-key-features) |
| 🏗️ | [System Architecture](#-system-architecture) |
| 🔄 | [End-to-End Pipeline](#-end-to-end-pipeline) |
| 🎥 | [Detection Engine](#-detection-engine-detectionpy) |
| 🔢 | [ANPR — Number Plate OCR](#-anpr--number-plate-recognition) |
| 🗄️ | [Database Schema](#-database-schema-db_accesspy) |
| 📄 | [E-Challan Generator](#-e-challan-generator-challanpy) |
| 🌐 | [Web Application](#-web-application-web_apppy) |
| 🗂️ | [Project Structure](#-project-structure) |
| 🚀 | [Quick Start](#-quick-start) |
| 🔭 | [Roadmap](#-future-roadmap) |

---

## 🎯 Problem Statement

<div align="center">

```
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   India records 4,50,000+ road accidents every year.                     ║
║   A significant cause: red-light jumping & overspeeding at junctions.   ║
║                                                                          ║
║   Traditional enforcement is:                                            ║
║   ❌  Slow — manual review of CCTV footage                               ║
║   ❌  Costly — dedicated traffic police at every junction                ║
║   ❌  Inconsistent — human bias and fatigue                              ║
║   ❌  Delayed — challans issued days after violation                     ║
║                                                                          ║
║   ► Smart Traffic Violation System solves this end-to-end:               ║
║                                                                          ║
║   🎥 Upload CCTV footage                                                 ║
║       └──▶ 🤖 ML detects violations (red light / overspeed)             ║
║               └──▶ 🔢 OCR reads number plate                            ║
║                       └──▶ 🗄️  DB looks up owner details               ║
║                               └──▶ 📄 E-Challan auto-generated          ║
║                                       └──▶ 💳 Payment link attached     ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

</div>

---

## ✨ Key Features

| ⚡ Feature | 📋 Description |
|---|---|
| 🎥 **Video Upload** | Drag-and-drop junction camera footage via web interface |
| 🚦 **Red Light Detection** | ML model + rule-based fallback detects signal violations frame-by-frame |
| ⚡ **Overspeed Detection** | Speed estimation from frame analysis vs configurable speed limit |
| 🔢 **ANPR** | Tesseract OCR with Otsu thresholding extracts vehicle number plates |
| 🗄️ **SQLite Database** | 4-table relational schema: Owners, Vehicles, Violations, Payments |
| 📄 **E-Challan Generation** | Digital challans with owner name, phone, email, fine amount, payment link |
| 📸 **Evidence Storage** | Timestamped violation frame snapshots saved as JPEG proof |
| 🌐 **Flask Web App** | Full-stack web interface: upload → analyze → view results |
| ⚙️ **Config-Driven** | All paths, speed limits, and locations managed in `config.py` |

---

## 🏗️ System Architecture

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║               SMART TRAFFIC VIOLATION SYSTEM — FULL ARCHITECTURE             ║
╚═══════════════════════════════════════════════════════════════════════════════╝

                        ┌─────────────────────────┐
                        │      BROWSER / USER      │
                        │  index.html + styles.css │
                        │  (drag & drop uploader)  │
                        └────────────┬────────────┘
                                     │  HTTP POST /upload (multipart video)
                                     ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                          FLASK WEB SERVER (web_app.py)                     │
│                                                                            │
│   Route: POST /upload                                                      │
│   ├── Save video to /uploads/                                              │
│   ├── Call detection.analyze_video(path)   ──────────────────────────┐    │
│   ├── For each ViolationResult:                                        │    │
│   │     ├── db_access.insert_violation(...)                           │    │
│   │     └── challan.generate_challan(...)                             │    │
│   └── Render result.html with violations list                         │    │
└───────────────────────────────────────────────────────────────────────┼────┘
                                                                        │
                        ┌───────────────────────────────────────────────┘
                        ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                        DETECTION ENGINE (detection.py)                    │
│                                                                           │
│  1. cv2.VideoCapture(path)   ──▶  Open video file                        │
│  2. Sample frames @ fps//2   ──▶  ~2 frames per second                   │
│  3. Per frame:                                                            │
│     ├── Gray + mean_intensity  ──▶  brightness feature                   │
│     ├── approx_speed = 30 + (intensity % 25)  ──▶  30–55 km/h           │
│     ├── signal_is_red = (int(t) % 10) < 5    ──▶  5s red / 5s green     │
│     │                                                                     │
│     ├── IF ML model loaded (violation_rf.pkl):                            │
│     │     Build feature DataFrame → clf.predict_proba()                  │
│     │     violation if prob >= 0.5                                        │
│     │                                                                     │
│     └── ELSE rule-based fallback:                                         │
│           red signal + speed > 5    ──▶  RED LIGHT violation             │
│           speed > SPEED_LIMIT + 5   ──▶  OVERSPEEDING violation          │
│                                                                           │
│  4. On first violation frame:                                             │
│     ├── Crop plate region (30–70% W, 60–90% H)                          │
│     ├── Tesseract OCR  ──▶  vehicle_no                                   │
│     ├── cv2.imwrite()  ──▶  evidence_YYYYMMDD_HHMMSS_PLATE.jpg          │
│     └── Return [ViolationResult dataclass]                                │
└───────────────────────────────────────────────────────────────────────────┘
              │                                    │
              ▼                                    ▼
┌─────────────────────────┐          ┌─────────────────────────────────────┐
│   DATABASE (traffic.db) │          │     CHALLAN GENERATOR (challan.py)  │
│   db_access.py          │          │                                     │
│                         │          │  get_owner_by_vehicle(plate_no)     │
│  ┌───────────────────┐  │          │  ──▶ owner name, phone, email       │
│  │     owners        │  │          │                                     │
│  │  (id,name,phone,  │◀─┤──────────│  Write challan_VID_PLATE.txt with:  │
│  │   email,address)  │  │          │  • Violation ID                     │
│  └────────┬──────────┘  │          │  • Vehicle No                       │
│           │              │          │  • Owner details                    │
│  ┌────────▼──────────┐  │          │  • Violation type + reason          │
│  │     vehicles      │  │          │  • Fine amount (Rs)                 │
│  │  (vehicle_no PK,  │  │          │  • Timestamp + Location             │
│  │   owner_id FK,    │  │          │  • Evidence image path              │
│  │   model, color)   │  │          │  • Payment link URL                 │
│  └────────┬──────────┘  │          └─────────────────────────────────────┘
│           │              │
│  ┌────────▼──────────┐  │
│  │    violations     │  │
│  │  (id, vehicle_no, │  │
│  │   type, timestamp,│  │
│  │   location,       │  │
│  │   speed_kmph,     │  │
│  │   evidence_img,   │  │
│  │   fine_amount,    │  │
│  │   paid=0)         │  │
│  └────────┬──────────┘  │
│           │              │
│  ┌────────▼──────────┐  │
│  │     payments      │  │
│  │  (id,violation_id,│  │
│  │   amount,timestamp│  │
│  │   method)         │  │
│  └───────────────────┘  │
└─────────────────────────┘
```

---

## 🔄 End-to-End Pipeline

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    COMPLETE END-TO-END PROCESSING PIPELINE                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  STEP 1 ── VIDEO INGESTION                                                    ║
║  ────────────────────────────────────────────────────────────────────────    ║
║  Browser   ──▶  POST /upload  ──▶  Flask saves to /uploads/<filename>       ║
║  Formats accepted: .mp4 · .avi · .mov · .mkv                                ║
║                                                                               ║
║  STEP 2 ── FRAME SAMPLING                                                     ║
║  ────────────────────────────────────────────────────────────────────────    ║
║  fps = cap.get(CAP_PROP_FPS)  →  default 25                                 ║
║  frame_interval = int(max(1, fps // 2))  →  every ~0.5 seconds              ║
║  Purpose: balance speed vs coverage (skip redundant frames)                  ║
║                                                                               ║
║  STEP 3 ── FEATURE EXTRACTION (per sampled frame)                             ║
║  ────────────────────────────────────────────────────────────────────────    ║
║  gray = cv2.cvtColor(frame, COLOR_BGR2GRAY)                                  ║
║  mean_intensity = float(gray.mean())           ──▶  brightness signal       ║
║  approx_speed   = 30.0 + (mean_intensity % 25) ──▶  estimated 30–55 km/h   ║
║  signal_is_red  = (int(frame_idx/fps) % 10) < 5 ──▶  5s red / 5s green    ║
║                                                                               ║
║  STEP 4 ── VIOLATION CLASSIFICATION                                           ║
║  ────────────────────────────────────────────────────────────────────────    ║
║                                                                               ║
║  ┌─────────────────────────────────┐    ┌──────────────────────────────┐    ║
║  │  ML MODEL PATH (if available)   │    │  RULE-BASED FALLBACK         │    ║
║  │  models/violation_rf.pkl        │    │                              │    ║
║  │                                 │    │  IF signal_is_red            │    ║
║  │  features = {                   │    │    AND speed > 5 km/h        │    ║
║  │    junction_id, camera_id,      │    │  → RED LIGHT VIOLATION       │    ║
║  │    speed_kmph, speed_limit,     │    │                              │    ║
║  │    lane_count, is_peak_hour,    │    │  IF speed >                  │    ║
║  │    vehicle_type_car/truck,      │    │     SPEED_LIMIT + 5          │    ║
║  │    signal_state_red/green       │    │  → OVERSPEEDING VIOLATION    │    ║
║  │  }                              │    └──────────────────────────────┘    ║
║  │  prob = clf.predict_proba(X)    │                                        ║
║  │  flag = prob >= 0.5             │                                        ║
║  └─────────────────────────────────┘                                        ║
║                                                                               ║
║  STEP 5 ── ANPR (Automatic Number Plate Recognition)                          ║
║  ────────────────────────────────────────────────────────────────────────    ║
║  plate_img = frame[60%H:90%H, 30%W:70%W]   ──▶  crop plate region          ║
║  gray      = cv2.cvtColor(plate_img, BGR2GRAY)                               ║
║  gray      = cv2.GaussianBlur(gray, (3,3), 0)                               ║
║  _, th     = cv2.threshold(THRESH_BINARY + THRESH_OTSU)  ──▶  binarize      ║
║  text      = pytesseract.image_to_string(th, psm=7,                         ║
║                whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789)               ║
║  plate_no  = "".join(alnum chars).upper()                                    ║
║                                                                               ║
║  STEP 6 ── EVIDENCE CAPTURE                                                   ║
║  ────────────────────────────────────────────────────────────────────────    ║
║  img_name = f"evidence_{timestamp}_{plate_no}.jpg"                           ║
║  cv2.imwrite(EVIDENCE_IMG_DIR / img_name, violation_frame)                   ║
║                                                                               ║
║  STEP 7 ── FINE CALCULATION                                                   ║
║  ────────────────────────────────────────────────────────────────────────    ║
║  Overspeeding detected         ──▶  Fine += Rs 500                          ║
║  Red light violation detected  ──▶  Fine += Rs 1000                         ║
║  General violation (fallback)  ──▶  Fine  = Rs 300                          ║
║  Combined violations           ──▶  Fines accumulate                        ║
║                                                                               ║
║  STEP 8 ── DB INSERT + E-CHALLAN                                              ║
║  ────────────────────────────────────────────────────────────────────────    ║
║  db_access.insert_violation(vehicle_no, type, location,                      ║
║                             speed_kmph, evidence_img, fine)                  ║
║  challan.generate_challan(violation_id, vehicle_no, ...)                     ║
║  ──▶  challan_{violation_id}_{plate_no}.txt saved to /challans/              ║
║                                                                               ║
║  STEP 9 ── RESULTS RENDERED                                                   ║
║  ────────────────────────────────────────────────────────────────────────    ║
║  Flask renders result.html with:                                             ║
║  • Violation table (type, plate, speed, fine)                                ║
║  • Evidence image thumbnail                                                  ║
║  • Download challan link                                                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 🎥 Detection Engine (`detection.py`)

### ViolationResult Dataclass

```python
@dataclass
class ViolationResult:
    vehicle_no:        str    # OCR-extracted plate number
    violation_type:    str    # "Red light violation" | "Overspeeding" | combined
    reason:            str    # Human-readable reason string
    speed_kmph:        float  # Estimated speed at violation frame
    timestamp:         str    # "YYYY-MM-DD HH:MM:SS"
    location:          str    # From config.LOCATION_NAME
    fine_amount:       float  # Rs 300 / 500 / 1000 / combined
    evidence_filename: str    # "evidence_YYYYMMDD_HHMMSS_PLATE.jpg"
```

### Signal State Machine

```
  TRAFFIC SIGNAL SIMULATION (time-based cycling)
  ──────────────────────────────────────────────────────────────────
  t = frame_index / fps   (seconds into video)

  t=0s      t=5s      t=10s     t=15s     t=20s
  │──RED──── │ ──GREEN─│ ──RED── │ ──GREEN─│
  │  0–5s   │   5–10s │  10–15s │  15–20s │
  │ RED🔴   │  GREEN🟢 │  RED 🔴 │ GREEN🟢 │

  signal_is_red = (int(t) % 10) < 5
  Violation triggered when: signal_is_red == True AND speed > 5 km/h
```

### ML Model Feature Vector

```
  Features fed to violation_rf.pkl (Random Forest Classifier):
  ──────────────────────────────────────────────────────────────
  junction_id          → int   (junction identifier)
  camera_id            → int   (camera identifier)
  speed_kmph           → float (estimated vehicle speed)
  speed_limit_kmph     → float (from config.SPEED_LIMIT_KMPH)
  lane_count           → int   (lanes at junction)
  is_peak_hour         → 0/1   (peak traffic hours flag)
  vehicle_type_car     → 0/1   (one-hot: car)
  vehicle_type_truck   → 0/1   (one-hot: truck)
  signal_state_green   → 0/1   (one-hot: green signal)
  signal_state_red     → 0/1   (one-hot: red signal)

  Output: predict_proba()[:, 1]  →  violation if prob >= 0.5
```

---

## 🔢 ANPR — Number Plate Recognition

```
  ANPR PIPELINE
  ──────────────────────────────────────────────────────────────────

  FULL FRAME (H × W × 3)
       │
       ▼  Crop to likely plate region
  PLATE REGION  =  frame[0.6H : 0.9H,  0.3W : 0.7W]
       │
       ▼  cv2.cvtColor(BGR → GRAY)
  GRAYSCALE IMAGE
       │
       ▼  cv2.GaussianBlur(kernel=(3,3), sigma=0)
  BLURRED IMAGE  (noise reduction)
       │
       ▼  cv2.threshold(THRESH_BINARY + THRESH_OTSU)
  BINARY IMAGE   (adaptive threshold — handles lighting variance)
       │
       ▼  pytesseract.image_to_string(psm=7)
       │    --psm 7  =  single line of text
       │    whitelist = A-Z 0-9 only
  RAW OCR TEXT
       │
       ▼  filter alphanumeric + .upper()
  VEHICLE NUMBER  →  e.g. "WB01AB1234"

  ──────────────────────────────────────────────────────────────────
  Tesseract Config:
  Path: C:\Program Files\Tesseract-OCR\tesseract.exe  (Windows)
  PSM:  7  (single text line)
  OEM:  Default LSTM engine
  ──────────────────────────────────────────────────────────────────
```

---

## 🗄️ Database Schema (`db_access.py`)

### Entity-Relationship Diagram

```
  ┌──────────────────────────┐         ┌──────────────────────────────────┐
  │         OWNERS           │         │            VEHICLES              │
  ├──────────────────────────┤         ├──────────────────────────────────┤
  │ owner_id  INTEGER PK AI  │◀───1:N──│ vehicle_no  TEXT  PK             │
  │ name      TEXT           │         │ owner_id    INTEGER  FK→owners   │
  │ phone     TEXT           │         │ model       TEXT                 │
  │ email     TEXT           │         │ color       TEXT                 │
  │ address   TEXT           │         └──────────────┬───────────────────┘
  └──────────────────────────┘                        │
                                                      │ 1:N
                                                      ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                          VIOLATIONS                              │
  ├──────────────────────────────────────────────────────────────────┤
  │ violation_id  INTEGER  PK AUTOINCREMENT                          │
  │ vehicle_no    TEXT     FK → vehicles.vehicle_no                  │
  │ type          TEXT     ("Red light violation" / "Overspeeding")  │
  │ timestamp     TEXT     ("YYYY-MM-DDTHH:MM:SS")                  │
  │ location      TEXT     (from config.LOCATION_NAME)              │
  │ speed_kmph    REAL     (estimated km/h at violation)            │
  │ evidence_img  TEXT     (filename of saved JPEG snapshot)        │
  │ fine_amount   REAL     (Rs 300 / 500 / 1000)                    │
  │ paid          INTEGER  DEFAULT 0  (0=unpaid, 1=paid)            │
  └──────────────────────────────┬───────────────────────────────────┘
                                 │ 1:N
                                 ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                           PAYMENTS                               │
  ├──────────────────────────────────────────────────────────────────┤
  │ payment_id    INTEGER  PK AUTOINCREMENT                          │
  │ violation_id  INTEGER  FK → violations.violation_id              │
  │ amount        REAL     (amount paid)                             │
  │ timestamp     TEXT     (payment datetime)                        │
  │ method        TEXT     (UPI / card / netbanking)                 │
  └──────────────────────────────────────────────────────────────────┘
```

### Key DB Functions

```python
init_db()                          # Create all 4 tables from SCHEMA
seed_demo_data()                   # Insert demo owner WB01AB1234
get_owner_by_vehicle(vehicle_no)   # JOIN owners + vehicles → (name, phone, email, address)
insert_violation(vehicle_no,       # INSERT INTO violations, return violation_id
                 vtype, location,
                 speed_kmph,
                 evidence_img,
                 fine_amount)
```

---

## 📄 E-Challan Generator (`challan.py`)

### Real Challan Format (from source code)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          E-CHALLAN                                  │
│─────────────────────────────────────────────────────────────────────│
│  Violation ID  :  42                                                │
│  Vehicle No    :  WB01AB1234                                        │
│  Owner         :  Demo User                                         │
│  Phone         :  +91-9999999999                                    │
│  Email         :  demo@example.com                                  │
│  Address       :  Kolkata, WB                                       │
│  Violation     :  Red light violation (approx)                      │
│  Fine Amount   :  Rs 1000                                           │
│  Time          :  2025-03-15 14:32:10                               │
│  Location      :  Junction 5, MG Road, Kolkata                     │
│  Evidence Img  :  evidence_20250315_143210_WB01AB1234.jpg           │
│  Payment Link  :  https://pay.example.com/42                        │
└─────────────────────────────────────────────────────────────────────┘

Saved as: challans/challan_42_WB01AB1234.txt
```

### Challan Generation Flow

```
  generate_challan(violation_id, vehicle_no, vtype, fine_amount,
                   evidence_path, location)
         │
         ├──▶  get_owner_by_vehicle(vehicle_no)
         │     └──▶  JOIN owners + vehicles in SQLite
         │           Returns: (name, phone, email, address)
         │
         ├──▶  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         │
         ├──▶  fname = f"challan_{violation_id}_{vehicle_no}.txt"
         │     fpath = CHALLAN_DIR / fname
         │
         └──▶  Write formatted text file with all fields
               Return: fpath (for web download link)
```

---

## 🌐 Web Application (`web_app.py`)

```
  FLASK ROUTES
  ──────────────────────────────────────────────────────────────────

  GET  /                       ──▶  Serve index.html (upload form)
  POST /upload                 ──▶  Process video:
                                    1. Save to /uploads/
                                    2. init_db() + seed_demo_data()
                                    3. analyze_video(path)
                                    4. insert_violation() per result
                                    5. generate_challan() per result
                                    6. Return result.html
  GET  /evidence/<filename>    ──▶  Serve evidence JPEG snapshots
  GET  /challans/<filename>    ──▶  Serve .txt challan for download

  FRONTEND PAGES
  ──────────────────────────────────────────────────────────────────

  index.html   → Upload interface (drag-and-drop video)
  result.html  → Violations table + evidence + challan download
  styles.css   → Shared styling for both pages
```

---

## 📁 Fine Structure & Rules

```
  VIOLATION FINE MATRIX
  ──────────────────────────────────────────────────────────────────

  Violation Type              Fine Amount    Legal Reference
  ─────────────────────────────────────────────────────────────────
  🔴 Red Light Jumping         Rs 1,000      MV Act Section 119
  ⚡ Overspeeding              Rs   500      MV Act Section 112
  🔴⚡ Red Light + Overspeed   Rs 1,500      Both fines combined
  ⚠️  General Violation        Rs   300      Fallback rule

  Speed Limit: Configurable in config.py (SPEED_LIMIT_KMPH)
  Trigger:     speed > SPEED_LIMIT_KMPH + 5 km/h buffer
```

---

## 🗂️ Project Structure

```
smart-traffic-violation-system/
│
├── 🌐 index.html              # Upload interface — drag & drop video
├── 🌐 result.html             # Results page — violations + challans
├── 🎨 styles.css              # Shared CSS styling
│
├── 🐍 web_app.py              # Flask routes: /upload, /evidence, /challans
├── 🐍 detection.py            # Core CV+ML engine — 182 lines
│   ├── analyze_video()        # Main pipeline function
│   ├── simple_plate_crop()    # ANPR region extraction
│   └── read_plate()           # Tesseract OCR wrapper
│
├── 🐍 db_access.py            # SQLite ORM — 99 lines
│   ├── SCHEMA                 # 4-table DDL (owners/vehicles/violations/payments)
│   ├── init_db()              # Create tables
│   ├── seed_demo_data()       # Insert demo vehicle WB01AB1234
│   ├── get_owner_by_vehicle() # JOIN query → owner details
│   └── insert_violation()     # INSERT + return violation_id
│
├── 🐍 challan.py              # E-Challan generator — 35 lines
│   └── generate_challan()     # Write .txt challan file
│
├── 🐍 config.py               # All constants: paths, speed limit, location
│
├── 🗄️  traffic.db             # SQLite database file
│
├── 📁 uploads/                # User-uploaded video files
├── 📁 evidence/               # Violation screenshot JPEGs
├── 📁 challans/               # Generated .txt E-Challan files
└── 📁 models/                 # violation_rf.pkl (optional ML model)
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/sreyoshmajumder/smart-traffic-violation-system.git
cd smart-traffic-violation-system

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate

pip install flask opencv-python pytesseract numpy pandas joblib
```

### 2. Install Tesseract OCR

```bash
# Windows — download installer:
# https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.4.1.20240618.exe
# Install → ensure it's in PATH

# Ubuntu / Debian
sudo apt install tesseract-ocr

# macOS
brew install tesseract
```

### 3. Configure

```python
# config.py — update these values:
SPEED_LIMIT_KMPH = 40           # Your junction's speed limit
LOCATION_NAME    = "Junction 5, MG Road, Kolkata"
DB_PATH          = "traffic.db"
MODELS_DIR       = "models/"
EVIDENCE_IMG_DIR = "evidence/"
CHALLAN_DIR      = "challans/"
```

### 4. (Optional) Add ML Model

```bash
# Place your trained Random Forest model at:
models/violation_rf.pkl

# Expected format (joblib dict):
# {"model": sklearn_clf, "feature_columns": [...]}
# Without model, rule-based fallback is used automatically.
```

### 5. Run

```bash
python web_app.py
# Open: http://localhost:5000
```

### 6. Usage Flow

```
1.  Open  http://localhost:5000
2.  Upload junction CCTV video (mp4/avi/mov)
3.  Wait for ML analysis (seconds to minutes)
4.  View violations table on result page
5.  Download E-Challan .txt files per violator
6.  Evidence JPEGs saved in /evidence/ folder
```

---

## 🔭 Future Roadmap

```
v1.0 ── CURRENT ───────────────────────────────────────────────────────
  ✅  Video upload + Flask web interface
  ✅  OpenCV frame sampling + feature extraction
  ✅  Rule-based + ML (Random Forest) violation detection
  ✅  Tesseract OCR ANPR with Otsu binarization
  ✅  4-table SQLite schema (owners/vehicles/violations/payments)
  ✅  Auto E-Challan generation with owner details + payment link
  ✅  Evidence JPEG snapshot storage

v2.0 ── DETECTION UPGRADE ─────────────────────────────────────────────
  🔲  YOLOv8 real-time vehicle detection (replace brightness heuristic)
  🔲  Deep ANPR model (LPRNet / OpenALPR) replacing simple crop + OCR
  🔲  True speed estimation using optical flow (Lucas-Kanade)
  🔲  Helmet detection for two-wheelers
  🔲  Wrong-way driving detection

v3.0 ── SCALE & INTEGRATION ───────────────────────────────────────────
  🔲  RTSP live camera stream support (real-time processing)
  🔲  PostgreSQL migration from SQLite
  🔲  REST API endpoints for external system integration
  🔲  E-Challan delivery via SMS (Twilio) + Email (SMTP)
  🔲  Payment gateway integration (Razorpay / PayU)
  🔲  Admin dashboard with violation analytics & heatmaps

v4.0 ── SMART CITY ─────────────────────────────────────────────────────
  🔲  Multi-junction deployment with centralized dashboard
  🔲  VAHAN database API integration for real owner lookup
  🔲  Court case auto-escalation for repeat offenders
  🔲  AI traffic flow optimization at junctions
```

---

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-0a0a0f?style=for-the-badge&logo=python&logoColor=ffd700)
![Flask](https://img.shields.io/badge/Flask-0a0a0f?style=for-the-badge&logo=flask&logoColor=ffffff)
![OpenCV](https://img.shields.io/badge/OpenCV-0a0a0f?style=for-the-badge&logo=opencv&logoColor=ff6347)
![Tesseract](https://img.shields.io/badge/Tesseract%20OCR-0a0a0f?style=for-the-badge&logo=google&logoColor=ff2d78)
![SQLite](https://img.shields.io/badge/SQLite-0a0a0f?style=for-the-badge&logo=sqlite&logoColor=00f5ff)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-0a0a0f?style=for-the-badge&logo=scikitlearn&logoColor=f7931e)
![NumPy](https://img.shields.io/badge/NumPy-0a0a0f?style=for-the-badge&logo=numpy&logoColor=013243)
![Pandas](https://img.shields.io/badge/Pandas-0a0a0f?style=for-the-badge&logo=pandas&logoColor=150458)
![HTML5](https://img.shields.io/badge/HTML5-0a0a0f?style=for-the-badge&logo=html5&logoColor=ff6347)
![CSS3](https://img.shields.io/badge/CSS3-0a0a0f?style=for-the-badge&logo=css3&logoColor=264de4)

</div>

---

## 👨‍💻 Author

<div align="center">

**Built with 🚦 + 🤖 + ❤️ by [Sreyosh Majumder](https://github.com/sreyoshmajumder)**

[![GitHub](https://img.shields.io/badge/GitHub-sreyoshmajumder-0a0a0f?style=for-the-badge&logo=github&logoColor=ff2d78)](https://github.com/sreyoshmajumder)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0a0a0f?style=for-the-badge&logo=linkedin&logoColor=0077b5)](https://linkedin.com/in/YOUR_LINKEDIN)

> *"Every junction with a camera is a junction that can enforce itself."*

</div>

---

## ⭐ Show Some Love

```
★  Star this repository
🍴  Fork it and extend with YOLOv8 or live RTSP feeds
🐛  Open an issue for bugs or feature suggestions
📢  Share with traffic engineers and civic tech enthusiasts
```

---

<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:1a0a00,50:1a1a00,100:0a0000&height=120&section=footer&text=Safer%20Roads.%20Smarter%20Enforcement.%20Zero%20Manual%20Effort.&fontSize=14&fontColor=ffd700&fontAlignY=65)

</div>
