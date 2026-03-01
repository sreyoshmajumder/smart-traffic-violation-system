# src/db_access.py
import sqlite3
from datetime import datetime
from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS owners (
  owner_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT,
  phone      TEXT,
  email      TEXT,
  address    TEXT
);

CREATE TABLE IF NOT EXISTS vehicles (
  vehicle_no TEXT PRIMARY KEY,
  owner_id   INTEGER,
  model      TEXT,
  color      TEXT,
  FOREIGN KEY(owner_id) REFERENCES owners(owner_id)
);

CREATE TABLE IF NOT EXISTS violations (
  violation_id INTEGER PRIMARY KEY AUTOINCREMENT,
  vehicle_no   TEXT,
  type         TEXT,
  timestamp    TEXT,
  location     TEXT,
  speed_kmph   REAL,
  evidence_img TEXT,
  fine_amount  REAL,
  paid         INTEGER DEFAULT 0,
  FOREIGN KEY(vehicle_no) REFERENCES vehicles(vehicle_no)
);

CREATE TABLE IF NOT EXISTS payments (
  payment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  violation_id INTEGER,
  amount       REAL,
  timestamp    TEXT,
  method       TEXT,
  FOREIGN KEY(violation_id) REFERENCES violations(violation_id)
);
"""


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    conn.close()


def seed_demo_data():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO owners(owner_id, name, phone, email, address) "
        "VALUES (1, 'Demo User', '+91-9999999999', 'demo@example.com', 'Kolkata, WB')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO vehicles(vehicle_no, owner_id, model, color) "
        "VALUES ('WB01AB1234', 1, 'Sedan', 'White')"
    )
    conn.commit()
    conn.close()


def get_owner_by_vehicle(vehicle_no: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT o.name, o.phone, o.email, o.address FROM owners o "
        "JOIN vehicles v ON o.owner_id = v.owner_id WHERE v.vehicle_no = ?",
        (vehicle_no,),
    )
    row = cur.fetchone()
    conn.close()
    return row


def insert_violation(vehicle_no, vtype, location, speed_kmph, evidence_img, fine_amount):
    conn = get_conn()
    cur = conn.cursor()
    ts = datetime.now().isoformat(timespec="seconds")
    cur.execute(
        "INSERT INTO violations(vehicle_no, type, timestamp, location, speed_kmph, evidence_img, fine_amount) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (vehicle_no, vtype, ts, location, speed_kmph, evidence_img, fine_amount),
    )
    violation_id = cur.lastrowid
    conn.commit()
    conn.close()
    return violation_id
