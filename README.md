# 🇮🇹 BandiItalia - Aggregatore Bandi e Finanziamenti

Aggregatore bandi a fondo perduto, finanziamenti agevolati e incentivi per PMI italiane.

## Architettura

- **Database**: Supabase (tabella `bandi`)
- **Sito**: `bandi.html` su raasautomazioni.it
- **Archiviazione**: Edge Function Supabase + cronjob giornaliero (cron-job.org, ore 6:00)
- **Manutenzione**: Script Python locali + GitHub Actions per check giornaliero

## Struttura Repository

```
bandi-scraper/
├── .github/workflows/
│   └── check-bandi.yml          # GitHub Actions: check giornaliero (NO inserimenti)
├── scripts/
│   ├── check_stato.py           # Fase A: analisi completa database
│   ├── carica_bandi.py          # Fase B: template caricamento nuovi bandi
│   ├── pulisci_tutto.py         # Fase C: pulizia duplicati + normalizzazione
│   └── archivia_scaduti.py      # Archivia bandi con scadenza passata
├── PROMPT_GESTIONE_BANDI.md     # Prompt da usare con Claude per aggiornamenti
├── requirements.txt
└── README.md
```

## Procedura Aggiornamento Bandi

### 1. Apri nuova chat con Claude
### 2. Incolla il contenuto di `PROMPT_GESTIONE_BANDI.md`
### 3. Passa i nuovi bandi (titoli, scadenze, link)
### 4. Claude genera script .py pronti da lanciare

## Comandi Rapidi

```bash
# Check stato database
py -3.12 scripts/check_stato.py

# Pulizia duplicati e normalizzazione
py -3.12 scripts/pulisci_tutto.py

# Archivia bandi scaduti
py -3.12 scripts/archivia_scaduti.py

# Carica nuovi bandi (dopo generazione da Claude)
py -3.12 scripts/carica_bandi.py
```

## Regioni Standard

Nazionale, Sud Italia, Piemonte, Valle d'Aosta, Lombardia, Trentino-Alto Adige, Veneto, Friuli Venezia Giulia, Liguria, Emilia-Romagna, Toscana, Umbria, Marche, Lazio, Abruzzo, Molise, Campania, Puglia, Basilicata, Calabria, Sicilia, Sardegna

## Campi Tabella `bandi`

| Campo | Tipo | Valori |
|---|---|---|
| titolo | text | "Ente — Descrizione breve" |
| ente | text | MIMIT, INAIL, Regione Veneto, etc. |
| tipo_ente | text | ministero, ente_nazionale, regione, cciaa, altro |
| regione | text | Vedi lista standard sopra |
| tipo_contributo | text | fondo_perduto, tasso_agevolato, misto, credito_imposta |
| stato | text | aperto, chiuso, in_arrivo |
| scadenza | text | GG/MM/AAAA oppure "A esaurimento" |
| descrizione | text | 30-50 parole SEO |
| url | text | Link ufficiale |
| attivo | boolean | true = visibile |

## Note Importanti

- **NON inserire bandi statici da GitHub Actions** (causa duplicati)
- GitHub Actions fa SOLO check/report, mai inserimenti
- I nuovi bandi si caricano SOLO manualmente via script generati da Claude
- Il dedup funziona per URL (normalizzato) + similarità titolo >= 70%
- Il cronjob su cron-job.org archivia automaticamente ogni mattina alle 6:00
