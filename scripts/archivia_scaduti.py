"""
ARCHIVIA BANDI SCADUTI
Mette attivo=false ai bandi con scadenza passata.
Esegui con: py -3.12 scripts/archivia_scaduti.py
"""
from supabase import create_client
from datetime import datetime
import time

SUPABASE_URL = "https://ieeriszlalrsbfsnarih.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImllZXJpc3psYWxyc2Jmc25hcmloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgxNjEyNjAsImV4cCI6MjA4MzczNzI2MH0.Sjwu1620mMTAAoKVHgXHQ1cA-m3hFXqtCtqjAQNErQo"

s = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Scarico bandi attivi...")
all_bandi = []
offset = 0
while True:
    r = s.table("bandi").select("id,titolo,scadenza,stato").eq("attivo", True).range(offset, offset + 999).execute()
    if not r.data:
        break
    all_bandi.extend(r.data)
    if len(r.data) < 1000:
        break
    offset += 1000

print(f"Bandi attivi: {len(all_bandi)}")

oggi = datetime.now()
scaduti = []

for b in all_bandi:
    scad = (b.get("scadenza") or "").strip()
    if not scad:
        continue
    try:
        d = datetime.strptime(scad, "%d/%m/%Y")
        if d < oggi:
            scaduti.append(b)
    except:
        pass

print(f"Bandi scaduti da archiviare: {len(scaduti)}")

if not scaduti:
    print("Nessun bando scaduto!")
    exit()

print(f"\nEsempi:")
for b in scaduti[:10]:
    print(f"  ID {b['id']}: {b['titolo'][:60]} (scad: {b['scadenza']})")

conferma = input(f"\nArchiviare {len(scaduti)} bandi? (si/no): ").strip().lower()
if conferma != "si":
    print("Annullato.")
    exit()

archived = 0
for b in scaduti:
    try:
        s.table("bandi").update({"attivo": False, "stato": "chiuso"}).eq("id", b["id"]).execute()
        archived += 1
    except Exception as e:
        print(f"  ERRORE {b['id']}: {e}")
    if archived > 0 and archived % 50 == 0:
        print(f"  ... {archived}/{len(scaduti)}")
        time.sleep(0.5)

print(f"\nArchiviati: {archived}")
print(f"Bandi rimasti attivi: {len(all_bandi) - archived}")
