#!/usr/bin/env python3
"""Open Data Portals API."""

import requests
from typing import List, Dict
import hashlib

def get_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:16]

BANDI_KEYWORDS = ['bandi', 'finanziamenti', 'contributi', 'incentivi', 'pnrr', 'fesr']

def scrape_opendata() -> List[Dict]:
    bandi = []
    print("      → Dati.gov.it...")
    
    try:
        url = "https://www.dati.gov.it/api/3/action/package_search"
        for keyword in BANDI_KEYWORDS[:2]:
            params = {'q': keyword, 'rows': 10}
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    results = data.get('result', {}).get('results', [])
                    for dataset in results:
                        titolo = dataset.get('title', '')
                        if titolo:
                            bando = {
                                'titolo': titolo[:500],
                                'ente': dataset.get('organization', {}).get('title', 'Dati.gov.it'),
                                'tipo_ente': 'ente_nazionale',
                                'regione': 'Nazionale',
                                'tipo_contributo': 'open_data',
                                'stato': 'aperto',
                                'contributo_max': 'Vedi dataset',
                                'percentuale': 'N/A',
                                'scadenza': dataset.get('metadata_modified', 'N/A')[:10],
                                'descrizione': dataset.get('notes', titolo)[:1000],
                                'beneficiari': 'Vedi dataset',
                                'url': f"https://www.dati.gov.it/view-dataset/dataset?id={dataset.get('id', '')}",
                                'fonte': 'Dati.gov.it',
                                'hash_id': get_hash(titolo),
                                'attivo': True
                            }
                            bandi.append(bando)
        print(f"        ✓ {len(bandi)} dataset")
    except Exception as e:
        print(f"        ⚠️ Errore: {str(e)[:30]}")
    
    return bandi
