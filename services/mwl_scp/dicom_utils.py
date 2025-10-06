from pydicom.dataset import Dataset

def order_to_item(o: dict) -> Dataset:
    ds = Dataset()
    ds.PatientName = o.get('patient_name', '')
    ds.PatientID = o.get('patient_id', '')
    ds.AccessionNumber = o.get('accession', '')
    ds.Modality = o.get('modality', '')
    # Minimal SPS date/time (YYYYMMDD / HHMMSS)
    dt = (o.get('scheduled_dt','') or '')
    ds.ScheduledProcedureStepStartDate = dt[:10].replace('-','') if len(dt) >= 10 else ''
    ds.ScheduledProcedureStepStartTime = dt[11:19].replace(':','') if len(dt) >= 19 else ''
    ds.ScheduledStationAETitle = o.get('ae','') or ''
    return ds
