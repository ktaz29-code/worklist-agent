import json, time
import urllib.request

data = {
  "accession":"ACC123",
  "patient_id":"P001",
  "patient_name":"DOE^JOHN",
  "modality":"CT",
  "scheduled_dt":"2025-10-06T14:00:00",
  "site":"STAR",
  "department":"CT",
  "ae":"CT01",
  "status":"SCHEDULED"
}

req = urllib.request.Request(
    "http://localhost:8000/orders",
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type":"application/json"},
    method="POST"
)
with urllib.request.urlopen(req) as resp:
    print("Seed response:", resp.status, resp.read().decode())
