# MWL Microservice (Starter)

This repo gives you a minimal Modality Worklist + HL7 intake stack.

## Run (Docker Desktop needed)
```powershell
docker compose up -d --build
```

Seed an example order (PowerShell):
```powershell
python scripts/seed_http.py
```

### Admin API (FastAPI)
- List: http://localhost:8000/orders
- Search: http://localhost:8000/orders?q=ACC123
- Policies:
  - GET:  http://localhost:8000/policies
  - PUT:  send updated JSON to that endpoint

### HL7 Intake
- **MLLP:** send HL7 v2 ORM^O01 to `localhost:2575`
- **Drop-folder:** put `*.hl7` files into `./inbox/`

### MWL SCP
- Listens on **2762**. Query it with your modality or tools like `findscu`.
- Results are filtered by AE→site/department policy in `config.json`.

> This is a starter. Improve HL7 mapping, authentication, logging, tests, and DB migrations as you iterate.
