# Monitoraggio

Aggiornate il Kanban quando cambia qualcosa; usate gli ID delle attività del piano nel Project Brief.

## Kanban

Stato: TODO, IN PROGRESS o DONE. Un'attività è DONE solo se avete una verifica (per esempio «`python main.py` salva `output/report.json`»).

| ID | Attività | Responsabile | Stato | Verifica |
|---|---|---|---|---|
| A1 | Database e funzioni per aggiungere e leggere oggetti | Micaela (supporto: Danilo) | DONE | `python main.py`, scelta 3 aggiunge un oggetto, scelta 1 lo mostra; al riavvio è ancora nel database |
| A2 | Dashboard che carica il report esportato dal backend | Giusy | DONE | Si apre `frontend/index.html`, si seleziona `output/report.json` e compaiono numeri, elenco e riepilogo |
| A3 | Test su aggiunta e dati | Danilo | DONE | Tabelle "Casi di prova" nel `README.md`, con risultato atteso e osservato |
| A4 | Documentazione e istruzioni d'uso | Gioacchino | DONE | `README.md` con avvio, menu, tecnologie, dashboard e test |
| A5 | Modifica dello stato di un oggetto (restituito) | Micaela (supporto: Giusy) | DONE | Scelta 4 con un ID: l'oggetto diventa "restituito" e il riepilogo (scelta 5) si aggiorna |
| A6 | Autenticazione chat | Nessuno | Non prevista (Won't) | Esclusa nel Project Brief |

## Checkpoint

| CP | Cosa abbiamo mostrato | Cosa cambiamo |
|---|---|---|
| CP1 | Project Brief: problema, target, obiettivi, tre operazioni, dati e piano delle attività | Definite meglio le tre operazioni del MVP (aggiunta, restituzione, riepilogo) |
| CP2 | Prima versione nella repository Smart-Community, con backend basato su Flask | Flask tolto perché non richiesto e fonte di problemi; progetto rifatto nella nuova repository FindMe con menu da terminale e database SQLite |
| CP3 | Flusso completo: `python main.py` → scelta 8 → `output/report.json` → dashboard nel browser | Frontend ridotto a dashboard del report (login e modifiche restano nel programma Python); casi di prova documentati nel README |

Cosa mostrare: CP1 brief, tre operazioni, dati e piano; CP2 programma avviato e una funzionalità completa; CP3 tutte le operazioni del MVP e flusso Python→file→pagina.
