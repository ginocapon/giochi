#!/usr/bin/env python3
"""RSS Feed ufficiali - BUR Regioni, MIMIT, Unioncamere."""

import requests
import hashlib
import xml.etree.ElementTree as ET
from typing import List, Dict
from datetime import datetime

def get_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:16]

# Feed RSS ufficiali verificati
RSS_FEEDS = [
    # BUR Regionali
    {'url': 'https://bur.regione.veneto.it/BurvServices/Pubblica/HomeConsultazione.aspx?rss=1', 'regione': 'Veneto', 'ente': 'BUR Veneto'},
    {'url': 'https://www.regione.lombardia.it/wps/portal/istituzionale/HP/rss/burl', 'regione': 'Lombardia', 'ente': 'BUR Lombardia'},
    {'url': 'https://bur.regione.emilia-romagna.it/rss', 'regione': 'Emilia-Romagna', 'ente': 'BUR Emilia-Romagna'},
    {'url': 'https://bur.regione.toscana.it/rss', 'regione': 'Toscana', 'ente': 'BUR Toscana'},
    {'url': 'https://bur.regione.piemonte.it/rss', 'regione': 'Piemonte', 'ente': 'BUR Piemonte'},
    {'url': 'https://bur.regione.lazio.it/rss', 'regione': 'Lazio', 'ente': 'BUR Lazio'},
    {'url': 'https://bur.regione.campania.it/rss', 'regione': 'Campania', 'ente': 'BUR Campania'},
    {'url': 'https://bur.regione.puglia.it/rss', 'regione': 'Puglia', 'ente': 'BUR Puglia'},
    {'url': 'https://bur.regione.sicilia.it/rss', 'regione': 'Sicilia', 'ente': 'BUR Sicilia'},
    {'url': 'https://bur.regione.fvg.it/rss', 'regione': 'Friuli Venezia Giulia', 'ente': 'BUR FVG'},
    
    # Portali nazionali
    {'url': 'https://www.mimit.gov.it/it/rss/incentivi', 'regione': 'Nazionale', 'ente': 'MIMIT'},
    {'url': 'https://www.invitalia.it/rss/bandi', 'regione': 'Nazionale', 'ente': 'Invitalia'},
    {'url': 'https://incentivi.gov.it/rss', 'regione': 'Nazionale', 'ente': 'Incentivi.gov.it'},
]

# Keyword per filtrare solo bandi/contributi
KEYWORDS_BANDI = [
    'bando', 'contribut', 'finanziam', 'incentiv', 'agevolaz',
    'voucher', 'fondo perduto', 'credito', 'sostegno', 'bonus',
    'pmi', 'imprese', 'startup', 'innovaz', 'digital'
]


def is_bando_relevant(title: str, description: str = '') -> bool:
    """Verifica se il contenuto è un bando rilevante."""
    text = (title + ' ' + description).lower()
    return any(kw in text for kw in KEYWORDS_BANDI)


def parse_rss_feed(feed_info: Dict) -> List[Dict]:
    """Parsing singolo feed RSS."""
    bandi = []
    try:
        response = requests.get(feed_info['url'], timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; BandiBot/1.0)'
        })
        
        if response.status_code != 200:
            return []
        
        root = ET.fromstring(response.content)
        
        # Cerca items in vari formati RSS/Atom
        items = root.findall('.//item') or root.findall('.//{http://www.w3.org/2005/Atom}entry')
        
        for item in items[:20]:  # Max 20 per feed
            # Estrai titolo
            title_elem = item.find('title') or item.find('{http://www.w3.org/2005/Atom}title')
            title = title_elem.text if title_elem is not None and title_elem.text else ''
            
            # Estrai descrizione
            desc_elem = item.find('description') or item.find('{http://www.w3.org/2005/Atom}summary')
            description = desc_elem.text if desc_elem is not None and desc_elem.text else ''
            
            # Estrai link
            link_elem = item.find('link') or item.find('{http://www.w3.org/2005/Atom}link')
            if link_elem is not None:
                url = link_elem.get('href') or link_elem.text or ''
            else:
                url = ''
            
            # Filtra solo bandi rilevanti
            if title and is_bando_relevant(title, description):
                bando = {
                    'titolo': title[:500],
                    'ente': feed_info['ente'],
                    'tipo_ente': 'regione' if 'BUR' in feed_info['ente'] else 'ente_nazionale',
                    'regione': feed_info['regione'],
                    'tipo_contributo': 'misto',
                    'stato': 'aperto',
                    'contributo_max': 'Vedi bando',
                    'percentuale': 'Vedi bando',
                    'scadenza': 'Vedi bando',
                    'descrizione': description[:1000] if description else title,
                    'beneficiari': 'Vedi bando',
                    'url': url,
                    'fonte': f'RSS {feed_info["ente"]}',
                    'hash_id': get_hash(title),
                    'attivo': True
                }
                bandi.append(bando)
                
    except Exception as e:
        print(f"        ⚠ Errore feed {feed_info['ente']}: {str(e)[:50]}")
    
    return bandi


def scrape_rss_ufficiali() -> List[Dict]:
    """Scarica bandi da tutti i feed RSS ufficiali."""
    print("      → Scanning RSS ufficiali (BUR, MIMIT, Invitalia)...")
    
    all_bandi = []
    feeds_ok = 0
    
    for feed in RSS_FEEDS:
        bandi = parse_rss_feed(feed)
        if bandi:
            feeds_ok += 1
            all_bandi.extend(bandi)
            print(f"        ✓ {feed['ente']}: {len(bandi)} bandi")
    
    print(f"      → Feed attivi: {feeds_ok}/{len(RSS_FEEDS)}, Bandi trovati: {len(all_bandi)}")
    
    return all_bandi
