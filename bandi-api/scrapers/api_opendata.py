#!/usr/bin/env python3
"""
===== OPEN DATA PORTALS (CKAN) =====
Accesso a portali Open Data italiani via API CKAN.
"""

import requests
from typing import List, Dict
import hashlib


def get_hash(text: str) -> str:
    """Genera hash per deduplicazione."""
    return hashlib.md5(text.encode()).hexdigest()[:16]


# Portali Open Data con API CKAN
OPENDATA_PORTALS = [
    {
        'nome': 'OpenCoesione',
        'base_url': 'https://opencoesione.gov.it/api',
        'tipo_ente': 'ente_nazionale',
        'regione': 'Nazionale'
    },
    {
        'nome': 'Dati.gov.it',
        'base_url': 'https://www.dati.gov.it/api/3/action',
        'tipo_ente': 'ente_nazionale',
        'regione': 'Nazionale'
    },
]


# Keywords per filtrare i dataset rilevanti
BANDI_KEYWORDS = [
    'bandi', 'finanziamenti', 'contributi', 'incentivi',
    'pnrr', 'fesr', 'fondi europei', 'agevolazioni',
    'gare', 'appalti'
]


def search_ckan_datasets(portal: dict) -> List[Dict]:
    """Cerca dataset su un portale CKAN."""
    bandi = []
    
    for keyword in BANDI_KEYWORDS[:3]:  # Limita le query
        try:
            url = f"{portal['base_url']}/package_search"
            params = {
                'q': keyword,
                'rows': 20
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    results = data.get('result', {}).get('results', [])
                    
                    for dataset in results:
                        bando = parse_ckan_dataset(dataset, portal)
                        if bando:
                            bandi.append(bando)
                            
        except Exception as e:
            pass
    
    return bandi


def parse_ckan_dataset(dataset: dict, portal: dict) -> Dict:
    """Parse di un dataset CKAN."""
    try:
        titolo = dataset.get('title', '')
        if not titolo:
            return None
        
        # Verifica se è rilevante
        full_text = f"{titolo} {dataset.get('notes', '')}".lower()
        if not any(kw in full_text for kw in BANDI_KEYWORDS):
            return None
            
        return {
            'titolo': titolo[:500],
            'ente': dataset.get('organization', {}).get('title', portal['nome']),
            'tipo_ente': portal['tipo_ente'],
            'regione': portal['regione'],
            'tipo_contributo': 'open_data',
            'stato': 'aperto',
            'contributo_max': 'Vedi dataset',
            'percentuale': 'N/A',
            'scadenza': dataset.get('metadata_modified', 'N/A')[:10],
            'descrizione': dataset.get('notes', titolo)[:1000],
            'beneficiari': 'Vedi dataset',
            'url': f"https://www.dati.gov.it/view-dataset/dataset?id={dataset.get('id', '')}",
            'fonte': portal['nome'],
            'hash_id': get_hash(titolo),
            'attivo': True
        }
    except:
        return None


def scrape_opendata() -> List[Dict]:
    """Funzione principale per Open Data."""
    bandi = []
    
    for portal in OPENDATA_PORTALS:
        print(f"      → {portal['nome']}...")
        try:
            risultati = search_ckan_datasets(portal)
            if risultati:
                bandi.extend(risultati)
                print(f"        ✓ {len(risultati)} dataset")
            else:
                print(f"        - Nessun risultato")
        except Exception as e:
            print(f"        ⚠️ Errore: {str(e)[:30]}")
    
    return bandi


if __name__ == '__main__':
    print("Test Open Data...")
    risultati = scrape_opendata()
    print(f"\nTotale: {len(risultati)} dataset")
