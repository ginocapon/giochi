"""
CHECK STATO DATABASE BANDI
Fase A: Analisi completa prima di qualsiasi operazione.
Esegui con: py -3.12 scripts/check_stato.py
"""
from supabase import create_client
from collections import Counter
from datetime import datetime
import re

SUPABASE_URL = "https://ieeriszlalrsbfsnarih.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImllZXJpc3psYWxyc2Jmc25hcmloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgxNjEyNjAsImV4cCI6MjA4MzczNzI2MH0.Sjwu1620mMTAAoKVHgXHQ1cA-m3hFXqtCtqjAQNErQo"

s = create_client(SUPABASE_URL, SUPABASE_KEY)

print("=" * 60)
print(f"CHECK STATO DATABASE - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
print("=" * 60)

# 1. CONTA TOTALE
r = s.table("bandi").select("id", count="exact").eq("attivo", True).execute()
print(f"\n1. BANDI ATTIVI TOTALI: {r.count}")

# 2. SCARICA TUTTI
print("\nScaricamento in corso...")
all_bandi = []
offset = 0
while True:
    r = s.table("bandi").select("id,titolo,url,regione,ente,scadenza,stato").eq("attivo", True).range(offset, offset + 999).execute()
    if not r.data:
        break
    all_bandi.extend(r.data)
    if len(r.data) < 1000:
        break
    offset += 1000

print(f"   Scaricati: {len(all_bandi)}")

# 3. BANDI PER REGIONE
print(f"\n2. BANDI PER REGIONE:")
regioni = Counter(b.get("regione") or "N/D" for b in all_bandi)
for r, c in regioni.most_common():
    print(f"   {r}: {c}")

# 4. BANDI PER TIPO ENTE
print(f"\n3. BANDI PER STATO:")
stati = Counter(b.get("stato") or "N/D" for b in all_bandi)
for st, c in stati.most_common():
    print(f"   {st}: {c}")

# 5. DUPLICATI URL
def normalizza_url(url):
    u = (url or "").strip().lower()
    u = re.sub(r'^https?://', '', u)
    u = re.sub(r'^www\.', '', u)
    u = u.rstrip('/')
    return u

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

print(f"\n4. DUPLICATI URL:")
print(f"   URL unici: {len(url_groups)}")
print(f"   URL duplicati: {len(url_dupes)} ({url_excess} record in eccesso)")

if url_dupes:
    print(f"\n   Top 10 URL duplicati:")
    for u, bandi in sorted(url_dupes.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"   [{len(bandi)}x] {u[:80]}")

# 6. SIMILARITA TITOLI
def parole_chiave(testo):
    stop = {'il','lo','la','le','gli','i','un','una','di','del','della','delle',
            'dei','degli','da','in','con','su','per','tra','fra','e','o','a','al',
            'alla','alle','ai','agli','che','non','si','come','anche','sono','nel',
            'nella','nelle','nei','negli','sul','sulla','sulle','sui','sugli',
            'piu','ed','bando','contributi','contributo','finanziamenti','agevolazioni',
            'incentivi','anno','anni','imprese','delle','degli','alla'}
    t = re.sub(r'[^a-z0-9\s]', ' ', (testo or "").lower())
    return set(p for p in t.split() if len(p) > 2 and p not in stop)

by_regione = {}
for b in all_bandi:
    reg = (b.get("regione") or "N/D").strip()
    if reg not in by_regione:
        by_regione[reg] = []
    by_regione[reg].append(b)

similar_count = 0
print(f"\n5. TITOLI SIMILI (>=70% stessa regione):")
for reg, bandi in by_regione.items():
    for i in range(len(bandi)):
        for j in range(i + 1, len(bandi)):
            p1 = parole_chiave(bandi[i]["titolo"])
            p2 = parole_chiave(bandi[j]["titolo"])
            if p1 and p2:
                sim = len(p1 & p2) / len(p1 | p2)
                if sim >= 0.70:
                    similar_count += 1
                    if similar_count <= 10:
                        print(f"   [{sim:.0%}] ID {bandi[i]['id']} vs {bandi[j]['id']}")
                        print(f"      A: {bandi[i]['titolo'][:70]}")
                        print(f"      B: {bandi[j]['titolo'][:70]}")

print(f"   Totale coppie simili: {similar_count}")

# 7. REGIONI NON STANDARD
REGIONI_OK = {"Nazionale","Italia","Sud Italia","Piemonte","Valle d'Aosta","Lombardia",
    "Trentino-Alto Adige","Veneto","Friuli Venezia Giulia","Liguria","Emilia-Romagna",
    "Toscana","Umbria","Marche","Lazio","Abruzzo","Molise","Campania","Puglia",
    "Basilicata","Calabria","Sicilia","Sardegna"}

non_standard = {r: c for r, c in regioni.items() if r not in REGIONI_OK}
print(f"\n6. REGIONI NON STANDARD:")
if non_standard:
    for r, c in non_standard.items():
        print(f"   '{r}': {c} bandi")
else:
    print(f"   Tutte standard!")

# 8. ULTIMI 5 INSERITI
ultimi = sorted(all_bandi, key=lambda x: x["id"], reverse=True)[:5]
print(f"\n7. ULTIMI 5 BANDI INSERITI:")
for b in ultimi:
    print(f"   ID {b['id']}: {b['titolo'][:70]}")

# 9. SCADENZE PASSATE ANCORA ATTIVE
oggi = datetime.now()
scaduti_attivi = 0
for b in all_bandi:
    scad = b.get("scadenza") or ""
    try:
        d = datetime.strptime(scad, "%d/%m/%Y")
        if d < oggi:
            scaduti_attivi += 1
    except:
        pass

print(f"\n8. BANDI SCADUTI ANCORA ATTIVI: {scaduti_attivi}")

# RIEPILOGO
print(f"\n{'=' * 60}")
print(f"RIEPILOGO")
print(f"{'=' * 60}")
print(f"Bandi attivi:          {len(all_bandi)}")
print(f"Duplicati URL:         {url_excess}")
print(f"Titoli simili:         {similar_count}")
print(f"Regioni non standard:  {len(non_standard)}")
print(f"Scaduti ancora attivi: {scaduti_attivi}")
problemi = url_excess + similar_count + len(non_standard) + scaduti_attivi
if problemi == 0:
    print(f"\nDATABASE PULITO!")
else:
    print(f"\nPROBLEMI DA RISOLVERE: {problemi}")
    print(f"Lancia: py -3.12 scripts/pulisci_tutto.py")
print("=" * 60)
