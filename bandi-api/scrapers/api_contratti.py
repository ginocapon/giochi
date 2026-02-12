#!/usr/bin/env python3
"""
===== CONTRATTI PUBBLICI - DEVELOPERS ITALIA =====
API ufficiale per bandi e gare pubbliche.
https://developers.italia.it/
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
import hashlib


def get_hash(text: str) -> str:
    """Genera hash per deduplicazione."""
    return hashlib.md5(text.encode()).hexdigest()[:16]


# Feed RSS ufficiali bandi pubblici
RSS_FEEDS = [
    {
        'url': 'https://www.serviziocontrattipubblici.it/SPInApp/rss.xml',
        'nome': 'Servizio Contratti Pubblici',
        'tipo': 'gara_appalto'
    },
    {
        'url': 'https://ted.europa.eu/api/v2.0/notices/search?scope=3&fields=ND,TI,CY,DD&pageSize=100&sortField=ND&sortOrder=desc',
        'nome': 'TED Europa',
        'tipo': 'gara_appalto_ue'
    }
]


def fetch_rss_feed(feed_config: dict) -> List[Dict]:
    """Recupera bandi da un feed RSS."""
    bandi = []
    
    try:
        response = requests.get(feed_config['url'], timeout=30)
        if response.status_code == 200:
            # Parsing XML
            root = ET.fromstring(response.content)
            
            # Cerca items nel feed
            for item in root.findall('.//item')[:50]:
                bando = parse_rss_item(item, feed_config)
                if bando:
                    bandi.append(bando)
                    
            # Formato Atom
            for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry')[:50]:
                bando = parse_atom_entry(entry, feed_config)
                if bando:
                    bandi.append(bando)
                    
    except Exception as e:
        print(f"      ⚠️ RSS {feed_config['nome']}: {str(e)[:50]}")
    
    return bandi


def parse_rss_item(item, feed_config: dict) -> Dict:
    """Parse di un item RSS."""
    try:
        titolo = item.findtext('title', '')
        if not titolo:
            return None
            
        return {
            'titolo': titolo[:500],
            'ente': feed_config['nome'],
            'tipo_ente': 'pubblica_amministrazione',
            'regione': 'Nazionale',
            'tipo_contributo': feed_config['tipo'],
            'stato': 'aperto',
            'contributo_max': 'Vedi bando',
            'percentuale': 'N/A',
            'scadenza': item.findtext('pubDate', 'Vedi bando'),
            'descrizione': item.findtext('description', titolo)[:1000],
            'beneficiari': 'Imprese',
            'url': item.findtext('link', ''),
            'fonte': feed_config['nome'],
            'hash_id': get_hash(titolo),
            'attivo': True
        }
    except:
        return None


def parse_atom_entry(entry, feed_config: dict) -> Dict:
    """Parse di un entry Atom."""
    try:
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        titolo = entry.findtext('atom:title', '', ns) or entry.findtext('title', '')
        if not titolo:
            return None
            
        link_elem = entry.find('atom:link', ns) or entry.find('link')
        link = link_elem.get('href', '') if link_elem is not None else ''
            
        return {
            'titolo': titolo[:500],
            'ente': feed_config['nome'],
            'tipo_ente': 'pubblica_amministrazione',
            'regione': 'Nazionale',
            'tipo_contributo': feed_config['tipo'],
            'stato': 'aperto',
            'contributo_max': 'Vedi bando',
            'percentuale': 'N/A',
            'scadenza': entry.findtext('atom:updated', '', ns) or 'Vedi bando',
            'descrizione': entry.findtext('atom:summary', '', ns) or titolo,
            'beneficiari': 'Imprese',
            'url': link,
            'fonte': feed_config['nome'],
            'hash_id': get_hash(titolo),
            'attivo': True
        }
    except:
        return None


def scrape_contratti_pubblici() -> List[Dict]:
    """Funzione principale per Contratti Pubblici."""
    bandi = []
    
    for feed in RSS_FEEDS:
        print(f"      → {feed['nome']}...")
        risultati = fetch_rss_feed(feed)
        bandi.extend(risultati)
        print(f"        Trovati: {len(risultati)}")
    
    return bandi


if __name__ == '__main__':
    print("Test Contratti Pubblici...")
    risultati = scrape_contratti_pubblici()
    print(f"Totale: {len(risultati)} bandi")
