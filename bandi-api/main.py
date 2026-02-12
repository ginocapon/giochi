#!/usr/bin/env python3
"""
===== BANDI ITALIA - API FIRST SYSTEM =====
Sistema intelligente basato su API ufficiali gratuite.

Caratteristiche:
- Priorità alle API ufficiali (ANAC, CKAN, RSS)
- Deduplicazione via hash
- Auto-aggiornamento giornaliero
- Nessun scraping HTML fragile
"""

import os
import sys
from datetime import datetime
from typing import List, Dict
import hashlib

from supabase import create_client, Client

# Import scrapers
from scrapers.bandi_statici import scrape_bandi_statici
from scrapers.api_rss import scrape_rss_feeds
from scrapers.api_opendata import scrape_opendata
from scrapers.api_anac import scrape_anac
from scrapers.api_contratti import scrape_contratti_pubblici


# Supabase config
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')


def get_supabase() -> Client:
    """Crea client Supabase."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY richiesti")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_hash(text: str) -> str:
    """Genera hash per deduplicazione."""
    return hashlib.md5(text.encode()).hexdigest()[:16]


def deduplicate_bandi(bandi: List[Dict]) -> List[Dict]:
    """Rimuove duplicati basandosi sull'hash del titolo."""
    seen = set()
    unique = []
    
    for bando in bandi:
        # Crea hash se non esiste
        if 'hash_id' not in bando:
            bando['hash_id'] = get_hash(bando.get('titolo', ''))
        
        hash_id = bando['hash_id']
        
        if hash_id not in seen:
            seen.add(hash_id)
            unique.append(bando)
    
    return unique


def save_to_supabase(bandi: List[Dict]) -> Dict:
    """
    Salva i bandi su Supabase con upsert intelligente.
    Usa hash_id per evitare duplicati.
    """
    if not bandi:
        return {'inserted': 0, 'updated': 0, 'errors': 0}
    
    supabase = get_supabase()
    inserted = 0
    updated = 0
    errors = 0
    
    for bando in bandi:
        try:
            # Prepara il record
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
            
            # Upsert basato su titolo
            result = supabase.table('bandi').upsert(
                record,
                on_conflict='titolo'
            ).execute()
            
            if result.data:
                inserted += 1
                
        except Exception as e:
            error_msg = str(e)
            if 'duplicate' in error_msg.lower():
                updated += 1
            else:
                print(f"      ⚠️ {bando.get('titolo', 'N/A')[:40]}: {error_msg[:50]}")
                errors += 1
    
    return {'inserted': inserted, 'updated': updated, 'errors': errors}


def run_all_scrapers():
    """Esegue tutti gli scraper API-first."""
    
    print("=" * 60)
    print("🇮🇹 BANDI ITALIA - API FIRST SYSTEM")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)
    
    all_bandi = []
    stats = {}
    
    # 1. BANDI STATICI (sempre garantiti)
    print("\n📌 [1/5] BANDI NAZIONALI GARANTITI")
    try:
        bandi = scrape_bandi_statici()
        all_bandi.extend(bandi)
        stats['Nazionali'] = len(bandi)
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        stats['Nazionali'] = 0
    
    # 2. RSS FEEDS (Regioni, MIMIT, etc.)
    print("\n📌 [2/5] RSS FEEDS UFFICIALI")
    try:
        bandi = scrape_rss_feeds()
        all_bandi.extend(bandi)
        stats['RSS'] = len(bandi)
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        stats['RSS'] = 0
    
    # 3. ANAC (gare pubbliche)
    print("\n📌 [3/5] ANAC OPEN DATA")
    try:
        bandi = scrape_anac()
        all_bandi.extend(bandi)
        stats['ANAC'] = len(bandi)
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        stats['ANAC'] = 0
    
    # 4. CONTRATTI PUBBLICI
    print("\n📌 [4/5] CONTRATTI PUBBLICI")
    try:
        bandi = scrape_contratti_pubblici()
        all_bandi.extend(bandi)
        stats['Contratti'] = len(bandi)
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        stats['Contratti'] = 0
    
    # 5. OPEN DATA PORTALS
    print("\n📌 [5/5] OPEN DATA PORTALS")
    try:
        bandi = scrape_opendata()
        all_bandi.extend(bandi)
        stats['OpenData'] = len(bandi)
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        stats['OpenData'] = 0
    
    # DEDUPLICAZIONE
    print("\n" + "=" * 60)
    print("🔄 DEDUPLICAZIONE...")
    unique_bandi = deduplicate_bandi(all_bandi)
    duplicates = len(all_bandi) - len(unique_bandi)
    print(f"   Rimossi {duplicates} duplicati")
    
    # SALVATAGGIO
    print("\n💾 SALVATAGGIO SU SUPABASE...")
    result = save_to_supabase(unique_bandi)
    
    # RIEPILOGO
    print("\n" + "=" * 60)
    print("📊 RIEPILOGO FINALE")
    print("=" * 60)
    
    total_found = sum(stats.values())
    print(f"\n🔍 BANDI TROVATI: {total_found}")
    for source, count in stats.items():
        print(f"   {source}: {count}")
    
    print(f"\n🔄 DOPO DEDUPLICAZIONE: {len(unique_bandi)}")
    print(f"💾 SALVATI/AGGIORNATI: {result['inserted']}")
    
    if result['errors'] > 0:
        print(f"⚠️  ERRORI: {result['errors']}")
    
    print("\n✅ AGGIORNAMENTO COMPLETATO!")
    print("=" * 60)
    
    return len(unique_bandi)


if __name__ == '__main__':
    run_all_scrapers()
