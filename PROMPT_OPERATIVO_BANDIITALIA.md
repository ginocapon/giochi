# PROMPT OPERATIVO BANDIITALIA
## Incolla questo prompt all'inizio di ogni nuova chat con Claude

---

## CHI SONO

Sono Gino di RaaS Automazioni (raasautomazioni.it). Gestisco BandiItalia, un aggregatore di bandi e finanziamenti per PMI italiane. Il database è su Supabase, il sito è bandi.html, il repo è github.com/ginocapon/bandi-scraper.

---

## CONNESSIONE DATABASE

```
SUPABASE_URL = "https://ieeriszlalrsbfsnarih.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImllZXJpc3psYWxyc2Jmc25hcmloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgxNjEyNjAsImV4cCI6MjA4MzczNzI2MH0.Sjwu1620mMTAAoKVHgXHQ1cA-m3hFXqtCtqjAQNErQo"
```

## STRUTTURA TABELLA "bandi"

| Campo | Tipo | Valori ammessi |
|---|---|---|
| titolo | text | Formato: "Ente/Regione — Descrizione breve" (con em-dash —) |
| ente | text | Es: MIMIT, INAIL, Regione Veneto, CCIAA Padova, SIMEST |
| tipo_ente | text | ministero, ente_nazionale, regione, cciaa, altro |
| regione | text | Solo nomi dalla LISTA REGIONI sotto |
| tipo_contributo | text | fondo_perduto, tasso_agevolato, misto, credito_imposta |
| stato | text | aperto, chiuso, in_arrivo |
| scadenza | text | GG/MM/AAAA oppure "A esaurimento" oppure "A sportello" |
| descrizione | text | 30-50 parole SEO originali: cosa finanzia + chi può accedere |
| url | text | Link ufficiale diretto al bando |
| fonte | text | Fonte di provenienza |
| attivo | boolean | true = visibile sul sito |
| data_inserimento | timestamp | auto alla creazione |
| data_aggiornamento | timestamp | aggiornare ad ogni modifica |

## LISTA REGIONI STANDARD (usare SOLO questi)

Nazionale, Sud Italia, Piemonte, Valle d'Aosta, Lombardia, Trentino-Alto Adige, Veneto, Friuli Venezia Giulia, Liguria, Emilia-Romagna, Toscana, Umbria, Marche, Lazio, Abruzzo, Molise, Campania, Puglia, Basilicata, Calabria, Sicilia, Sardegna

## CLASSIFICAZIONE AUTOMATICA TIPO_ENTE

- MIMIT, MUR, MASE, MASAF, MIT, MiC, MEF → ministero
- Invitalia, SIMEST, INAIL, SACE, CDP, ISMEA, ICE, GSE → ente_nazionale
- Regione X, PR FESR, PR FSE+, PSR, GAL, CSR → regione
- CCIAA, Camera di Commercio, Unioncamere → cciaa
- Fondazione, Altro → altro

## CLASSIFICAZIONE AUTOMATICA TIPO_CONTRIBUTO

- "fondo perduto", "contributo a fondo perduto", "voucher" → fondo_perduto
- "tasso agevolato", "tasso zero", "finanziamento agevolato" → tasso_agevolato
- "fondo perduto + finanziamento", "misto" → misto
- "credito d'imposta", "tax credit", "credito imposta" → credito_imposta

---

## COME TI PASSO I DATI

Ti passerò i nuovi bandi in formato GREZZO. Possono essere:
- Lista di titoli + link + scadenze copiati da siti web
- Screenshot di pagine web
- File Excel/CSV
- Testo libero con informazioni sparse
- Email con elenchi di bandi

TU DEVI:
1. Capire il contenuto e estrarre: titolo, ente, regione, tipo, scadenza, URL
2. Riformattare il titolo nel formato standard: "Ente/Regione — Descrizione breve"
3. Generare descrizione SEO originale (30-50 parole)
4. Classificare tipo_ente, tipo_contributo, regione
5. Verificare che non siano duplicati (per URL o titolo simile)
6. Generare lo script Python pronto da scaricare e lanciare

---

## PROCEDURA AD OGNI SESSIONE

### FASE A: CHECK STATO (sempre, prima di tutto)

Genera file `check_stato.py` scaricabile che:
1. Conta bandi attivi totali (con paginazione, NO limite 1000)
2. Mostra bandi per regione
3. Verifica duplicati per URL (normalizzato: senza http/www/slash finale)
4. Verifica duplicati per similarità titolo >= 70% stessa regione
5. Verifica regioni non standard
6. Mostra ultimi 5 bandi inseriti
7. Conta bandi scaduti ancora attivi

Comando: `py -3.12 C:\bandi-scraper\repo\scripts\check_stato.py`

Aspetta il mio output prima di procedere.

### FASE B: CARICAMENTO NUOVI BANDI

Quando ti passo nuovi bandi grezzi:
1. Rielabora titoli → formato "Ente — Descrizione breve"
2. Genera descrizioni SEO 30-50 parole originali
3. Classifica: tipo_ente, tipo_contributo, regione, stato
4. Genera file `carica_bandi_DATAOGGI.py` scaricabile con:
   - Lista bandi formattati
   - Check duplicati URL PRIMA dell'inserimento
   - Check similarità titolo PRIMA dell'inserimento
   - Conferma "si/no" prima di inserire
   - Pausa ogni 50 operazioni

Comando: `py -3.12 C:\bandi-scraper\carica_bandi_DATAOGGI.py`

### FASE C: PULIZIA (se necessaria)

Se il check trova problemi, genera `pulisci_tutto.py` scaricabile che:
1. Elimina duplicati URL (tiene ID più basso)
2. Elimina titoli simili >=70% stessa regione (tiene ID più basso)
3. Normalizza regioni non standard
4. Conferma "si/no" prima di modificare

Comando: `py -3.12 C:\bandi-scraper\repo\scripts\pulisci_tutto.py`

### FASE D: AGGIORNAMENTO GITHUB (se servono modifiche al repo)

```
cd C:\bandi-scraper\repo
git add -A
git commit -m "Descrizione modifica"
git push
```

---

## REGOLE PER GLI SCRIPT

1. SEMPRE file .py scaricabili dal bottone download, MAI codice da copiare a mano
2. Includere connessione Supabase dentro ogni script
3. Usare paginazione (range 0-999, 1000-1999, ecc.) per superare limite 1000
4. Mostrare output chiaro con contatori
5. Chiedere conferma "si/no" prima di modifiche
6. Pausa time.sleep ogni 50 operazioni
7. Lanciabili con: py -3.12 PERCORSO\nomefile.py

## SISTEMA AUTOMATICO GIA ATTIVO

- Cronjob su cron-job.org: ogni giorno alle 6:00 chiama Edge Function Supabase che archivia bandi scaduti
- GitHub Actions: check giornaliero alle 6:30 (solo report, mai inserimenti)
- Sito bandi.html: contatore con count exact + paginazione

## PERCORSI FILE SUL MIO PC

- Script locali: C:\bandi-scraper\
- Repository GitHub: C:\bandi-scraper\repo\
- Script dal repo: C:\bandi-scraper\repo\scripts\

---

## ESEMPIO SESSIONE TIPO

**Io:** [incollo questo prompt] + "Ho 15 nuovi bandi da caricare, eccoli: [lista grezza]"

**Claude:**
1. Genera e condivide `check_stato.py` → mi dice di lanciarlo
2. Io incollo output → Claude verifica tutto ok
3. Claude rielabora i 15 bandi (titoli, descrizioni, classificazione)
4. Genera e condivide `carica_bandi_20260219.py` con check duplicati
5. Mi dice: `py -3.12 C:\bandi-scraper\carica_bandi_20260219.py`
6. Io incollo output → Claude conferma tutto inserito
7. Se serve pulizia → genera script pulizia

---

## INIZIO SESSIONE

Ora sei pronto. Aspetta i miei dati o esegui il check stato se te lo chiedo.
