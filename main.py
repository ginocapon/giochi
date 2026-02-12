#!/usr/bin/env python3
"""
===== BANDI ITALIA - API FIRST SYSTEM =====
"""

import os
import sys
from datetime import datetime
from typing import List, Dict
import hashlib

from supabase import create_client, Client

from scrapers.bandi_statici import scrape_bandi_statici
from scrapers.api_rss import scrape_rss_feeds
from scrapers.api_opendata import scrape_opendata

SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')


def get_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY richiesti")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:16]


def deduplicate_bandi(bandi: List[Dict]) -> List[Dict]:
    seen = set()
    unique = []
    for bando in bandi:
        if 'hash_id' not in bando:
            bando['hash_id'] = get_hash(bando.get('titolo', ''))
        hash_id = bando['hash_id']
        if hash_id not in seen:
            seen.add(hash_id)
            unique.append(bando)
    return unique


def save_to_supabase(bandi: List[Dict]) -> Dict:
    if not bandi:
        return {'inserted': 0, 'errors': 0}
    
    supabase = get_supabase()
    inserted = 0
    errors = 0
    
    for bando in bandi:
        try:
            record = {
                'titolo': bando.get('titolo', '')[:500],
                'ente': bando.get('ente', 'N/A'),
                'tipo_ente': bando.get('tipo_ente', 'altro'),
                'regione': bando.get('regione', 'Nazionale'),
                'tipo_contributo': bando.get('tipo_contributo', 'misto'),
                'stato': bando.get('stato', 'aperto'),
                'contributo_max': str(bando.get('contributo_max', 'Vedi bando')),
                'percentuale': str(bando.get('percentuale', 'Vedi bando')),
                'scadenza': bando.get('scadenza', 'Vedi bando'),
                'descrizione': bando.get('descrizione', '')[:2000],
                'beneficiari': bando.get('beneficiari', 'Imprese'),
                'url': bando.get('url', ''),
                'fonte': bando.get('fonte', 'API'),
                'attivo': True,
                'updated_at': datetime.now().isoformat()
            }
            
            result = supabase.table('bandi').upsert(record, on_conflict='titolo').execute()
            if result.data:
                inserted += 1
        except Exception as e:
            print(f"      ⚠️ {bando.get('titolo', 'N/A')[:40]}: {str(e)[:50]}")
            errors += 1
    
    return {'inserted': inserted, 'errors': errors}


def run_all_scrapers():
    print("=" * 60)
    print("🇮🇹 BANDI ITALIA - API FIRST SYSTEM")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    
    all_bandi = []
    stats = {}
    
    print("\n📌 [1/3] BANDI NAZIONALI GARANTITI")
    try:
        bandi = scrape_bandi_statici()
        all_bandi.extend(bandi)
        stats['Nazionali'] = len(bandi)
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        stats['Nazionali'] = 0
    
    print("\n📌 [2/3] RSS FEEDS UFFICIALI")
    try:
        bandi = scrape_rss_feeds()
        all_bandi.extend(bandi)
        stats['RSS'] = len(bandi)
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        stats['RSS'] = 0
    
    print("\n📌 [3/3] OPEN DATA PORTALS")
    try:
        bandi = scrape_opendata()
        all_bandi.extend(bandi)
        stats['OpenData'] = len(bandi)
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        stats['OpenData'] = 0
    
    print("\n" + "=" * 60)
    print("🔄 DEDUPLICAZIONE...")
    unique_bandi = deduplicate_bandi(all_bandi)
    print(f"   Rimossi {len(all_bandi) - len(unique_bandi)} duplicati")
    
    print("\n💾 SALVATAGGIO SU SUPABASE...")
    result = save_to_supabase(unique_bandi)
    
    print("\n" + "=" * 60)
    print("📊 RIEPILOGO FINALE")
    print("=" * 60)
    print(f"\n🔍 BANDI TROVATI: {sum(stats.values())}")
    for source, count in stats.items():
        print(f"   {source}: {count}")
    print(f"\n🔄 DOPO DEDUPLICAZIONE: {len(unique_bandi)}")
    print(f"💾 SALVATI: {result['inserted']}")
    if result['errors'] > 0:
        print(f"⚠️  ERRORI: {result['errors']}")
    print("\n✅ COMPLETATO!")
    
    return len(unique_bandi)


if __name__ == '__main__':
    run_all_scrapers()
