#!/usr/bin/env python3
"""
===== RSS FEEDS REGIONALI E INCENTIVI =====
Feed RSS ufficiali di Regioni, MIMIT, Invitalia, etc.
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
import hashlib
import re


def get_hash(text: str) -> str:
    """Genera hash per deduplicazione."""
    return hashlib.md5(text.encode()).hexdigest()[:16]


# Feed RSS ufficiali
RSS_SOURCES = [
    # === MINISTERI ===
    {
        'url': 'https://www.mimit.gov.it/it/rss/notizie.xml',
        'nome': 'MIMIT',
        'tipo_ente': 'ministero',
        'regione': 'Nazionale',
        'tipo': 'incentivo'
    },
    
    # === INVITALIA ===
    {
        'url': 'https://www.invitalia.it/rss.xml',
        'nome': 'Invitalia',
        'tipo_ente': 'ente_nazionale',
        'regione': 'Nazionale',
        'tipo': 'incentivo'
    },
    
    # === REGIONI ===
    {
        'url': 'https://www.regione.veneto.it/web/bandi/-/rss',
        'nome': 'Regione Veneto',
        'tipo_ente': 'regione',
        'regione': 'Veneto',
        'tipo': 'bando_regionale'
    },
    {
        'url': 'https://www.regione.lombardia.it/wps/portal/istituzionale/HP/!ut/p/z1/rss',
        'nome': 'Regione Lombardia',
        'tipo_ente': 'regione',
        'regione': 'Lombardia',
        'tipo': 'bando_regionale'
    },
    {
        'url': 'https://www.regione.piemonte.it/web/rss',
        'nome': 'Regione Piemonte',
        'tipo_ente': 'regione',
        'regione': 'Piemonte',
        'tipo': 'bando_regionale'
    },
    {
        'url': 'https://www.regione.emilia-romagna.it/rss',
        'nome': 'Regione Emilia-Romagna',
        'tipo_ente': 'regione',
        'regione': 'Emilia-Romagna',
        'tipo': 'bando_regionale'
    },
    {
        'url': 'https://www.regione.toscana.it/rss',
        'nome': 'Regione Toscana',
        'tipo_ente': 'regione',
        'regione': 'Toscana',
        'tipo': 'bando_regionale'
    },
    {
        'url': 'https://www.regione.fvg.it/rafvg/cms/RAFVG/rss/',
        'nome': 'Regione FVG',
        'tipo_ente': 'regione',
        'regione': 'Friuli Venezia Giulia',
        'tipo': 'bando_regionale'
    },
    {
        'url': 'https://www.regione.lazio.it/rss',
        'nome': 'Regione Lazio',
        'tipo_ente': 'regione',
        'regione': 'Lazio',
        'tipo': 'bando_regionale'
    },
    {
        'url': 'https://www.regione.campania.it/rss',
        'nome': 'Regione Campania',
        'tipo_ente': 'regione',
        'regione': 'Campania',
        'tipo': 'bando_regionale'
    },
    {
        'url': 'https://www.regione.puglia.it/rss',
        'nome': 'Regione Puglia',
        'tipo_ente': 'regione',
        'regione': 'Puglia',
        'tipo': 'bando_regionale'
    },
    {
        'url': 'https://www.regione.sicilia.it/rss',
        'nome': 'Regione Sicilia',
        'tipo_ente': 'regione',
        'regione': 'Sicilia',
        'tipo': 'bando_regionale'
    },
    
    # === CAMERE DI COMMERCIO ===
    {
        'url': 'https://www.unioncamere.gov.it/rss',
        'nome': 'Unioncamere',
        'tipo_ente': 'cciaa',
        'regione': 'Nazionale',
        'tipo': 'voucher'
    },
]


def is_bando_related(text: str) -> bool:
    """Verifica se il testo è relativo a bandi/finanziamenti."""
    keywords = [
        'bando', 'finanziament', 'contribut', 'incentiv', 'agevolazion',
        'fondo perduto', 'voucher', 'bonus', 'credito', 'imposta',
        'pnrr', 'fesr', 'fse', 'startup', 'innovazione', 'digital',
        'imprese', 'pmi', 'appalto', 'gara', 'avviso pubblico'
    ]
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)


def extract_importo(text: str) -> str:
    """Estrae l'importo dal testo."""
    patterns = [
        r'€\s*[\d.,]+(?:\s*(?:milioni|mila|k|m))?',
        r'[\d.,]+\s*(?:euro|€)',
        r'importo[:\s]+[\d.,]+',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return 'Vedi bando'


def extract_scadenza(text: str) -> str:
    """Estrae la scadenza dal testo."""
    patterns = [
        r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
        r'\d{1,2}\s+(?:gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s+\d{4}',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return 'Vedi bando'


def fetch_rss_feed(source: dict) -> List[Dict]:
    """Recupera bandi da un feed RSS."""
    bandi = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; BandiBot/1.0)'
        }
        response = requests.get(source['url'], timeout=15, headers=headers)
        
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                
                # Parsing RSS 2.0
                for item in root.findall('.//item')[:30]:
                    titolo = item.findtext('title', '')
                    descrizione = item.findtext('description', '')
                    
                    # Filtra solo contenuti relativi a bandi
                    if titolo and is_bando_related(titolo + ' ' + descrizione):
                        bando = {
                            'titolo': titolo[:500],
                            'ente': source['nome'],
                            'tipo_ente': source['tipo_ente'],
                            'regione': source['regione'],
                            'tipo_contributo': source['tipo'],
                            'stato': 'aperto',
                            'contributo_max': extract_importo(descrizione),
                            'percentuale': 'Vedi bando',
                            'scadenza': extract_scadenza(descrizione) or item.findtext('pubDate', 'Vedi bando'),
                            'descrizione': descrizione[:1000] if descrizione else titolo,
                            'beneficiari': 'PMI, Imprese',
                            'url': item.findtext('link', source['url']),
                            'fonte': source['nome'],
                            'hash_id': get_hash(titolo),
                            'attivo': True
                        }
                        bandi.append(bando)
                        
            except ET.ParseError:
                pass
                
    except requests.exceptions.RequestException as e:
        # Silenzioso per feed non disponibili
        pass
    
    return bandi


def scrape_rss_feeds() -> List[Dict]:
    """Funzione principale per RSS feeds."""
    bandi = []
    
    for source in RSS_SOURCES:
        print(f"      → {source['nome']}...")
        risultati = fetch_rss_feed(source)
        if risultati:
            bandi.extend(risultati)
            print(f"        ✓ {len(risultati)} bandi")
        else:
            print(f"        - Nessun bando trovato")
    
    return bandi


if __name__ == '__main__':
    print("Test RSS Feeds...")
    risultati = scrape_rss_feeds()
    print(f"\nTotale: {len(risultati)} bandi")
