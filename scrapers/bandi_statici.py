#!/usr/bin/env python3
"""Bandi nazionali e regionali - Database completo."""

from typing import List, Dict
import hashlib

def get_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:16]

BANDI_COMPLETI = [
    # ========== MIMIT - MINISTERO ==========
    {'titolo': 'Nuova Sabatini 2025', 'ente': 'MIMIT', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'tasso_agevolato', 'contributo_max': '€4.000.000', 'percentuale': '100%', 'scadenza': '31/12/2025', 'descrizione': 'Finanziamento agevolato per acquisto macchinari, impianti e tecnologie 4.0', 'beneficiari': 'PMI', 'url': 'https://www.mimit.gov.it/it/incentivi/nuova-sabatini'},
    {'titolo': 'Transizione 5.0', 'ente': 'MIMIT', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'credito_imposta', 'contributo_max': '€50.000.000', 'percentuale': '45%', 'scadenza': '31/12/2025', 'descrizione': 'Credito imposta per transizione digitale ed energetica', 'beneficiari': 'Tutte le imprese', 'url': 'https://www.mimit.gov.it/it/incentivi/transizione-50'},
    {'titolo': 'Credito Imposta Ricerca e Sviluppo', 'ente': 'MIMIT', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'credito_imposta', 'contributo_max': '€10.000.000', 'percentuale': '20%', 'scadenza': '31/12/2025', 'descrizione': 'Credito imposta per ricerca e sviluppo', 'beneficiari': 'Tutte le imprese', 'url': 'https://www.mimit.gov.it/it/incentivi/credito-dimposta-ricerca-e-sviluppo'},
    {'titolo': 'Patent Box', 'ente': 'MIMIT', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'credito_imposta', 'contributo_max': 'Variabile', 'percentuale': '110%', 'scadenza': 'Sempre aperto', 'descrizione': 'Super deduzione 110% costi R&S per brevetti e software', 'beneficiari': 'Tutte le imprese', 'url': 'https://www.mimit.gov.it/it/incentivi/patent-box'},
    {'titolo': 'Voucher 3I - Investire in Innovazione', 'ente': 'MIMIT', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'voucher', 'contributo_max': '€10.000', 'percentuale': '80%', 'scadenza': '31/12/2025', 'descrizione': 'Voucher per brevetti e marchi startup e PMI innovative', 'beneficiari': 'Startup e PMI innovative', 'url': 'https://www.mimit.gov.it/it/incentivi/voucher-3i'},
    {'titolo': 'Fondo Crescita Sostenibile - Accordi Innovazione', 'ente': 'MIMIT', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'misto', 'contributo_max': '€20.000.000', 'percentuale': '50%', 'scadenza': 'A sportello', 'descrizione': 'Progetti R&S in collaborazione con organismi di ricerca', 'beneficiari': 'Imprese e centri ricerca', 'url': 'https://www.mimit.gov.it/it/incentivi/fondo-crescita-sostenibile'},
    {'titolo': 'Contratti di Sviluppo', 'ente': 'MIMIT', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'misto', 'contributo_max': '€50.000.000', 'percentuale': '75%', 'scadenza': 'A sportello', 'descrizione': 'Grandi investimenti industriali, turistici e ambientali', 'beneficiari': 'Grandi imprese e PMI', 'url': 'https://www.mimit.gov.it/it/incentivi/contratti-di-sviluppo'},
    {'titolo': 'Mini Contratti di Sviluppo', 'ente': 'MIMIT', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'misto', 'contributo_max': '€20.000.000', 'percentuale': '60%', 'scadenza': 'A sportello', 'descrizione': 'Investimenti produttivi tra 5 e 20 milioni', 'beneficiari': 'PMI', 'url': 'https://www.mimit.gov.it/it/incentivi/mini-contratti-sviluppo'},
    
    # ========== INVITALIA ==========
    {'titolo': 'Smart&Start Italia', 'ente': 'Invitalia', 'tipo_ente': 'ente_nazionale', 'regione': 'Nazionale', 'tipo_contributo': 'misto', 'contributo_max': '€1.500.000', 'percentuale': '80%', 'scadenza': 'Sempre aperto', 'descrizione': 'Finanziamento a tasso zero per startup innovative', 'beneficiari': 'Startup innovative', 'url': 'https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/smartstart-italia'},
    {'titolo': 'Resto al Sud 2025', 'ente': 'Invitalia', 'tipo_ente': 'ente_nazionale', 'regione': 'Sud Italia', 'tipo_contributo': 'misto', 'contributo_max': '€200.000', 'percentuale': '50%', 'scadenza': 'Sempre aperto', 'descrizione': 'Incentivi per nuove attività nel Mezzogiorno', 'beneficiari': 'Under 56 Sud Italia', 'url': 'https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/resto-al-sud'},
    {'titolo': 'ON - Oltre Nuove Imprese a Tasso Zero', 'ente': 'Invitalia', 'tipo_ente': 'ente_nazionale', 'regione': 'Nazionale', 'tipo_contributo': 'misto', 'contributo_max': '€3.000.000', 'percentuale': '90%', 'scadenza': 'Sempre aperto', 'descrizione': 'Finanziamenti a tasso zero per giovani e donne', 'beneficiari': 'Under 35 e donne', 'url': 'https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/nuove-imprese-a-tasso-zero'},
    {'titolo': 'Cultura Crea 2.0', 'ente': 'Invitalia', 'tipo_ente': 'ente_nazionale', 'regione': 'Sud Italia', 'tipo_contributo': 'misto', 'contributo_max': '€400.000', 'percentuale': '80%', 'scadenza': 'Sempre aperto', 'descrizione': 'Incentivi per imprese culturali e creative', 'beneficiari': 'Imprese culturali', 'url': 'https://www.invitalia.it/cosa-facciamo/rafforziamo-le-imprese/cultura-crea'},
    {'titolo': 'Fondo Impresa Donna', 'ente': 'Invitalia', 'tipo_ente': 'ente_nazionale', 'regione': 'Nazionale', 'tipo_contributo': 'misto', 'contributo_max': '€400.000', 'percentuale': '80%', 'scadenza': 'Sempre aperto', 'descrizione': 'Agevolazioni per imprenditoria femminile', 'beneficiari': 'Imprese femminili', 'url': 'https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/fondo-impresa-donna'},
    {'titolo': 'Selfiemployment', 'ente': 'Invitalia', 'tipo_ente': 'ente_nazionale', 'regione': 'Nazionale', 'tipo_contributo': 'tasso_zero', 'contributo_max': '€50.000', 'percentuale': '100%', 'scadenza': 'Sempre aperto', 'descrizione': 'Prestiti a tasso zero per NEET e disoccupati', 'beneficiari': 'NEET e disoccupati', 'url': 'https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/selfiemployment'},
    {'titolo': 'Autoimpiego Centro-Nord', 'ente': 'Invitalia', 'tipo_ente': 'ente_nazionale', 'regione': 'Centro-Nord', 'tipo_contributo': 'misto', 'contributo_max': '€200.000', 'percentuale': '65%', 'scadenza': 'Sempre aperto', 'descrizione': 'Incentivi per nuove imprese nel Centro-Nord', 'beneficiari': 'Under 35, donne, disoccupati', 'url': 'https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/autoimpiego'},
    
    # ========== SIMEST ==========
    {'titolo': 'SIMEST Fondo 394 - Transizione Digitale', 'ente': 'SIMEST', 'tipo_ente': 'ente_nazionale', 'regione': 'Nazionale', 'tipo_contributo': 'tasso_agevolato', 'contributo_max': '€300.000', 'percentuale': '10% fondo perduto', 'scadenza': 'Sempre aperto', 'descrizione': 'Digitalizzazione PMI esportatrici', 'beneficiari': 'PMI esportatrici', 'url': 'https://www.simest.it/'},
    {'titolo': 'SIMEST Fondo 394 - Fiere e Mostre', 'ente': 'SIMEST', 'tipo_ente': 'ente_nazionale', 'regione': 'Nazionale', 'tipo_contributo': 'tasso_agevolato', 'contributo_max': '€150.000', 'percentuale': '10% fondo perduto', 'scadenza': 'Sempre aperto', 'descrizione': 'Partecipazione fiere internazionali', 'beneficiari': 'PMI esportatrici', 'url': 'https://www.simest.it/'},
    {'titolo': 'SIMEST Fondo 394 - E-commerce', 'ente': 'SIMEST', 'tipo_ente': 'ente_nazionale', 'regione': 'Nazionale', 'tipo_contributo': 'tasso_agevolato', 'contributo_max': '€450.000', 'percentuale': '10% fondo perduto', 'scadenza': 'Sempre aperto', 'descrizione': 'Sviluppo e-commerce per export', 'beneficiari': 'PMI esportatrici', 'url': 'https://www.simest.it/'},
    {'titolo': 'SIMEST Fondo 394 - Temporary Manager', 'ente': 'SIMEST', 'tipo_ente': 'ente_nazionale', 'regione': 'Nazionale', 'tipo_contributo': 'tasso_agevolato', 'contributo_max': '€150.000', 'percentuale': '10% fondo perduto', 'scadenza': 'Sempre aperto', 'descrizione': 'Inserimento temporary export manager', 'beneficiari': 'PMI esportatrici', 'url': 'https://www.simest.it/'},
    {'titolo': 'SIMEST Fondo 394 - Certificazioni e Consulenze', 'ente': 'SIMEST', 'tipo_ente': 'ente_nazionale', 'regione': 'Nazionale', 'tipo_contributo': 'tasso_agevolato', 'contributo_max': '€100.000', 'percentuale': '10% fondo perduto', 'scadenza': 'Sempre aperto', 'descrizione': 'Certificazioni internazionali', 'beneficiari': 'PMI esportatrici', 'url': 'https://www.simest.it/'},
    
    # ========== INAIL ==========
    {'titolo': 'Bando ISI INAIL 2024', 'ente': 'INAIL', 'tipo_ente': 'ente_nazionale', 'regione': 'Nazionale', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€130.000', 'percentuale': '65%', 'scadenza': '28/02/2025', 'descrizione': 'Sicurezza sul lavoro', 'beneficiari': 'Tutte le imprese', 'url': 'https://www.inail.it/'},
    {'titolo': 'Bando ISI Agricoltura INAIL', 'ente': 'INAIL', 'tipo_ente': 'ente_nazionale', 'regione': 'Nazionale', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€60.000', 'percentuale': '65%', 'scadenza': '28/02/2025', 'descrizione': 'Sicurezza agricoltura', 'beneficiari': 'Imprese agricole', 'url': 'https://www.inail.it/'},
    
    # ========== AGENZIA COESIONE ==========
    {'titolo': 'ZES Unica Mezzogiorno', 'ente': 'Agenzia Coesione', 'tipo_ente': 'ente_nazionale', 'regione': 'Sud Italia', 'tipo_contributo': 'credito_imposta', 'contributo_max': '€100.000.000', 'percentuale': '60%', 'scadenza': '31/12/2025', 'descrizione': 'Credito imposta investimenti ZES', 'beneficiari': 'Imprese ZES', 'url': 'https://www.agenziacoesione.gov.it/'},
    {'titolo': 'Decontribuzione Sud', 'ente': 'INPS', 'tipo_ente': 'ente_nazionale', 'regione': 'Sud Italia', 'tipo_contributo': 'bonus_fiscale', 'contributo_max': 'Variabile', 'percentuale': '30%', 'scadenza': '31/12/2025', 'descrizione': 'Sgravio contributivo assunzioni Sud', 'beneficiari': 'Imprese Sud Italia', 'url': 'https://www.inps.it/'},
    
    # ========== REGIONE LOMBARDIA ==========
    {'titolo': 'Bando Digitalizzazione PMI Lombardia', 'ente': 'Regione Lombardia', 'tipo_ente': 'regione', 'regione': 'Lombardia', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€50.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Digitalizzazione imprese lombarde', 'beneficiari': 'PMI Lombardia', 'url': 'https://www.regione.lombardia.it/'},
    {'titolo': 'Bando Innovazione Lombardia', 'ente': 'Regione Lombardia', 'tipo_ente': 'regione', 'regione': 'Lombardia', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€100.000', 'percentuale': '40%', 'scadenza': 'Vedi bando', 'descrizione': 'Innovazione e R&S', 'beneficiari': 'PMI Lombardia', 'url': 'https://www.regione.lombardia.it/'},
    {'titolo': 'Bando Internazionalizzazione Lombardia', 'ente': 'Regione Lombardia', 'tipo_ente': 'regione', 'regione': 'Lombardia', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€30.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Export e fiere internazionali', 'beneficiari': 'PMI Lombardia', 'url': 'https://www.regione.lombardia.it/'},
    {'titolo': 'Bando Efficienza Energetica Lombardia', 'ente': 'Regione Lombardia', 'tipo_ente': 'regione', 'regione': 'Lombardia', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€80.000', 'percentuale': '40%', 'scadenza': 'Vedi bando', 'descrizione': 'Risparmio energetico imprese', 'beneficiari': 'PMI Lombardia', 'url': 'https://www.regione.lombardia.it/'},
    
    # ========== REGIONE VENETO ==========
    {'titolo': 'POR FESR Veneto - Innovazione', 'ente': 'Regione Veneto', 'tipo_ente': 'regione', 'regione': 'Veneto', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€200.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Innovazione e competitività', 'beneficiari': 'PMI Veneto', 'url': 'https://www.regione.veneto.it/'},
    {'titolo': 'Bando Digitalizzazione PMI Veneto', 'ente': 'Regione Veneto', 'tipo_ente': 'regione', 'regione': 'Veneto', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€40.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Trasformazione digitale', 'beneficiari': 'PMI Veneto', 'url': 'https://www.regione.veneto.it/'},
    {'titolo': 'Bando Startup Veneto 2025', 'ente': 'Regione Veneto', 'tipo_ente': 'regione', 'regione': 'Veneto', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€100.000', 'percentuale': '60%', 'scadenza': 'Vedi bando', 'descrizione': 'Sostegno startup innovative', 'beneficiari': 'Startup Veneto', 'url': 'https://www.regione.veneto.it/'},
    {'titolo': 'Bando Turismo Veneto', 'ente': 'Regione Veneto', 'tipo_ente': 'regione', 'regione': 'Veneto', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€60.000', 'percentuale': '40%', 'scadenza': 'Vedi bando', 'descrizione': 'Sviluppo settore turistico', 'beneficiari': 'Imprese turistiche', 'url': 'https://www.regione.veneto.it/'},
    
    # ========== REGIONE EMILIA-ROMAGNA ==========
    {'titolo': 'Bando Innovazione Emilia-Romagna', 'ente': 'Regione Emilia-Romagna', 'tipo_ente': 'regione', 'regione': 'Emilia-Romagna', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€150.000', 'percentuale': '45%', 'scadenza': 'Vedi bando', 'descrizione': 'R&S e innovazione', 'beneficiari': 'PMI Emilia-Romagna', 'url': 'https://www.regione.emilia-romagna.it/'},
    {'titolo': 'Bando Digitalizzazione Emilia-Romagna', 'ente': 'Regione Emilia-Romagna', 'tipo_ente': 'regione', 'regione': 'Emilia-Romagna', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€50.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Transizione digitale', 'beneficiari': 'PMI Emilia-Romagna', 'url': 'https://www.regione.emilia-romagna.it/'},
    {'titolo': 'Bando Green Economy Emilia-Romagna', 'ente': 'Regione Emilia-Romagna', 'tipo_ente': 'regione', 'regione': 'Emilia-Romagna', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€100.000', 'percentuale': '40%', 'scadenza': 'Vedi bando', 'descrizione': 'Economia circolare e sostenibilità', 'beneficiari': 'PMI Emilia-Romagna', 'url': 'https://www.regione.emilia-romagna.it/'},
    
    # ========== REGIONE PIEMONTE ==========
    {'titolo': 'Bando Competitività Piemonte', 'ente': 'Regione Piemonte', 'tipo_ente': 'regione', 'regione': 'Piemonte', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€120.000', 'percentuale': '45%', 'scadenza': 'Vedi bando', 'descrizione': 'Competitività PMI', 'beneficiari': 'PMI Piemonte', 'url': 'https://www.regione.piemonte.it/'},
    {'titolo': 'Linea Credito Piemonte', 'ente': 'Finpiemonte', 'tipo_ente': 'regione', 'regione': 'Piemonte', 'tipo_contributo': 'tasso_agevolato', 'contributo_max': '€500.000', 'percentuale': 'Tasso agevolato', 'scadenza': 'Sempre aperto', 'descrizione': 'Finanziamenti agevolati', 'beneficiari': 'PMI Piemonte', 'url': 'https://www.finpiemonte.it/'},
    {'titolo': 'Bando Innovazione Piemonte', 'ente': 'Regione Piemonte', 'tipo_ente': 'regione', 'regione': 'Piemonte', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€80.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Progetti innovativi', 'beneficiari': 'PMI Piemonte', 'url': 'https://www.regione.piemonte.it/'},
    
    # ========== REGIONE TOSCANA ==========
    {'titolo': 'Bando Digitalizzazione Toscana', 'ente': 'Regione Toscana', 'tipo_ente': 'regione', 'regione': 'Toscana', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€45.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Digitalizzazione PMI', 'beneficiari': 'PMI Toscana', 'url': 'https://www.regione.toscana.it/'},
    {'titolo': 'Bando Turismo Toscana', 'ente': 'Regione Toscana', 'tipo_ente': 'regione', 'regione': 'Toscana', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€70.000', 'percentuale': '40%', 'scadenza': 'Vedi bando', 'descrizione': 'Sviluppo turistico', 'beneficiari': 'Imprese turistiche', 'url': 'https://www.regione.toscana.it/'},
    {'titolo': 'Bando Artigianato Toscana', 'ente': 'Regione Toscana', 'tipo_ente': 'regione', 'regione': 'Toscana', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€30.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Sostegno artigianato', 'beneficiari': 'Artigiani Toscana', 'url': 'https://www.regione.toscana.it/'},
    
    # ========== REGIONE LAZIO ==========
    {'titolo': 'Bando Innovazione Lazio', 'ente': 'Regione Lazio', 'tipo_ente': 'regione', 'regione': 'Lazio', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€100.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Innovazione PMI', 'beneficiari': 'PMI Lazio', 'url': 'https://www.regione.lazio.it/'},
    {'titolo': 'Startup Lazio', 'ente': 'Lazio Innova', 'tipo_ente': 'regione', 'regione': 'Lazio', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€80.000', 'percentuale': '60%', 'scadenza': 'Vedi bando', 'descrizione': 'Sostegno startup', 'beneficiari': 'Startup Lazio', 'url': 'https://www.lazioinnova.it/'},
    {'titolo': 'Bando Commercio Lazio', 'ente': 'Regione Lazio', 'tipo_ente': 'regione', 'regione': 'Lazio', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€25.000', 'percentuale': '40%', 'scadenza': 'Vedi bando', 'descrizione': 'Sostegno commercio', 'beneficiari': 'Commercianti Lazio', 'url': 'https://www.regione.lazio.it/'},
    
    # ========== REGIONE CAMPANIA ==========
    {'titolo': 'Bando Sviluppo Campania', 'ente': 'Regione Campania', 'tipo_ente': 'regione', 'regione': 'Campania', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€150.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Sviluppo imprese', 'beneficiari': 'PMI Campania', 'url': 'https://www.regione.campania.it/'},
    {'titolo': 'Yes I Start Up Campania', 'ente': 'Regione Campania', 'tipo_ente': 'regione', 'regione': 'Campania', 'tipo_contributo': 'misto', 'contributo_max': '€100.000', 'percentuale': '70%', 'scadenza': 'Sempre aperto', 'descrizione': 'Autoimpiego giovani', 'beneficiari': 'Under 35 Campania', 'url': 'https://www.regione.campania.it/'},
    
    # ========== REGIONE PUGLIA ==========
    {'titolo': 'NIDI Puglia - Nuove Iniziative Impresa', 'ente': 'Regione Puglia', 'tipo_ente': 'regione', 'regione': 'Puglia', 'tipo_contributo': 'misto', 'contributo_max': '€150.000', 'percentuale': '60%', 'scadenza': 'Sempre aperto', 'descrizione': 'Avvio nuove imprese', 'beneficiari': 'Nuove imprese Puglia', 'url': 'https://www.regione.puglia.it/'},
    {'titolo': 'Tecnonidi Puglia', 'ente': 'Regione Puglia', 'tipo_ente': 'regione', 'regione': 'Puglia', 'tipo_contributo': 'misto', 'contributo_max': '€250.000', 'percentuale': '80%', 'scadenza': 'Sempre aperto', 'descrizione': 'Startup tecnologiche', 'beneficiari': 'Startup tech Puglia', 'url': 'https://www.regione.puglia.it/'},
    {'titolo': 'PIN Puglia - Iniziative Giovanili', 'ente': 'Regione Puglia', 'tipo_ente': 'regione', 'regione': 'Puglia', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€30.000', 'percentuale': '100%', 'scadenza': 'Sempre aperto', 'descrizione': 'Progetti giovani', 'beneficiari': 'Under 35 Puglia', 'url': 'https://www.regione.puglia.it/'},
    
    # ========== REGIONE SICILIA ==========
    {'titolo': 'Bando Turismo Sicilia', 'ente': 'Regione Sicilia', 'tipo_ente': 'regione', 'regione': 'Sicilia', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€100.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Sviluppo turistico', 'beneficiari': 'Imprese turistiche', 'url': 'https://www.regione.sicilia.it/'},
    {'titolo': 'Bando Startup Sicilia', 'ente': 'Regione Sicilia', 'tipo_ente': 'regione', 'regione': 'Sicilia', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€80.000', 'percentuale': '70%', 'scadenza': 'Vedi bando', 'descrizione': 'Sostegno startup', 'beneficiari': 'Startup Sicilia', 'url': 'https://www.regione.sicilia.it/'},
    
    # ========== REGIONE SARDEGNA ==========
    {'titolo': 'Bando Imprese Sardegna', 'ente': 'Regione Sardegna', 'tipo_ente': 'regione', 'regione': 'Sardegna', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€120.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Sviluppo imprese', 'beneficiari': 'PMI Sardegna', 'url': 'https://www.regione.sardegna.it/'},
    {'titolo': 'Startup Sardegna', 'ente': 'Sardegna Ricerche', 'tipo_ente': 'regione', 'regione': 'Sardegna', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€70.000', 'percentuale': '60%', 'scadenza': 'Vedi bando', 'descrizione': 'Sostegno startup', 'beneficiari': 'Startup Sardegna', 'url': 'https://www.sardegnaricerche.it/'},
    
    # ========== REGIONE CALABRIA ==========
    {'titolo': 'Bando PMI Calabria', 'ente': 'Regione Calabria', 'tipo_ente': 'regione', 'regione': 'Calabria', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€100.000', 'percentuale': '60%', 'scadenza': 'Vedi bando', 'descrizione': 'Sviluppo PMI', 'beneficiari': 'PMI Calabria', 'url': 'https://www.regione.calabria.it/'},
    {'titolo': 'Bando Turismo Calabria', 'ente': 'Regione Calabria', 'tipo_ente': 'regione', 'regione': 'Calabria', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€80.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Turismo e ospitalità', 'beneficiari': 'Imprese turistiche', 'url': 'https://www.regione.calabria.it/'},
    
    # ========== REGIONE ABRUZZO ==========
    {'titolo': 'Bando Innovazione Abruzzo', 'ente': 'Regione Abruzzo', 'tipo_ente': 'regione', 'regione': 'Abruzzo', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€80.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Innovazione PMI', 'beneficiari': 'PMI Abruzzo', 'url': 'https://www.regione.abruzzo.it/'},
    
    # ========== REGIONE MARCHE ==========
    {'titolo': 'Bando Digitalizzazione Marche', 'ente': 'Regione Marche', 'tipo_ente': 'regione', 'regione': 'Marche', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€40.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Digitalizzazione PMI', 'beneficiari': 'PMI Marche', 'url': 'https://www.regione.marche.it/'},
    
    # ========== REGIONE UMBRIA ==========
    {'titolo': 'Bando Competitività Umbria', 'ente': 'Regione Umbria', 'tipo_ente': 'regione', 'regione': 'Umbria', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€60.000', 'percentuale': '45%', 'scadenza': 'Vedi bando', 'descrizione': 'Competitività imprese', 'beneficiari': 'PMI Umbria', 'url': 'https://www.regione.umbria.it/'},
    
    # ========== REGIONE FRIULI VENEZIA GIULIA ==========
    {'titolo': 'Bando Innovazione FVG', 'ente': 'Regione FVG', 'tipo_ente': 'regione', 'regione': 'Friuli Venezia Giulia', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€100.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Innovazione PMI', 'beneficiari': 'PMI FVG', 'url': 'https://www.regione.fvg.it/'},
    {'titolo': 'Bando Digitalizzazione PMI FVG', 'ente': 'Regione FVG', 'tipo_ente': 'regione', 'regione': 'Friuli Venezia Giulia', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€50.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Trasformazione digitale', 'beneficiari': 'PMI FVG', 'url': 'https://www.regione.fvg.it/'},
    
    # ========== REGIONE LIGURIA ==========
    {'titolo': 'Bando PMI Liguria', 'ente': 'Regione Liguria', 'tipo_ente': 'regione', 'regione': 'Liguria', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€50.000', 'percentuale': '45%', 'scadenza': 'Vedi bando', 'descrizione': 'Sviluppo PMI', 'beneficiari': 'PMI Liguria', 'url': 'https://www.regione.liguria.it/'},
    
    # ========== REGIONE MOLISE ==========
    {'titolo': 'Bando Imprese Molise', 'ente': 'Regione Molise', 'tipo_ente': 'regione', 'regione': 'Molise', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€50.000', 'percentuale': '60%', 'scadenza': 'Vedi bando', 'descrizione': 'Sviluppo imprese', 'beneficiari': 'PMI Molise', 'url': 'https://www.regione.molise.it/'},
    
    # ========== REGIONE BASILICATA ==========
    {'titolo': 'Bando PMI Basilicata', 'ente': 'Regione Basilicata', 'tipo_ente': 'regione', 'regione': 'Basilicata', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€80.000', 'percentuale': '60%', 'scadenza': 'Vedi bando', 'descrizione': 'Sviluppo PMI', 'beneficiari': 'PMI Basilicata', 'url': 'https://www.regione.basilicata.it/'},
    
    # ========== TRENTINO ALTO ADIGE ==========
    {'titolo': 'Bando Innovazione Trentino', 'ente': 'Provincia Trento', 'tipo_ente': 'regione', 'regione': 'Trentino-Alto Adige', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€100.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Innovazione imprese', 'beneficiari': 'PMI Trentino', 'url': 'https://www.provincia.tn.it/'},
    {'titolo': 'Bando Innovazione Alto Adige', 'ente': 'Provincia Bolzano', 'tipo_ente': 'regione', 'regione': 'Trentino-Alto Adige', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€120.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Innovazione imprese', 'beneficiari': 'PMI Alto Adige', 'url': 'https://www.provincia.bz.it/'},
    
    # ========== VALLE D'AOSTA ==========
    {'titolo': 'Bando Imprese Valle Aosta', 'ente': 'Regione Valle Aosta', 'tipo_ente': 'regione', 'regione': 'Valle Aosta', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€50.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Sviluppo imprese', 'beneficiari': 'PMI Valle Aosta', 'url': 'https://www.regione.vda.it/'},
    
    # ========== CAMERE DI COMMERCIO ==========
    {'titolo': 'Voucher Digitali I4.0 CCIAA Milano', 'ente': 'Camera Commercio Milano', 'tipo_ente': 'cciaa', 'regione': 'Lombardia', 'tipo_contributo': 'voucher', 'contributo_max': '€10.000', 'percentuale': '70%', 'scadenza': 'Vedi bando', 'descrizione': 'Digitalizzazione', 'beneficiari': 'PMI Milano', 'url': 'https://www.milomb.camcom.it/'},
    {'titolo': 'Voucher Digitali CCIAA Torino', 'ente': 'Camera Commercio Torino', 'tipo_ente': 'cciaa', 'regione': 'Piemonte', 'tipo_contributo': 'voucher', 'contributo_max': '€10.000', 'percentuale': '70%', 'scadenza': 'Vedi bando', 'descrizione': 'Digitalizzazione', 'beneficiari': 'PMI Torino', 'url': 'https://www.to.camcom.it/'},
    {'titolo': 'Voucher Digitali CCIAA Venezia', 'ente': 'Camera Commercio Venezia', 'tipo_ente': 'cciaa', 'regione': 'Veneto', 'tipo_contributo': 'voucher', 'contributo_max': '€10.000', 'percentuale': '70%', 'scadenza': 'Vedi bando', 'descrizione': 'Digitalizzazione', 'beneficiari': 'PMI Venezia', 'url': 'https://www.ve.camcom.it/'},
    {'titolo': 'Voucher Digitali CCIAA Bologna', 'ente': 'Camera Commercio Bologna', 'tipo_ente': 'cciaa', 'regione': 'Emilia-Romagna', 'tipo_contributo': 'voucher', 'contributo_max': '€10.000', 'percentuale': '70%', 'scadenza': 'Vedi bando', 'descrizione': 'Digitalizzazione', 'beneficiari': 'PMI Bologna', 'url': 'https://www.bo.camcom.gov.it/'},
    {'titolo': 'Voucher Digitali CCIAA Roma', 'ente': 'Camera Commercio Roma', 'tipo_ente': 'cciaa', 'regione': 'Lazio', 'tipo_contributo': 'voucher', 'contributo_max': '€10.000', 'percentuale': '70%', 'scadenza': 'Vedi bando', 'descrizione': 'Digitalizzazione', 'beneficiari': 'PMI Roma', 'url': 'https://www.rm.camcom.it/'},
    {'titolo': 'Voucher Digitali CCIAA Napoli', 'ente': 'Camera Commercio Napoli', 'tipo_ente': 'cciaa', 'regione': 'Campania', 'tipo_contributo': 'voucher', 'contributo_max': '€10.000', 'percentuale': '70%', 'scadenza': 'Vedi bando', 'descrizione': 'Digitalizzazione', 'beneficiari': 'PMI Napoli', 'url': 'https://www.na.camcom.gov.it/'},
    {'titolo': 'Voucher Digitali CCIAA Bari', 'ente': 'Camera Commercio Bari', 'tipo_ente': 'cciaa', 'regione': 'Puglia', 'tipo_contributo': 'voucher', 'contributo_max': '€10.000', 'percentuale': '70%', 'scadenza': 'Vedi bando', 'descrizione': 'Digitalizzazione', 'beneficiari': 'PMI Bari', 'url': 'https://www.ba.camcom.it/'},
    {'titolo': 'Voucher Digitali CCIAA Firenze', 'ente': 'Camera Commercio Firenze', 'tipo_ente': 'cciaa', 'regione': 'Toscana', 'tipo_contributo': 'voucher', 'contributo_max': '€10.000', 'percentuale': '70%', 'scadenza': 'Vedi bando', 'descrizione': 'Digitalizzazione', 'beneficiari': 'PMI Firenze', 'url': 'https://www.fi.camcom.gov.it/'},
    {'titolo': 'Voucher Export CCIAA Milano', 'ente': 'Camera Commercio Milano', 'tipo_ente': 'cciaa', 'regione': 'Lombardia', 'tipo_contributo': 'voucher', 'contributo_max': '€15.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Internazionalizzazione', 'beneficiari': 'PMI Milano', 'url': 'https://www.milomb.camcom.it/'},
    
    # ========== SETTORE AGRICOLTURA ==========
    {'titolo': 'PSR - Giovani Agricoltori', 'ente': 'Ministero Agricoltura', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€70.000', 'percentuale': '100%', 'scadenza': 'Vedi bando', 'descrizione': 'Insediamento giovani in agricoltura', 'beneficiari': 'Under 41 agricoltori', 'url': 'https://www.politicheagricole.it/'},
    {'titolo': 'PSR - Investimenti Aziende Agricole', 'ente': 'Ministero Agricoltura', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€500.000', 'percentuale': '40%', 'scadenza': 'Vedi bando', 'descrizione': 'Modernizzazione aziende agricole', 'beneficiari': 'Imprese agricole', 'url': 'https://www.politicheagricole.it/'},
    {'titolo': 'OCM Vino - Investimenti', 'ente': 'Ministero Agricoltura', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€400.000', 'percentuale': '50%', 'scadenza': 'Vedi bando', 'descrizione': 'Settore vitivinicolo', 'beneficiari': 'Aziende vitivinicole', 'url': 'https://www.politicheagricole.it/'},
    {'titolo': 'Bando Agroalimentare PNRR', 'ente': 'Ministero Agricoltura', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€2.000.000', 'percentuale': '40%', 'scadenza': 'Vedi bando', 'descrizione': 'Innovazione filiera agroalimentare', 'beneficiari': 'Imprese agroalimentari', 'url': 'https://www.politicheagricole.it/'},
    
    # ========== SETTORE TURISMO ==========
    {'titolo': 'Fondo Rotativo Turismo', 'ente': 'Ministero Turismo', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'misto', 'contributo_max': '€1.000.000', 'percentuale': '35%', 'scadenza': 'Vedi bando', 'descrizione': 'Riqualificazione strutture turistiche', 'beneficiari': 'Imprese turistiche', 'url': 'https://www.ministeroturismo.gov.it/'},
    {'titolo': 'Bonus Alberghi', 'ente': 'Ministero Turismo', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'credito_imposta', 'contributo_max': '€200.000', 'percentuale': '80%', 'scadenza': 'Vedi bando', 'descrizione': 'Ristrutturazione alberghi', 'beneficiari': 'Alberghi e strutture ricettive', 'url': 'https://www.ministeroturismo.gov.it/'},
    
    # ========== SETTORE CULTURA ==========
    {'titolo': 'Tax Credit Cinema', 'ente': 'MiC', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'credito_imposta', 'contributo_max': '€1.000.000', 'percentuale': '40%', 'scadenza': 'Sempre aperto', 'descrizione': 'Produzioni cinematografiche', 'beneficiari': 'Case di produzione', 'url': 'https://www.beniculturali.it/'},
    {'titolo': 'Art Bonus', 'ente': 'MiC', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'credito_imposta', 'contributo_max': 'Variabile', 'percentuale': '65%', 'scadenza': 'Sempre aperto', 'descrizione': 'Donazioni beni culturali', 'beneficiari': 'Tutti i contribuenti', 'url': 'https://artbonus.gov.it/'},
    
    # ========== PNRR ==========
    {'titolo': 'PNRR Parità di Genere', 'ente': 'PCM', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€50.000', 'percentuale': '80%', 'scadenza': 'Vedi bando', 'descrizione': 'Imprenditoria femminile PNRR', 'beneficiari': 'Imprese femminili', 'url': 'https://www.italiadomani.gov.it/'},
    {'titolo': 'PNRR Digitalizzazione PA', 'ente': 'PCM', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'fondo_perduto', 'contributo_max': 'Variabile', 'percentuale': '100%', 'scadenza': 'Vedi bando', 'descrizione': 'Servizi digitali per PA', 'beneficiari': 'Enti pubblici e fornitori', 'url': 'https://www.italiadomani.gov.it/'},
    {'titolo': 'PNRR Green Transition', 'ente': 'MASE', 'tipo_ente': 'ministero', 'regione': 'Nazionale', 'tipo_contributo': 'fondo_perduto', 'contributo_max': '€3.000.000', 'percentuale': '40%', 'scadenza': 'Vedi bando', 'descrizione': 'Transizione ecologica imprese', 'beneficiari': 'PMI e Grandi imprese', 'url': 'https://www.mase.gov.it/'},
]


def scrape_bandi_statici() -> List[Dict]:
    """Carica tutti i bandi dal database statico."""
    print("      → Caricamento database bandi completo...")
    bandi = []
    for bando_info in BANDI_COMPLETI:
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
