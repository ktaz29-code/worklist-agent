import time, os, sqlite3
from hl7_utils import extract_order_fields

INBOX = '/app/inbox'
DB_PATH = os.getenv('DB_PATH', '/app/data/orders.db')
os.makedirs(INBOX, exist_ok=True)

def ensure_db():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
      accession TEXT PRIMARY KEY,
      patient_id TEXT, patient_name TEXT, modality TEXT,
      scheduled_dt TEXT, site TEXT, department TEXT, ae TEXT,
      status TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit(); conn.close()

ensure_db()

while True:
    for f in [x for x in os.listdir(INBOX) if x.endswith('.hl7')]:
        p = os.path.join(INBOX, f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
            raw = fh.read()
        order = extract_order_fields(raw)
        accession = order.get('accession') or f"FILE{int(time.time())}"
        conn = sqlite3.connect(DB_PATH); c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO orders(accession,patient_id,patient_name,modality,scheduled_dt,site,department,ae,status) VALUES (?,?,?,?,?,?,?,?,?)",
                  (accession, order.get('patient_id',''), order.get('patient_name',''), order.get('modality',''),
                   order.get('scheduled_dt',''), order.get('site',''), order.get('department',''), '', 'SCHEDULED'))
        conn.commit(); conn.close()
        os.remove(p)
    time.sleep(2)
