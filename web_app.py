# src/web_app.py
import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    flash,
)
from db_access import init_db, seed_demo_data, insert_violation
from config import UPLOAD_VIDEO_DIR, EVIDENCE_IMG_DIR
from detection import analyze_video
from challan import generate_challan

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = "super-secret"  # change in real use


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_video():
    file = request.files.get("video")
    if not file or file.filename == "":
        flash("Please select a video file.")
        return redirect(url_for("index"))

    filename = file.filename
    save_path = os.path.join(UPLOAD_VIDEO_DIR, filename)
    file.save(save_path)

    try:
        violations = analyze_video(save_path)
    except Exception as e:
        flash(f"Error analyzing video: {e}")
        return redirect(url_for("index"))

    challans = []
    for v in violations:
        violation_id = insert_violation(
            vehicle_no=v.vehicle_no,
            vtype=v.violation_type,
            location=v.location,
            speed_kmph=v.speed_kmph,
            evidence_img=v.evidence_filename,
            fine_amount=v.fine_amount,
        )
        challan_path = generate_challan(
            violation_id=violation_id,
            vehicle_no=v.vehicle_no,
            vtype=v.violation_type,
            fine_amount=v.fine_amount,
            evidence_path=v.evidence_filename,
            location=v.location,
        )
        challans.append({
            "violation_id": violation_id,
            "vehicle_no": v.vehicle_no,
            "violation_type": v.violation_type,
            "reason": v.reason,
            "speed_kmph": v.speed_kmph,
            "timestamp": v.timestamp,
            "location": v.location,
            "fine_amount": v.fine_amount,
            "evidence_url": url_for("get_evidence", filename=v.evidence_filename),
            "challan_file": os.path.basename(challan_path),
        })

    return render_template("result.html", challans=challans, filename=filename)


@app.route("/evidence/<path:filename>")
def get_evidence(filename):
    return send_from_directory(EVIDENCE_IMG_DIR, filename)


if __name__ == "__main__":
    init_db()
    seed_demo_data()
    app.run(debug=True)
