#!/usr/bin/env python3
"""RSS Feeds regionali e nazionali."""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
import hashlib
import re

def get_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:16]

RSS_SOURCES = [
    {'url': 'https://www.mimit.gov.it/it/rss/notizie.xml', 'nome': 'MIMIT', 'tipo_ente': 'ministero', 'regione': 'Nazionale'},
    {'url': 'https://www.regione.veneto.it/web/bandi/-/rss', 'nome': 'Regione Veneto', 'tipo_ente': 'regione', 'regione': 'Veneto'},
    {'url': 'https://www.regione.lombardia.it/wps/portal/istituzionale/HP/rss', 'nome': 'Regione Lombardia', 'tipo_ente': 'regione', 'regione': 'Lombardia'},
    {'url': 'https://www.regione.piemonte.it/web/rss', 'nome': 'Regione Piemonte', 'tipo_ente': 'regione', 'regione': 'Piemonte'},
    {'url': 'https://www.regione.emilia-romagna.it/rss', 'nome': 'Regione Emilia-Romagna', 'tipo_ente': 'regione', 'regione': 'Emilia-Romagna'},
    {'url': 'https://www.regione.toscana.it/rss', 'nome': 'Regione Toscana', 'tipo_ente': 'regione', 'regione': 'Toscana'},
    {'url': 'https://www.regione.lazio.it/rss', 'nome': 'Regione Lazio', 'tipo_ente': 'regione', 'regione': 'Lazio'},
    {'url': 'https://www.regione.campania.it/rss', 'nome': 'Regione Campania', 'tipo_ente': 'regione', 'regione': 'Campania'},
    {'url': 'https://www.regione.puglia.it/rss', 'nome': 'Regione Puglia', 'tipo_ente': 'regione', 'regione': 'Puglia'},
    {'url': 'https://www.regione.sicilia.it/rss', 'nome': 'Regione Sicilia', 'tipo_ente': 'regione', 'regione': 'Sicilia'},
]

def is_bando_related(text: str) -> bool:
    keywords = ['bando', 'finanziament', 'contribut', 'incentiv', 'agevolazion',
                'fondo perduto', 'voucher', 'bonus', 'credito', 'imposta',
                'pnrr', 'fesr', 'startup', 'innovazione', 'imprese', 'pmi']
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)

def fetch_rss_feed(source: dict) -> List[Dict]:
    bandi = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; BandiBot/1.0)'}
        response = requests.get(source['url'], timeout=15, headers=headers)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall('.//item')[:30]:
                titolo = item.findtext('title', '')
                descrizione = item.findtext('description', '')
                if titolo and is_bando_related(titolo + ' ' + descrizione):
                    bando = {
                        'titolo': titolo[:500],
                        'ente': source['nome'],
                        'tipo_ente': source['tipo_ente'],
                        'regione': source['regione'],
                        'tipo_contributo': 'bando_regionale',
                        'stato': 'aperto',
                        'contributo_max': 'Vedi bando',
                        'percentuale': 'Vedi bando',
                        'scadenza': item.findtext('pubDate', 'Vedi bando'),
                        'descrizione': descrizione[:1000] if descrizione else titolo,
                        'beneficiari': 'PMI, Imprese',
                        'url': item.findtext('link', source['url']),
                        'fonte': source['nome'],
                        'hash_id': get_hash(titolo),
                        'attivo': True
                    }
                    bandi.append(bando)
    except:
        pass
    return bandi

def scrape_rss_feeds() -> List[Dict]:
    bandi = []
    for source in RSS_SOURCES:
        print(f"      → {source['nome']}...")
        risultati = fetch_rss_feed(source)
        if risultati:
            bandi.extend(risultati)
            print(f"        ✓ {len(risultati)} bandi")
        else:
            print(f"        - Nessun bando")
    return bandi
