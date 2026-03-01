# 🚦 Smart Traffic Violation System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-green.svg)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-orange.svg)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Upload junction camera video → AI detects traffic violations → Auto-generate E-Challans with vehicle number, violation type, fine amount & evidence photos**

## ✨ Features

- 🎥 **Video Upload** - Drag & drop junction camera footage
- 🚦 **Red Light Detection** - ML model analyzes signal violations
- ⚡ **Overspeed Detection** - Speed estimation from video frames  
- 🔢 **ANPR (Number Plate Recognition)** - Tesseract OCR extracts vehicle numbers
- 💾 **SQLite Database** - Owners, Vehicles, Violations, Payments tracking
- 📄 **E-Challan Generation** - Digital challans with owner details & payment links
- 📊 **Evidence Storage** - Violation snapshots with timestamps

## 🏗️ Project Structure

smart-traffic-violation-system/
├── static/ # CSS styling
├── templates/ # HTML pages (upload, results)
├── src/ # Backend logic
│ ├── config.py # Paths & constants
│ ├── detection.py # Video → violation pipeline
│ ├── db_access.py # SQLite ORM
│ ├── challan.py # E-challan generator
│ └── web_app.py # Flask app
├── uploads/ # User videos
├── evidence/ # Screenshots + challans
├── models/ # ML model (optional)
└── requirements.txt


## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/YOUR_USERNAME/smart-traffic-violation-system.git
cd smart-traffic-violation-system

## 2. Environment

bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac  
source .venv/bin/activate

pip install -r requirements.txt

3. Tesseract OCR (Windows)

    Download: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.4.1.20240618.exe

    Install → Add to PATH

    Update path in src/detection.py
4. Run

bash
python src/web_app.py
