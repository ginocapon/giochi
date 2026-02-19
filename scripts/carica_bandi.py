"""
CARICA NUOVI BANDI
Fase B: Inserimento nuovi bandi con check duplicati.
Esegui con: py -3.12 scripts/carica_bandi.py

ISTRUZIONI: Questo file viene generato da Claude ad ogni aggiornamento.
Non modificare manualmente - chiedi a Claude di generare i bandi.
"""
from supabase import create_client
from datetime import datetime
import re
import time

SUPABASE_URL = "https://ieeriszlalrsbfsnarih.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImllZXJpc3psYWxyc2Jmc25hcmloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgxNjEyNjAsImV4cCI6MjA4MzczNzI2MH0.Sjwu1620mMTAAoKVHgXHQ1cA-m3hFXqtCtqjAQNErQo"

s = create_client(SUPABASE_URL, SUPABASE_KEY)
now = datetime.now().isoformat()


def normalizza_url(url):
    u = (url or "").strip().lower()
    u = re.sub(r'^https?://', '', u)
    u = re.sub(r'^www\.', '', u)
    u = u.rstrip('/')
    return u


def parole_chiave(testo):
    stop = {'il','lo','la','le','gli','i','un','una','di','del','della','delle',
            'dei','degli','da','in','con','su','per','tra','fra','e','o','a','al',
            'alla','alle','ai','agli','che','non','si','come','anche','sono','nel',
            'nella','nelle','nei','negli','sul','sulla','sulle','sui','sugli',
            'piu','ed','bando','contributi','contributo','finanziamenti','agevolazioni',
            'incentivi','anno','anni','imprese','delle','degli','alla'}
    t = re.sub(r'[^a-z0-9\s]', ' ', (testo or "").lower())
    return set(p for p in t.split() if len(p) > 2 and p not in stop)


# ============================================
# NUOVI BANDI DA CARICARE
# (Questa lista viene generata da Claude)
# ============================================

bandi = [
    # ESEMPIO - sostituire con bandi reali:
    # {
    #     "titolo": "MIMIT — Nuova Sabatini 2026",
    #     "ente": "MIMIT",
    #     "tipo_ente": "ministero",
    #     "regione": "Nazionale",
    #     "tipo_contributo": "tasso_agevolato",
    #     "stato": "aperto",
    #     "scadenza": "31/12/2026",
    #     "descrizione": "Finanziamento agevolato per acquisto macchinari e tecnologie 4.0. Rivolto a PMI italiane di tutti i settori.",
    #     "url": "https://www.mimit.gov.it/nuova-sabatini",
    #     "fonte": "MIMIT",
    #     "attivo": True
    # },
]

if not bandi:
    print("Nessun bando da caricare. Modifica la lista 'bandi' nel file.")
    exit()

# CHECK DUPLICATI PRIMA DI INSERIRE
print("Scarico bandi esistenti per check duplicati...")
existing = []
offset = 0
while True:
    r = s.table("bandi").select("id,titolo,url,regione").eq("attivo", True).range(offset, offset + 999).execute()
    if not r.data:
        break
    existing.extend(r.data)
    if len(r.data) < 1000:
        break
    offset += 1000

existing_urls = set(normalizza_url(b.get("url")) for b in existing)

print(f"Bandi esistenti: {len(existing)}")
print(f"Nuovi bandi da caricare: {len(bandi)}")

# Filtra duplicati
to_insert = []
skipped = []
for b in bandi:
    url_norm = normalizza_url(b.get("url"))

    if url_norm and url_norm in existing_urls:
        skipped.append((b["titolo"], "URL duplicato"))
        continue

    pk = parole_chiave(b["titolo"])
    is_similar = False
    for ex in existing:
        if (ex.get("regione") or "") != (b.get("regione") or ""):
            continue
        epk = parole_chiave(ex.get("titolo"))
        if pk and epk and len(pk & epk) / len(pk | epk) >= 0.70:
            skipped.append((b["titolo"], f"Simile a ID {ex['id']}: {ex['titolo'][:50]}"))
            is_similar = True
            break

    if not is_similar:
        to_insert.append(b)

if skipped:
    print(f"\nSKIPPATI ({len(skipped)} duplicati):")
    for titolo, motivo in skipped:
        print(f"  SKIP: {titolo[:60]} -> {motivo}")

if not to_insert:
    print("\nNessun bando nuovo da inserire (tutti duplicati).")
    exit()

print(f"\nDA INSERIRE: {len(to_insert)} bandi")
for b in to_insert:
    print(f"  + {b['titolo'][:70]}")

conferma = input(f"\nInserire {len(to_insert)} bandi? (si/no): ").strip().lower()
if conferma != "si":
    print("Annullato.")
    exit()

inserted = 0
errors = 0
for b in to_insert:
    b["data_inserimento"] = now
    b["data_aggiornamento"] = now
    try:
        r = s.table("bandi").insert(b).execute()
        if r.data:
            inserted += 1
    except Exception as e:
        print(f"  ERRORE: {b['titolo'][:50]} -> {e}")
        errors += 1
    if inserted > 0 and inserted % 10 == 0:
        time.sleep(0.3)

print(f"\nInseriti: {inserted}")
print(f"Errori: {errors}")
print(f"Totale bandi nel DB: {len(existing) + inserted}")
