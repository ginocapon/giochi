# CLAUDE.md — Istruzioni Automatiche

> Questo file viene letto automaticamente da Claude ad ogni sessione.
> Per le regole operative complete, consulta **SKILL.md**.

## Regole Rapide

1. **Leggi SKILL.md** prima di ogni sessione di lavoro
2. **Tech stack:** HTML + CSS + JS vanilla — ZERO librerie esterne
3. **Mobile-first** — progetta prima per mobile, poi adatta per desktop
4. **Commit in italiano** — messaggi chiari e descrittivi
5. **Aggiorna sitemap.xml** quando aggiungi/rimuovi pagine
6. **Performance:** mai filter su animazioni, solo opacity/transform
7. **Accessibilita':** skip-nav, focus-visible, contrast 4.5:1, alt text
8. **Immagini:** WebP, width+height espliciti, lazy solo below-fold
9. **Dati verificati:** ogni numero deve avere fonte citata
10. **Sicurezza:** sanitizzare input, mai API keys nel frontend

## Comandi Utili

```bash
# Check stato bandi database
python scripts/check_stato.py

# Pulizia duplicati
python scripts/pulisci_tutto.py

# Archivia bandi scaduti
python scripts/archivia_scaduti.py
```

## File Chiave
- `SKILL.md` — Unica fonte di verita' (regole, design, KPI)
- `strategia-business-crescita-web-30gg.md` — Strategia business
- `index.html` — Homepage piattaforma Gaming Rewards
- `css/style.css` — CSS design system
- `js/app.js` — Logica principale
