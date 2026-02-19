# PROMPT GESTIONE BANDI - BandiItalia
## Da usare ad ogni sessione di aggiornamento database

---

### ISTRUZIONI PER CLAUDE

Sono Gino di RaaS Automazioni. Gestisco il database bandi su Supabase per BandiItalia.
Ogni volta che ti passo questo prompt, devi seguire questa procedura:

---

## 1. CONNESSIONE DATABASE

```
SUPABASE_URL = "https://ieeriszlalrsbfsnarih.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImllZXJpc3psYWxyc2Jmc25hcmloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgxNjEyNjAsImV4cCI6MjA4MzczNzI2MH0.Sjwu1620mMTAAoKVHgXHQ1cA-m3hFXqtCtqjAQNErQo"
```

## 2. STRUTTURA TABELLA "bandi"

| Campo | Tipo | Note |
|---|---|---|
| id | int | auto-increment |
| titolo | text | Formato: "Regione/Ente — Descrizione breve del bando" con em-dash |
| ente | text | Es: MIMIT, INAIL, Regione Veneto, CCIAA Padova |
| tipo_ente | text | Valori: ministero, ente_nazionale, regione, cciaa, altro |
| regione | text | Vedi lista regioni standard sotto |
| tipo_contributo | text | Valori: fondo_perduto, tasso_agevolato, misto, credito_imposta |
| stato | text | Valori: aperto, chiuso, in_arrivo |
| scadenza | text | Formato: GG/MM/AAAA oppure "A esaurimento" |
| descrizione | text | 30-50 parole SEO: cosa finanzia, chi può accedere, opportunità |
| url | text | Link ufficiale al bando |
| fonte | text | Fonte di provenienza |
| attivo | boolean | true = visibile sul sito |
| data_inserimento | timestamp | auto |
| data_aggiornamento | timestamp | aggiornare ad ogni modifica |

## 3. REGIONI STANDARD (usare SOLO questi nomi)

- Nazionale
- Italia
- Sud Italia
- Piemonte
- Valle d'Aosta
- Lombardia
- Trentino-Alto Adige
- Veneto
- Friuli Venezia Giulia
- Liguria
- Emilia-Romagna
- Toscana
- Umbria
- Marche
- Lazio
- Abruzzo
- Molise
- Campania
- Puglia
- Basilicata
- Calabria
- Sicilia
- Sardegna

## 4. PROCEDURA STANDARD

### FASE A: CHECK STATO DATABASE
Prima di qualsiasi operazione, genera uno script Python che:
1. Conta bandi attivi totali (con paginazione, NO limite 1000)
2. Conta bandi per regione
3. Verifica duplicati per URL (normalizzato senza http/www/slash finale)
4. Verifica duplicati per similarità titolo >= 70% nella stessa regione
5. Verifica regioni non standard da normalizzare
6. Mostra ultimi 5 bandi inseriti (ID più alti)
7. Mostra bandi con scadenza passata ancora attivi

### FASE B: CARICAMENTO NUOVI BANDI
Quando ti passo nuovi bandi (titoli, descrizioni, scadenze, link):
1. Rielabora i titoli nel formato standard: "Regione/Ente — Descrizione"
2. Genera descrizioni SEO 30-50 parole se mancanti
3. Classifica automaticamente: tipo_ente, tipo_contributo, regione
4. Controlla che URL non esista già nel database
5. Controlla che titolo non sia simile (>=70%) a uno esistente nella stessa regione
6. Genera script Python pronto da eseguire con: py -3.12 nomefile.py
7. Lo script deve includere check duplicati PRIMA dell'inserimento

### FASE C: PULIZIA
Se necessario:
1. Elimina duplicati (tiene ID più basso)
2. Normalizza regioni non standard
3. Archivia (attivo=false) bandi con scadenza passata
4. Chiedi SEMPRE conferma prima di eliminare/modificare

## 5. FORMATO SCRIPT OUTPUT

Tutti gli script Python devono:
- Essere file .py completi e autonomi
- Avere la connessione Supabase inclusa
- Usare paginazione (range 0-999, 1000-1999, ecc.)
- Mostrare output chiaro con contatori
- Chiedere conferma "si/no" prima di modifiche distruttive
- Avere pausa (time.sleep) ogni 50 operazioni
- Essere lanciabili con: py -3.12 C:\bandi-scraper\nomefile.py

## 6. CRONJOB ATTIVO

C'è un cronjob su cron-job.org che ogni giorno alle 6:00 chiama:
```
https://ieeriszlalrsbfsnarih.supabase.co/functions/v1/archivia-bandi?secret=bandi2025newsletter
```
Questa Edge Function archivia automaticamente i bandi scaduti.

## 7. SITO WEB

File: bandi.html su raasautomazioni.it
- La funzione loadBandi() usa paginazione e count exact
- Contatore mostra numero reale di bandi attivi
- Filtri: regione, tipo ente, tipo contributo, stato, ricerca testo

---

## QUANDO TI PASSO QUESTO PROMPT + NUOVI BANDI:

1. Leggi il prompt
2. Genera script CHECK STATO (Fase A)
3. Dammi il comando per lanciarlo
4. Aspetta il mio output
5. Se tutto ok, genera script CARICAMENTO (Fase B) con i nuovi bandi
6. Dammi il comando per lanciarlo
7. Se servono pulizie, genera script PULIZIA (Fase C)
8. Dammi il comando

IMPORTANTE: Genera SEMPRE file .py scaricabili, MAI codice da copiare a mano.
