from typing import Iterable, Any

def _get(field: Any, key: str, default=None):
    """Compat: legge sia da dict che da oggetti (es. Pydantic)."""
    if isinstance(field, dict):
        return field.get(key, default)
    return getattr(field, key, default)

def to_vcard(fullname: str, fields: Iterable[Any]) -> str:
    """
    Converte una lista di campi (dict o CardField) in una vCard 3.0.
    Gestisce 'visible', 'type', 'value' e mapping base (tel/email/url/org/title/addr).
    """
    tel, emails, urls, orgs = [], [], [], []
    title = None
    adr = None

    for f in fields or []:
        if not _get(f, "visible", True):
            continue
        ftype = (_get(f, "type", "") or "").lower()
        fval = (_get(f, "value", "") or "").strip()
        if not ftype or not fval:
            continue

        if ftype in ("phone", "tel", "mobile"):
            tel.append(fval)
        elif ftype in ("email",):
            emails.append(fval)
        elif ftype in ("url", "website", "site", "link"):
            urls.append(fval)
        elif ftype in ("company", "org", "organization"):
            orgs.append(fval)
        elif ftype in ("role", "title", "job"):
            # conserva il primo title
            if title is None:
                title = fval
        elif ftype in ("address", "addr"):
            if adr is None:
                adr = fval

    # vCard 3.0 con CRLF
    lines = ["BEGIN:VCARD", "VERSION:3.0", f"FN:{fullname}"]
    if title:
        lines.append(f"TITLE:{title}")
    for o in orgs:
        lines.append(f"ORG:{o}")
    for e in emails:
        lines.append(f"EMAIL;TYPE=INTERNET:{e}")
    for t in tel:
        lines.append(f"TEL;TYPE=CELL:{t}")
    for u in urls:
        lines.append(f"URL:{u}")
    if adr:
        # Formato ADR: PO Box;Extended;Street;Locality;Region;Postal Code;Country
        # Mettiamo l'indirizzo in Street come fallback
        lines.append(f"ADR;TYPE=WORK:;;{adr};;;;")
    lines.append("END:VCARD")
    return "\r\n".join(lines)
