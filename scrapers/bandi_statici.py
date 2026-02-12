#!/usr/bin/env python3
"""Bandi nazionali sempre attivi."""

from typing import List, Dict
import hashlib

def get_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:16]

BANDI_NAZIONALI = [
    {
        'titolo': 'Nuova Sabatini 2025',
        'ente': 'MIMIT',
        'tipo_ente': 'ministero',
        'regione': 'Nazionale',
        'tipo_contributo': 'tasso_agevolato',
        'contributo_max': '€4.000.000',
        'percentuale': '100%',
        'scadenza': '31/12/2025',
        'descrizione': 'Finanziamento agevolato per acquisto macchinari, impianti, attrezzature e tecnologie digitali 4.0',
        'beneficiari': 'PMI tutti i settori',
        'url': 'https://www.mimit.gov.it/it/incentivi/nuova-sabatini'
    },
    {
        'titolo': 'Transizione 5.0',
        'ente': 'MIMIT',
        'tipo_ente': 'ministero',
        'regione': 'Nazionale',
        'tipo_contributo': 'credito_imposta',
        'contributo_max': '€50.000.000',
        'percentuale': '45%',
        'scadenza': '31/12/2025',
        'descrizione': 'Credito imposta per investimenti in transizione digitale ed energetica',
        'beneficiari': 'Tutte le imprese',
        'url': 'https://www.mimit.gov.it/it/incentivi/transizione-50'
    },
    {
        'titolo': 'Smart&Start Italia',
        'ente': 'Invitalia',
        'tipo_ente': 'ente_nazionale',
        'regione': 'Nazionale',
        'tipo_contributo': 'misto',
        'contributo_max': '€1.500.000',
        'percentuale': '80%',
        'scadenza': 'Sempre aperto',
        'descrizione': 'Finanziamento a tasso zero per startup innovative',
        'beneficiari': 'Startup innovative',
        'url': 'https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/smartstart-italia'
    },
    {
        'titolo': 'Resto al Sud',
        'ente': 'Invitalia',
        'tipo_ente': 'ente_nazionale',
        'regione': 'Sud Italia',
        'tipo_contributo': 'misto',
        'contributo_max': '€200.000',
        'percentuale': '50% fondo perduto',
        'scadenza': 'Sempre aperto',
        'descrizione': 'Incentivi per nuove attività imprenditoriali nel Mezzogiorno',
        'beneficiari': 'Under 56 residenti Sud Italia',
        'url': 'https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/resto-al-sud'
    },
    {
        'titolo': 'ON - Nuove Imprese a Tasso Zero',
        'ente': 'Invitalia',
        'tipo_ente': 'ente_nazionale',
        'regione': 'Nazionale',
        'tipo_contributo': 'misto',
        'contributo_max': '€3.000.000',
        'percentuale': '90%',
        'scadenza': 'Sempre aperto',
        'descrizione': 'Finanziamenti a tasso zero per giovani e donne',
        'beneficiari': 'Under 35 e donne',
        'url': 'https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/nuove-imprese-a-tasso-zero'
    },
    {
        'titolo': 'Fondo Impresa Donna',
        'ente': 'Invitalia',
        'tipo_ente': 'ente_nazionale',
        'regione': 'Nazionale',
        'tipo_contributo': 'misto',
        'contributo_max': '€400.000',
        'percentuale': '80%',
        'scadenza': 'Sempre aperto',
        'descrizione': 'Agevolazioni per imprenditoria femminile',
        'beneficiari': 'Imprese femminili',
        'url': 'https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/fondo-impresa-donna'
    },
    {
        'titolo': 'SIMEST Fondo 394 - Transizione Digitale',
        'ente': 'SIMEST',
        'tipo_ente': 'ente_nazionale',
        'regione': 'Nazionale',
        'tipo_contributo': 'tasso_agevolato',
        'contributo_max': '€300.000',
        'percentuale': '10% fondo perduto',
        'scadenza': 'Sempre aperto',
        'descrizione': 'Finanziamento agevolato per digitalizzazione PMI esportatrici',
        'beneficiari': 'PMI esportatrici',
        'url': 'https://www.simest.it/prodotti-e-servizi/finanziamenti-agevolati'
    },
    {
        'titolo': 'Bando ISI INAIL 2024',
        'ente': 'INAIL',
        'tipo_ente': 'ente_nazionale',
        'regione': 'Nazionale',
        'tipo_contributo': 'fondo_perduto',
        'contributo_max': '€130.000',
        'percentuale': '65%',
        'scadenza': '28/02/2025',
        'descrizione': 'Incentivi a fondo perduto per sicurezza sul lavoro',
        'beneficiari': 'Tutte le imprese',
        'url': 'https://www.inail.it/cs/internet/attivita/prevenzione-e-sicurezza/agevolazioni-e-finanziamenti/incentivi-alle-imprese/bando-isi.html'
    },
    {
        'titolo': 'ZES Unica Mezzogiorno',
        'ente': 'Agenzia Coesione',
        'tipo_ente': 'ente_nazionale',
        'regione': 'Sud Italia',
        'tipo_contributo': 'credito_imposta',
        'contributo_max': '€100.000.000',
        'percentuale': '60%',
        'scadenza': '31/12/2025',
        'descrizione': 'Credito imposta per investimenti nelle Zone Economiche Speciali',
        'beneficiari': 'Imprese ZES Mezzogiorno',
        'url': 'https://www.agenziacoesione.gov.it/zes-unica/'
    },
    {
        'titolo': 'Credito Imposta Ricerca e Sviluppo',
        'ente': 'MIMIT',
        'tipo_ente': 'ministero',
        'regione': 'Nazionale',
        'tipo_contributo': 'credito_imposta',
        'contributo_max': '€10.000.000',
        'percentuale': '20%',
        'scadenza': '31/12/2025',
        'descrizione': 'Credito imposta per ricerca e sviluppo sperimentale',
        'beneficiari': 'Tutte le imprese',
        'url': 'https://www.mimit.gov.it/it/incentivi/credito-dimposta-ricerca-e-sviluppo'
    },
]

def scrape_bandi_statici() -> List[Dict]:
    print("      → Caricamento bandi nazionali garantiti...")
    bandi = []
    for bando_info in BANDI_NAZIONALI:
        bando = {
            **bando_info,
            'stato': 'aperto',
            'fonte': bando_info['ente'],
            'hash_id': get_hash(bando_info['titolo']),
            'attivo': True
        }
        bandi.append(bando)
    print(f"        ✓ {len(bandi)} bandi caricati")
    return bandi
