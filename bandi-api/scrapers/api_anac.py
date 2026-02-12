#!/usr/bin/env python3
"""
===== ANAC OPEN DATA API =====
Fonte ufficiale per gare d'appalto pubbliche italiane.
https://dati.anticorruzione.it/
"""

import requests
from typing import List, Dict
from datetime import datetime, timedelta
import hashlib

# Endpoint ANAC Open Data
ANAC_BASE_URL = "https://dati.anticorruzione.it/api/3/action"


def get_hash(text: str) -> str:
    """Genera hash per deduplicazione."""
    return hashlib.md5(text.encode()).hexdigest()[:16]


def fetch_anac_gare() -> List[Dict]:
    """
    Recupera le gare pubbliche da ANAC Open Data.
    Usa l'API CKAN per accedere ai dataset.
    """
    bandi = []
    
    try:
        # Dataset delle gare
        datasets = [
            "gare-contratti-pubblici",
            "bandi-gara",
        ]
        
        for dataset_id in datasets:
            url = f"{ANAC_BASE_URL}/package_show?id={dataset_id}"
            
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        resources = data.get('result', {}).get('resources', [])
                        
                        for resource in resources:
                            if resource.get('format', '').upper() in ['JSON', 'CSV']:
                                # Scarica il resource
                                resource_url = resource.get('url')
                                if resource_url:
                                    try:
                                        res_data = requests.get(resource_url, timeout=60)
                                        if res_data.status_code == 200:
                                            # Parsing dati
                                            items = parse_anac_data(res_data, resource.get('format'))
                                            bandi.extend(items)
                                    except:
                                        pass
            except Exception as e:
                print(f"      ⚠️ ANAC dataset {dataset_id}: {str(e)[:50]}")
                
    except Exception as e:
        print(f"      ❌ Errore ANAC API: {str(e)[:50]}")
    
    return bandi


def parse_anac_data(response, format_type: str) -> List[Dict]:
    """Parse dei dati ANAC."""
    bandi = []
    
    try:
        if format_type.upper() == 'JSON':
            data = response.json()
            if isinstance(data, list):
                for item in data[:100]:  # Limita a 100 per performance
                    bando = extract_anac_bando(item)
                    if bando:
                        bandi.append(bando)
    except:
        pass
    
    return bandi


def extract_anac_bando(item: dict) -> Dict:
    """Estrae i campi da un record ANAC."""
    try:
        titolo = item.get('oggetto') or item.get('descrizione') or item.get('titolo', '')
        if not titolo:
            return None
            
        return {
            'titolo': titolo[:500],
            'ente': item.get('denominazione_sa') or item.get('stazione_appaltante') or 'ANAC',
            'tipo_ente': 'pubblica_amministrazione',
            'regione': item.get('regione') or 'Nazionale',
            'tipo_contributo': 'gara_appalto',
            'stato': 'aperto',
            'contributo_max': item.get('importo_aggiudicazione') or item.get('importo_base_asta') or 'Vedi bando',
            'percentuale': 'N/A',
            'scadenza': item.get('data_scadenza') or item.get('termine_presentazione') or 'Vedi bando',
            'descrizione': titolo,
            'beneficiari': 'Imprese',
            'url': item.get('url_bando') or 'https://dati.anticorruzione.it/',
            'fonte': 'ANAC',
            'hash_id': get_hash(titolo),
            'attivo': True
        }
    except:
        return None


def scrape_anac() -> List[Dict]:
    """Funzione principale per ANAC."""
    print("      → Interrogazione API ANAC...")
    return fetch_anac_gare()


if __name__ == '__main__':
    print("Test ANAC API...")
    risultati = scrape_anac()
    print(f"Trovati {len(risultati)} gare")
