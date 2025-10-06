import os, sqlite3, json
from pynetdicom import AE, evt, ALL_TRANSFER_SYNTAXES
from pynetdicom.sop_class import ModalityWorklistInformationFind
from dicom_utils import order_to_item

DB_PATH = os.getenv('DB_PATH','/app/data/orders.db')
CONFIG_PATH = os.getenv('CONFIG_PATH','/app/config.json')
PORT = int(os.getenv('MWL_PORT','2762'))

with open(CONFIG_PATH) as f:
    POLICIES = json.load(f).get('ae_policies', {})

def load_orders():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("SELECT accession,patient_id,patient_name,modality,scheduled_dt,site,department,ae,status FROM orders")
    keys=["accession","patient_id","patient_name","modality","scheduled_dt","site","department","ae","status"]
    rows=[dict(zip(keys,r)) for r in c.fetchall()]
    conn.close(); return rows

def on_c_find(event):
    requestor_ae = event.assoc.requestor.ae_title.decode().strip()
    policy = POLICIES.get(requestor_ae)
    items = []
    for o in load_orders():
        if policy:
            if o.get('site') not in policy.get('sites', []):
                continue
            if o.get('department') not in policy.get('departments', []):
                continue
        items.append(order_to_item(o))
    for ds in items:
        yield 0xFF00, ds

handlers = [(evt.EVT_C_FIND, on_c_find)]

ae = AE(ae_title=b"MWL")
ae.add_supported_context(ModalityWorklistInformationFind, ALL_TRANSFER_SYNTAXES)
ae.start_server(("0.0.0.0", PORT), block=True, evt_handlers=handlers)
