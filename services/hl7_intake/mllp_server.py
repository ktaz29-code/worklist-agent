import asyncio, os, sqlite3
from hl7_utils import extract_order_fields

DB_PATH = os.getenv('DB_PATH', '/app/data/orders.db')
PORT = int(os.getenv('MLLP_PORT', '2575'))

START_BLOCK = b'\x0b'; END_BLOCK = b'\x1c'; CARRIAGE_RETURN = b'\x0d'

async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    data = await reader.readuntil(END_BLOCK + CARRIAGE_RETURN)
    raw = data.strip(END_BLOCK + CARRIAGE_RETURN).strip(START_BLOCK).decode('utf-8', errors='ignore')
    order = extract_order_fields(raw)
    accession = order.get('accession') or 'ACC' + str(abs(hash(raw))%10_000_000)
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
      accession TEXT PRIMARY KEY,
      patient_id TEXT, patient_name TEXT, modality TEXT,
      scheduled_dt TEXT, site TEXT, department TEXT, ae TEXT,
      status TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute("INSERT OR REPLACE INTO orders(accession,patient_id,patient_name,modality,scheduled_dt,site,department,ae,status) VALUES (?,?,?,?,?,?,?,?,?)",
              (accession, order.get('patient_id',''), order.get('patient_name',''), order.get('modality',''),
               order.get('scheduled_dt',''), order.get('site',''), order.get('department',''), '', 'SCHEDULED'))
    conn.commit(); conn.close()
    # Minimal ACK
    ack = f"MSH|^~\\&|MWL|RIS||MODALITY||ACK|1|P|2.3\rMSA|AA|1\r".encode()
    writer.write(START_BLOCK + ack + END_BLOCK + CARRIAGE_RETURN)
    await writer.drain(); writer.close(); await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle, '0.0.0.0', PORT)
    async with server:
        print(f"MLLP listening on {PORT}")
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
