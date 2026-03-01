# src/challan.py
import os
from datetime import datetime
from config import CHALLAN_DIR
from db_access import get_owner_by_vehicle


def generate_challan(violation_id, vehicle_no, vtype, fine_amount, evidence_path, location):
    owner = get_owner_by_vehicle(vehicle_no)
    name, phone, email, address = owner if owner else ("Unknown", "-", "-", "-")

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fname = f"challan_{violation_id}_{vehicle_no}.txt"
    fpath = os.path.join(CHALLAN_DIR, fname)

    text = f"""E-CHALLAN
Violation ID : {violation_id}
Vehicle No   : {vehicle_no}
Owner        : {name}
Phone        : {phone}
Email        : {email}
Address      : {address}

Violation    : {vtype}
Fine Amount  : Rs {fine_amount}
Time         : {ts}
Location     : {location}
Evidence Img : {evidence_path}
Payment Link : https://pay.example.com/{violation_id}
"""

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(text)

    return fpath
