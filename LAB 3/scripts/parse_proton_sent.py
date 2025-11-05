#!/usr/bin/env python3
"""
parse_proton_sent.py
Read ProtonMail API JSON for a sent message and print a human-readable summary,
save PGP body to file and save attachments metadata.
Usage: python3 parse_proton_sent.py sent_response.json
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
try:
    from zoneinfo import ZoneInfo
    TZ_LISBON = ZoneInfo("Europe/Lisbon")
except Exception:
    TZ_LISBON = None

def ts_to_iso(ts):
    try:
        # Some APIs use integer seconds; ensure int
        t = int(ts)
        dt_utc = datetime.fromtimestamp(t, tz=timezone.utc)
        if TZ_LISBON:
            dt_local = dt_utc.astimezone(TZ_LISBON)
            return dt_utc.isoformat(), dt_local.isoformat()
        else:
            return dt_utc.isoformat(), None
    except Exception:
        return None, None

def pprint_message(msg):
    print("=== MESSAGE SUMMARY ===")
    print("ID:", msg.get("ID"))
    print("Subject:", msg.get("Subject"))
    time_ts = msg.get("Time") or msg.get("DeliveryTime")
    utc_iso, local_iso = ts_to_iso(time_ts) if time_ts else (None,None)
    print("Time (timestamp):", time_ts)
    if utc_iso:
        print("Time (UTC)    :", utc_iso)
    if local_iso:
        print("Time (Europe/Lisbon):", local_iso)
    print("SenderAddress:", msg.get("SenderAddress") or (msg.get("Sender",{}).get("Address")))
    print("To:", ", ".join([r.get("Address") for r in msg.get("ToList", [])]) or "[]")
    print("IsEncrypted:", bool(msg.get("IsEncrypted")))
    print("NumAttachments:", msg.get("NumAttachments"))
    print("Size (bytes):", msg.get("Size"))
    print()

def save_pgp_body(msg, outdir):
    body = msg.get("Body")
    if not body:
        print("No Body field found.")
        return None
    # Save the PGP armored body
    out = outdir / "message.pgp.asc"
    with out.open("w", encoding="utf-8") as f:
        f.write(body)
    print("Saved PGP body to:", out)
    return out

def save_parsed_headers(msg, outdir):
    ph = msg.get("ParsedHeaders") or msg.get("Header")
    if not ph:
        print("No parsed headers found.")
        return None
    out = outdir / "parsed_headers.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(ph, f, indent=2, ensure_ascii=False)
    print("Saved parsed headers to:", out)
    return out

def save_attachments(msg, outdir):
    atts = msg.get("Attachments", [])
    if not atts:
        print("No attachments metadata found.")
        return None
    out = outdir / "attachments.json"
    # We won't try to reconstruct the binary attachment here (not present)
    with out.open("w", encoding="utf-8") as f:
        json.dump(atts, f, indent=2, ensure_ascii=False)
    print("Saved attachments metadata to:", out)
    # Print summary to console
    print("\nAttachments:")
    for a in atts:
        print(" - Name:", a.get("Name"), "Size:", a.get("Size"), "MIME:", a.get("MIMEType"), "ID:", a.get("ID"))
    return out

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_proton_sent.py sent_response.json")
        sys.exit(1)
    p = Path(sys.argv[1])
    if not p.exists():
        print("File not found:", p)
        sys.exit(1)
    data = json.loads(p.read_text(encoding="utf-8"))
    # If the JSON includes top-level 'Sent' or similar, adapt
    # try to find the message dictionary
    msg = None
    if "Sent" in data:
        msg = data["Sent"]
    elif "Message" in data:
        msg = data["Message"]
    else:
        # maybe the file is exactly the message already
        msg = data

    outdir = Path(".") / (p.stem + "_parsed")
    outdir.mkdir(exist_ok=True)

    pprint_message(msg)
    save_pgp_body(msg, outdir)
    save_parsed_headers(msg, outdir)
    save_attachments(msg, outdir)

    # If conversation info exists, show some
    conv = data.get("Conversation")
    if conv:
        print("\n=== CONVERSATION SUMMARY ===")
        print("Conversation ID:", conv.get("ID"))
        print("Subject:", conv.get("Subject"))
        print("NumMessages:", conv.get("NumMessages"))
        print("Labels:", [lab.get("ID") for lab in conv.get("Labels", [])])

if __name__ == "__main__":
    main()

