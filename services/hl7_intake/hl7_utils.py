from hl7apy.parser import parse_message

def _get(component, default=""):
    try:
        return component.to_er7()
    except Exception:
        return default

def extract_order_fields(raw: str):
    # expects ORM^O01; parses defensively
    msg = parse_message(raw, find_groups=False, validation_level=None)
    pid = getattr(msg, 'PID', None)
    obr = getattr(msg, 'OBR', None)
    pv1 = getattr(msg, 'PV1', None)

    patient_id = _get(pid.pid_3.cx_1) if pid else ""
    patient_name = _get(pid.pid_5.xpn_1) if pid else ""
    accession = _get(obr.obr_18.cx_1) if obr else ""
    modality = _get(obr.obr_24.cwe_1) if obr else ""
    # OBR-36 (Scheduled Date/Time) is TQ1 in some feeds; this is a simple starter
    scheduled_dt = _get(obr.obr_36.tq_1) if (obr and hasattr(obr, 'obr_36')) else ""

    site = _get(pv1.pv1_3.pl_1) if pv1 else ""
    department = _get(pv1.pv1_3.pl_2) if pv1 else ""

    return dict(accession=accession, patient_id=patient_id, patient_name=patient_name,
                modality=modality, scheduled_dt=scheduled_dt, site=site, department=department)
