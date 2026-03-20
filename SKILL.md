# SKILL 2.0 — Piattaforma Giochi & Business
## Prompt Operativo Master Unificato

> **Versione:** 2.0 — 19 Marzo 2026
> **Unica fonte di verita'** per lo sviluppo del progetto "giochi"
> **Basato su:** strategia-business-crescita-web-30gg.md + Regole SKILL RaaS Automazioni

---

## 1. ISTRUZIONI PER CLAUDE

### 1.1 Regole Operative
1. **Leggi prima** il file da modificare — mai al buio
2. **Mobile-first** — ogni modifica deve funzionare su mobile
3. **No librerie extra** — il sito e' volutamente leggero (vanilla HTML/CSS/JS)
4. **Commit** chiari e descrittivi in italiano
5. **Aggiorna** sitemap.xml quando aggiungi/rimuovi pagine
6. **Performance** — mai animazioni sull'elemento LCP; usare opacity/transform, mai filter
7. **CTA contrast** — minimo 4.5:1 (WCAG AA)
8. **Dati verificati** — ogni dato numerico DEVE avere fonte citata. Se non hai fonte, scrivi "dato non disponibile"
9. **Zero claim inventati** — nessuna percentuale o statistica senza fonte verificabile
10. **Registra ogni nuova pagina** in sitemap.xml
11. **og:image obbligatorio** — ogni pagina DEVE avere `<meta property="og:image">` per condivisione social
12. **Skip navigation** — ogni pagina DEVE avere un link skip-nav per accessibilita'
13. **Focus visible** — ogni pagina DEVE avere stili `*:focus-visible` per elementi interattivi
14. **Preconnect** — aggiungere `<link rel="preconnect">` per tutti i domini esterni usati
15. **Font-Awesome defer** — caricare con media swap
16. **Immagini width/height** — TUTTE le `<img>` DEVONO avere attributi `width` e `height` espliciti

### 1.2 Stile di Comunicazione
- Rispondi in italiano
- Sii diretto e pratico
- Proponi sempre prima di agire su operazioni irreversibili
- Tono professionale ma dinamico (settore gaming/tech)

---

## 2. CONTESTO PROGETTO

### 2.1 Informazioni Generali
| Campo | Valore |
|---|---|
| **Repository** | GitHub — ginocapon/giochi |
| **Tech Stack** | HTML statico + CSS custom + JS vanilla |
| **Framework** | Nessuno — zero dipendenze frontend |
| **Database** | Supabase (PostgreSQL) |
| **Lingua principale** | Italiano |
| **Target** | Utenti consumer (B2C) + Aziende sponsor (B2B) |
| **Modello** | Traffico sponsorizzato — le aziende pagano, gli utenti giocano gratis |

### 2.2 Modello di Business — Gaming Rewards (Play-to-Earn Sponsorizzato)
Una piattaforma dove gli utenti giocano a mini-giochi e guadagnano punti convertibili in premi reali.
I premi sono finanziati dagli sponsor (brand, e-commerce, app).

### 2.3 Modello Revenue
```
BRAND/SPONSOR → paga per impressions/click/install
         ↓
   PIATTAFORMA → trattiene 60-70% dei ricavi
         ↓
   UTENTE → riceve 30-40% sotto forma di premi/punti
```

| Fonte | Modello | Revenue Stimato |
|---|---|---|
| Offerte CPI (Cost Per Install) | €0.50-€3.00 per install | Alto |
| Video Ads (rewarded) | €5-€15 CPM | Medio-Alto |
| Survey sponsorizzate | €0.30-€1.50 per completamento | Medio |
| Affiliate marketing | 5-15% commissione | Medio |

### 2.4 Piano 30 Giorni — Gaming Rewards
| Settimana | Azione |
|---|---|
| 1 | Sviluppo piattaforma web (HTML/CSS/JS), 5 mini-giochi, sistema punti |
| 2 | Integrazione network pubblicitari (AdMob web, IronSource, Tapjoy) |
| 3 | Beta test, acquisizione primi 500 utenti (TikTok organico + gruppi gaming) |
| 4 | Ottimizzazione conversioni, scaling con UGC e referral program |

### 2.5 Struttura File Progetto
```
/
├── CLAUDE.md                    # Istruzioni automatiche per Claude
├── SKILL.md                     # Questo file — unica fonte di verita'
├── strategia-business-crescita-web-30gg.md  # Strategia business
├── index.html                   # Homepage piattaforma
├── giochi.html                  # Catalogo giochi
├── profilo.html                 # Profilo utente + punti + premi
├── classifica.html              # Classifiche e leaderboard
├── premi.html                   # Catalogo premi riscattabili
├── come-funziona.html           # Spiegazione per utenti
├── sponsor.html                 # Landing page per sponsor/brand (B2B)
├── privacy.html                 # Privacy Policy GDPR
├── cookie.html                  # Cookie Policy
├── termini.html                 # Termini di servizio
├── sitemap.xml                  # URL indicizzate
├── robots.txt                   # Configurazione crawler
├── llms.txt                     # Info per AI bots
├── ai.json                      # Permessi AI
├── humans.txt                   # Info team
├── security.txt                 # Contatto sicurezza
├── .well-known/
│   └── security.txt             # Copia security.txt
├── css/
│   └── style.css                # CSS unico, mobile-first
├── js/
│   ├── app.js                   # Logica principale
│   ├── games.js                 # Engine mini-giochi
│   └── points.js                # Sistema punti
├── games/                       # Mini-giochi individuali
│   ├── quiz/
│   ├── trivia/
│   ├── puzzle/
│   ├── memory/
│   └── speed-click/
├── assets/
│   ├── img/                     # Immagini (WebP)
│   └── icons/                   # Icone
├── scripts/                     # Script Python (bandi, manutenzione)
│   ├── check_stato.py
│   ├── carica_bandi.py
│   ├── pulisci_tutto.py
│   └── archivia_scaduti.py
└── .github/
    └── workflows/               # GitHub Actions
```

---

## 3. DESIGN SYSTEM

### 3.1 Colori
| Elemento | Valore | Uso |
|---|---|---|
| **Primario** | #6C63FF (viola vibrante) | CTA principali, accenti, link |
| **Primario dark** | #5A52D5 | Hover, gradienti |
| **Secondario** | #FF6B6B (rosso corallo) | Notifiche, badge, punti |
| **Accent** | #4ECDC4 (teal) | Successo, conferme, premi |
| **Dark** | #1a1a2e | Background hero, sezioni scure |
| **Dark secondary** | #16213e | Card, sidebar |
| **Surface** | #0f3460 | Elementi su sfondo scuro |
| **Text light** | #e8e8e8 | Testo su sfondo scuro |
| **Gold** | #FFD93D | Punti, coin, premium |

### 3.2 Tipografia
- **Font primario:** System font stack (zero caricamento esterno)
  ```css
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  ```
- **Font size base:** 16px (mobile), 18px (desktop)
- **Line height:** 1.6

### 3.3 Componenti CTA
| Elemento | Background | Testo | Ratio |
|---|---|---|---|
| CTA primario | #6C63FF | white | ~5.5:1 |
| CTA secondario | #1a1a2e | white | ~14:1 |
| CTA accent | #4ECDC4 | #1a1a2e | ~5:1 |
| CTA gold | #FFD93D | #1a1a2e | ~9:1 |

---

## 4. REQUISITI TECNICI

### 4.1 Core Web Vitals — Target
| Metrica | Target |
|---|---|
| **LCP** | < 2.0s |
| **INP** | < 200ms |
| **CLS** | < 0.1 |

### 4.2 Performance Rules
1. **No `filter: blur`** su animazioni — usare `opacity` e `transform`
2. **No `will-change` permanente** — solo al `:hover`
3. **Hero animations ritardate** — nessuna animazione above-the-fold nei primi 3s
4. **Immagini above-fold** — mai `loading="lazy"`, sempre `fetchpriority="high"`
5. **Font** — system font stack, zero caricamento esterno
6. **Critical CSS** — inline nel `<head>` per above-fold
7. **No `@import`** nei CSS
8. **JavaScript** — script non critici con `defer`
9. **Preconnect** — per tutti i domini esterni
10. **Immagini** — WebP, con `width` + `height` espliciti
11. **Facade pattern** — per iframe/video (thumbnail + click)

### 4.3 Mobile-First
- Touch target minimo: 44x44px (Apple HIG)
- Font size minimo: 16px body text
- Viewport meta tag obbligatorio
- Menu hamburger con area tocco generosa

### 4.4 Accessibilita' (WCAG)
- Contrast ratio minimo 4.5:1 testo normale, 3:1 testo grande
- Alt text su tutte le immagini informative
- Focus visible su tutti gli elementi interattivi
- Struttura heading gerarchica (H1 > H2 > H3)
- aria-label su icone/bottoni senza testo
- Skip navigation link su tutte le pagine

### 4.5 Sicurezza
- HTTPS obbligatorio
- Sanitizzare tutti gli input utente (prevenzione XSS)
- API keys mai esposte nel frontend
- Rate limiting sui form

### 4.6 SEO On-Page — Checklist
- [ ] Title tag unico (max 60 char)
- [ ] Meta description unica (max 160 char)
- [ ] H1 unico per pagina
- [ ] Alt text su tutte le immagini
- [ ] Canonical URL
- [ ] Open Graph tags completi (og:title, og:description, og:url, og:type, og:locale, og:image)
- [ ] Schema.org JSON-LD appropriato
- [ ] Registrato in sitemap.xml

---

## 5. CHECKLIST AUTOMATICHE

### Per Ogni Nuova Pagina
- [ ] Title tag unico (max 60 char)
- [ ] Meta description unica (max 160 char)
- [ ] H1 unico con keyword
- [ ] Schema.org JSON-LD
- [ ] Open Graph tags completi (incluso og:image)
- [ ] `<meta name="theme-color">`
- [ ] `<link rel="canonical">`
- [ ] Tutte le immagini con `width` + `height`
- [ ] CTA con contrasto >= 4.5:1
- [ ] Registrato in sitemap.xml
- [ ] GA4 presente (quando attivato)
- [ ] Mobile responsive
- [ ] Skip navigation link
- [ ] Focus visible styles
- [ ] Preconnect per domini esterni

### Per Ogni Modifica CSS
- [ ] Mobile-first: stili base per mobile, `@media` per desktop
- [ ] No `filter` su animazioni
- [ ] No `will-change` permanente
- [ ] Contrasto minimo 4.5:1 su CTA
- [ ] No `@import`
- [ ] Critical CSS inline, non-critico defer

### Commit
- [ ] Messaggio in italiano, descrittivo
- [ ] Nessun file sensibile (.env, credenziali)

---

## 6. KPI E OBIETTIVI

### Gaming Rewards — Obiettivi 30 Giorni
| Metrica | Settimana 1 | Settimana 2 | Settimana 3 | Settimana 4 |
|---|---|---|---|---|
| Mini-giochi | 5 | 5 | 5+ | 5+ |
| Utenti registrati | 0 | 0 | 500 | 1000+ |
| Sponsor integrati | 0 | 2-3 | 3-5 | 5+ |
| Revenue | €0 | €0 | €100-500 | €500-2000 |

### Revenue Potenziale
| Mese | Gaming Rewards |
|---|---|
| Mese 3 | €1.000-5.000 |
| Mese 12 | €5.000-30.000 |

---

> **Regola d'Oro:** "Se non hai fonte verificabile, NON inserire il dato."
> **Principio Guida:** "Le aziende pagano per raggiungere utenti. Tu crei il ponte. L'utente riceve valore gratis."
