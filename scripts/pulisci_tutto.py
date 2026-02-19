"""
PULIZIA COMPLETA DATABASE BANDI
Fase C: Elimina duplicati URL, titoli simili, normalizza regioni.
Esegui con: py -3.12 scripts/pulisci_tutto.py
"""
from supabase import create_client
from collections import Counter
import time
import re

SUPABASE_URL = "https://ieeriszlalrsbfsnarih.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImllZXJpc3psYWxyc2Jmc25hcmloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgxNjEyNjAsImV4cCI6MjA4MzczNzI2MH0.Sjwu1620mMTAAoKVHgXHQ1cA-m3hFXqtCtqjAQNErQo"

s = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Scarico tutti i bandi attivi...")
all_bandi = []
offset = 0
while True:
    r = s.table("bandi").select("id,titolo,url,regione,ente").eq("attivo", True).range(offset, offset + 999).execute()
    if not r.data:
        break
    all_bandi.extend(r.data)
    if len(r.data) < 1000:
        break
    offset += 1000

print(f"Totale bandi attivi: {len(all_bandi)}")


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


# FASE 1: DUPLICATI URL
print("\n" + "=" * 60)
print("FASE 1: DUPLICATI PER URL")
print("=" * 60)

url_groups = {}
for b in all_bandi:
    u = normalizza_url(b.get("url"))
    if not u:
        continue
    if u not in url_groups:
        url_groups[u] = []
    url_groups[u].append(b)

url_dupes = {u: bandi for u, bandi in url_groups.items() if len(bandi) > 1}
url_excess = sum(len(bandi) - 1 for bandi in url_dupes.values())
print(f"URL duplicati: {len(url_dupes)} ({url_excess} record in eccesso)")

ids_url_delete = []
for u, bandi in url_dupes.items():
    sb = sorted(bandi, key=lambda x: x["id"])
    for b in sb[1:]:
        ids_url_delete.append(b["id"])


# FASE 2: TITOLI SIMILI
print("\n" + "=" * 60)
print("FASE 2: DUPLICATI PER SIMILARITA TITOLO")
print("=" * 60)

url_dupe_ids = set(ids_url_delete)
by_regione = {}
for b in all_bandi:
    reg = (b.get("regione") or "N/D").strip()
    if reg not in by_regione:
        by_regione[reg] = []
    by_regione[reg].append(b)

extra_dupes = set()
for reg, bandi in by_regione.items():
    for i in range(len(bandi)):
        for j in range(i + 1, len(bandi)):
            b1, b2 = bandi[i], bandi[j]
            if b1["id"] in url_dupe_ids and b2["id"] in url_dupe_ids:
                continue
            p1 = parole_chiave(b1["titolo"])
            p2 = parole_chiave(b2["titolo"])
            if p1 and p2 and len(p1 & p2) / len(p1 | p2) >= 0.70:
                extra_dupes.add(max(b1["id"], b2["id"]))

print(f"Titoli simili da eliminare: {len(extra_dupes)}")


# FASE 3: REGIONI
print("\n" + "=" * 60)
print("FASE 3: REGIONI DA NORMALIZZARE")
print("=" * 60)

REGIONE_FIX = {
    "Friuli-Venezia Giulia": "Friuli Venezia Giulia",
    "Valle Aosta": "Valle d'Aosta",
    "Trentino-Alto-Adige": "Trentino-Alto Adige",
    "Mezzogiorno": "Sud Italia",
    "Centro-Nord": "Nazionale",
}

regioni_da_fix = []
for b in all_bandi:
    reg = b.get("regione") or ""
    if reg in REGIONE_FIX:
        regioni_da_fix.append((b["id"], reg, REGIONE_FIX[reg]))

print(f"Regioni da correggere: {len(regioni_da_fix)}")


# RIEPILOGO
all_ids_delete = set(ids_url_delete) | extra_dupes
print(f"\n{'=' * 60}")
print(f"RIEPILOGO")
print(f"{'=' * 60}")
print(f"Bandi attivi ora:           {len(all_bandi)}")
print(f"Duplicati URL:              {len(ids_url_delete)}")
print(f"Duplicati titolo simile:    {len(extra_dupes)}")
print(f"TOTALE da eliminare:        {len(all_ids_delete)}")
print(f"Regioni da normalizzare:    {len(regioni_da_fix)}")
print(f"Bandi dopo pulizia:         {len(all_bandi) - len(all_ids_delete)}")

if not all_ids_delete and not regioni_da_fix:
    print("\nDatabase pulito! Niente da fare.")
    exit()

conferma = input(f"\nProcedere? (si/no): ").strip().lower()
if conferma != "si":
    print("Annullato.")
    exit()

deleted = 0
if all_ids_delete:
    print(f"\nEliminazione {len(all_ids_delete)} duplicati...")
    for bid in all_ids_delete:
        try:
            r = s.table("bandi").delete().eq("id", bid).execute()
            if r.data:
                deleted += 1
        except Exception as e:
            print(f"  ERRORE {bid}: {e}")
        if deleted > 0 and deleted % 100 == 0:
            print(f"  ... {deleted}/{len(all_ids_delete)}")
            time.sleep(0.5)
    print(f"  Eliminati: {deleted}")

fixed = 0
if regioni_da_fix:
    print(f"\nNormalizzo regioni...")
    for bid, old, new in regioni_da_fix:
        try:
            s.table("bandi").update({"regione": new}).eq("id", bid).execute()
            fixed += 1
        except:
            pass
    print(f"  Corrette: {fixed}")

print(f"\nFATTO! Eliminati: {deleted}, Regioni corrette: {fixed}")
print(f"Bandi rimasti: {len(all_bandi) - deleted}")
