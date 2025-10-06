from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os, sqlite3, json

DB_PATH = os.getenv("DB_PATH", "/app/data/orders.db")
CONFIG_PATH = os.getenv("CONFIG_PATH", "/app/config.json")

app = FastAPI(title="MWL Admin API")

class Order(BaseModel):
    accession: str
    patient_id: str
    patient_name: str
    modality: str
    scheduled_dt: str
    site: str
    department: str
    ae: str
    status: str = "SCHEDULED"

def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
      accession TEXT PRIMARY KEY,
      patient_id TEXT, patient_name TEXT, modality TEXT,
      scheduled_dt TEXT, site TEXT, department TEXT, ae TEXT,
      status TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit(); conn.close()

@app.on_event("startup")
def init_db():
    _ensure_db()

@app.get("/orders")
def list_orders(q: Optional[str] = None):
    _ensure_db()
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    if q:
        c.execute("SELECT * FROM orders WHERE accession LIKE ? OR patient_id LIKE ? OR patient_name LIKE ?",
                  (f"%{q}%", f"%{q}%", f"%{q}%"))
    else:
        c.execute("SELECT * FROM orders ORDER BY created_at DESC")
    rows = c.fetchall(); conn.close()
    keys = ["accession","patient_id","patient_name","modality","scheduled_dt","site","department","ae","status","created_at"]
    return [dict(zip(keys,r)) for r in rows]

@app.post("/orders", status_code=201)
def create_order(o: Order):
    _ensure_db()
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    try:
        c.execute("INSERT INTO orders(accession,patient_id,patient_name,modality,scheduled_dt,site,department,ae,status) VALUES (?,?,?,?,?,?,?,?,?)",
                  (o.accession,o.patient_id,o.patient_name,o.modality,o.scheduled_dt,o.site,o.department,o.ae,o.status))
        conn.commit()
        return {"ok": True}
    except sqlite3.IntegrityError:
        raise HTTPException(409, "accession exists")
    finally:
        conn.close()

@app.get("/policies")
def get_policies():
    with open(CONFIG_PATH) as f:
        return json.load(f)

@app.put("/policies")
def set_policies(payload: dict):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(payload, f, indent=2)
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
