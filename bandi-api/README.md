# 🇮🇹 Bandi Italia - API First System

Sistema intelligente per il monitoraggio di bandi, finanziamenti e gare d'appalto italiane.

## 🎯 Caratteristiche

- **API-First**: Priorità alle API ufficiali (ANAC, CKAN, RSS)
- **Deduplicazione intelligente**: Evita duplicati tramite hash
- **Auto-aggiornamento**: Esecuzione automatica giornaliera
- **Nessun scraping HTML fragile**: Solo API e feed ufficiali
- **Gratuito**: Nessun costo di API

## 📊 Fonti Dati

| Fonte | Tipo | Copertura |
|-------|------|-----------|
| MIMIT, Invitalia, SIMEST, INAIL | Bandi statici | Nazionale |
| RSS Feeds Regionali | Feed RSS | 10+ Regioni |
| ANAC Open Data | API CKAN | Gare pubbliche |
| Contratti Pubblici | API/RSS | Appalti UE |
| Dati.gov.it | API CKAN | Open Data |

## 🚀 Esecuzione

### Automatica (GitHub Actions)
Il sistema si esegue automaticamente ogni giorno alle 7:00 ora italiana.

### Manuale
```bash
python main.py
```

## 🔧 Configurazione

Variabili d'ambiente richieste:
- `SUPABASE_URL`: URL del progetto Supabase
- `SUPABASE_KEY`: Chiave service_role di Supabase

## 📈 Roadmap

- [x] Fase 1: Bandi nazionali garantiti
- [x] Fase 2: RSS feeds regionali
- [x] Fase 3: API ANAC e Open Data
- [ ] Fase 4: NLP per estrazione automatica
- [ ] Fase 5: Alert real-time

## 📋 Struttura

```
bandi-api/
├── main.py                 # Script principale
├── requirements.txt        # Dipendenze
├── scrapers/
│   ├── bandi_statici.py    # Bandi nazionali garantiti
│   ├── api_rss.py          # RSS feeds
│   ├── api_anac.py         # ANAC Open Data
│   ├── api_contratti.py    # Contratti pubblici
│   └── api_opendata.py     # Portali Open Data
└── .github/
    └── workflows/
        └── scrape-bandi.yml
```
