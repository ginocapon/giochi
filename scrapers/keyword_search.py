#!/usr/bin/env python3
"""
KEYWORD SEARCH INTELLIGENTE
Cerca bandi combinando keyword per regione, settore, beneficiari, etc.
"""

import requests
import hashlib
from typing import List, Dict
from itertools import product
import time

def get_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:16]

# === KEYWORD DATABASE ===

REGIONI = [
    "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna",
    "Friuli-Venezia-Giulia", "Lazio", "Liguria", "Lombardia", "Marche",
    "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana",
    "Trentino-Alto-Adige", "Umbria", "Valle d'Aosta", "Veneto", "Nazionale"
]

BENEFICIARI = [
    "PMI", "Micro impresa", "Grande Impresa", "Startup", "Cooperativa",
    "Libero professionista", "Ente pubblico", "Associazione", "Non profit",
    "Impresa sociale", "Centro ricerca", "Ente formazione", "Consorzio",
    "Aspirante imprenditore", "Persona fisica"
]

SETTORI = [
    "Agricoltura", "Agroalimentare", "Artigianato", "Commercio", "Cultura",
    "Industria", "Servizi", "Turismo", "Manifatturiero", "Tecnologia",
    "Green", "Sociale", "Sanitario", "Edilizia", "Trasporti"
]

TIPI_AGEVOLAZIONE = [
    "fondo perduto", "tasso agevolato", "tasso zero", "credito imposta",
    "bonus fiscale", "garanzia", "voucher", "contributo", "finanziamento"
]

SPESE_FINANZIATE = [
    "digitalizzazione", "macchinari", "attrezzature", "innovazione",
    "ricerca sviluppo", "formazione", "assunzioni", "personale",
    "internazionalizzazione", "export", "fiere", "marketing",
    "brevetti", "marchi", "consulenze", "software", "hardware",
    "risparmio energetico", "efficienza energetica", "sostenibilità",
    "avvio attività", "startup", "opere edili", "impianti"
]

KEYWORDS_BASE = [
    "bando", "contributo", "finanziamento", "incentivo", "agevolazione",
    "voucher", "bonus", "fondo perduto", "credito imposta"
]

# === FONTI UFFICIALI DA CERCARE ===

FONTI_RICERCA = [
    {
        'nome': 'Google CSE Italia',
        'url': 'https://www.googleapis.com/customsearch/v1',
        'tipo': 'api'
    }
]

# === RSS FEEDS PER REGIONE ===

RSS_REGIONALI = {
    'Abruzzo': 'https://www.regione.abruzzo.it/rss',
    'Basilicata': 'https://www.regione.basilicata.it/rss',
    'Calabria': 'https://www.regione.calabria.it/rss',
    'Campania': 'https://www.regione.campania.it/rss',
    'Emilia-Romagna': 'https://www.regione.emilia-romagna.it/rss',
    'Friuli-Venezia-Giulia': 'https://www.regione.fvg.it/rss',
    'Lazio': 'https://www.regione.lazio.it/rss',
    'Liguria': 'https://www.regione.liguria.it/rss',
    'Lombardia': 'https://www.regione.lombardia.it/rss',
    'Marche': 'https://www.regione.marche.it/rss',
    'Molise': 'https://www.regione.molise.it/rss',
    'Piemonte': 'https://www.regione.piemonte.it/rss',
    'Puglia': 'https://www.regione.puglia.it/rss',
    'Sardegna': 'https://www.regione.sardegna.it/rss',
    'Sicilia': 'https://www.regione.sicilia.it/rss',
    'Toscana': 'https://www.regione.toscana.it/rss',
    'Trentino-Alto-Adige': 'https://www.regione.taa.it/rss',
    'Umbria': 'https://www.regione.umbria.it/rss',
    'Valle d\'Aosta': 'https://www.regione.vda.it/rss',
    'Veneto': 'https://www.regione.veneto.it/rss',
}


def genera_query_ricerca() -> List[Dict]:
    """
    Genera combinazioni intelligenti di keyword per la ricerca.
    Non genera TUTTE le combinazioni (sarebbero troppe), ma quelle più rilevanti.
    """
    queries = []
    
    # Query per regione + tipo agevolazione
    for regione in REGIONI[:10]:  # Prime 10 regioni più attive
        for tipo in TIPI_AGEVOLAZIONE[:5]:
            queries.append({
                'query': f"bando {tipo} {regione} 2025",
                'regione': regione,
                'tipo': tipo
            })
    
    # Query per settore + beneficiario
    for settore in SETTORI[:8]:
        for beneficiario in BENEFICIARI[:5]:
            queries.append({
                'query': f"bando {settore} {beneficiario} 2025",
                'settore': settore,
                'beneficiario': beneficiario
            })
    
    # Query per spese finanziate
    for spesa in SPESE_FINANZIATE[:10]:
        queries.append({
            'query': f"contributo {spesa} imprese 2025",
            'spesa': spesa
        })
    
    # Query specifiche nazionali
    queries_nazionali = [
        "bando PNRR imprese 2025",
        "bando FESR 2021-2027",
        "incentivi transizione 5.0",
        "bando digitalizzazione PMI",
        "contributi startup innovative",
        "finanziamenti imprenditoria femminile",
        "bando giovani imprenditori",
        "incentivi green economia circolare",
        "bando export internazionalizzazione",
        "contributi agricoltura 2025",
        "bando turismo 2025",
        "incentivi efficienza energetica imprese",
        "bando artigianato 2025",
        "finanziamenti ricerca sviluppo",
        "bando commercio dettaglio",
    ]
    
    for q in queries_nazionali:
        queries.append({'query': q, 'regione': 'Nazionale'})
    
    return queries


def search_duckduckgo(query: str) -> List[Dict]:
    """
    Cerca su DuckDuckGo (gratuito, no API key).
    """
    bandi = []
    
    try:
        # DuckDuckGo Instant Answer API
        url = "https://api.duckduckgo.com/"
        params = {
            'q': query,
            'format': 'json',
            'no_html': 1,
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Risultati correlati
            for result in data.get('RelatedTopics', [])[:5]:
                if isinstance(result, dict) and 'Text' in result:
                    text = result.get('Text', '')
                    url = result.get('FirstURL', '')
                    
                    if any(kw in text.lower() for kw in ['bando', 'contribut', 'finanziam', 'incentiv']):
                        bandi.append({
                            'titolo': text[:200],
                            'url': url,
                            'fonte': 'DuckDuckGo'
                        })
    except:
        pass
    
    return bandi


def cerca_bandi_keyword() -> List[Dict]:
    """
    Funzione principale: cerca bandi usando le keyword intelligenti.
    """
    print("      🔍 Generazione query di ricerca...")
    queries = genera_query_ricerca()
    print(f"      📋 Generate {len(queries)} query")
    
    all_bandi = []
    
    # Limita le ricerche per non sovraccaricare
    max_searches = 20
    
    print(f"      🌐 Ricerca in corso (max {max_searches} query)...")
    
    for i, q in enumerate(queries[:max_searches]):
        try:
            results = search_duckduckgo(q['query'])
            
            for r in results:
                bando = {
                    'titolo': r['titolo'][:500],
                    'ente': 'Da verificare',
                    'tipo_ente': 'altro',
                    'regione': q.get('regione', 'Nazionale'),
                    'tipo_contributo': q.get('tipo', 'misto'),
                    'stato': 'aperto',
                    'contributo_max': 'Vedi bando',
                    'percentuale': 'Vedi bando',
                    'scadenza': 'Vedi bando',
                    'descrizione': r['titolo'],
                    'beneficiari': q.get('beneficiario', 'Imprese'),
                    'url': r.get('url', ''),
                    'fonte': 'Keyword Search',
                    'hash_id': get_hash(r['titolo']),
                    'attivo': True
                }
                all_bandi.append(bando)
            
            # Pausa per non sovraccaricare
            time.sleep(0.5)
            
        except Exception as e:
            pass
    
    print(f"      ✓ Trovati {len(all_bandi)} potenziali bandi")
    
    return all_bandi


def get_keyword_stats() -> Dict:
    """Restituisce statistiche sulle keyword disponibili."""
    return {
        'regioni': len(REGIONI),
        'beneficiari': len(BENEFICIARI),
        'settori': len(SETTORI),
        'tipi_agevolazione': len(TIPI_AGEVOLAZIONE),
        'spese_finanziate': len(SPESE_FINANZIATE),
        'combinazioni_possibili': len(REGIONI) * len(SETTORI) * len(BENEFICIARI)
    }


if __name__ == '__main__':
    print("Test Keyword Search...")
    stats = get_keyword_stats()
    print(f"Keyword disponibili: {stats}")
    
    bandi = cerca_bandi_keyword()
    print(f"\nTrovati {len(bandi)} bandi")
