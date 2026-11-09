# FindMe

Applicazione **Lost & Found** per la comunità universitaria: chi trova un oggetto lo registra, chi l'ha perso lo cerca e, alla consegna, l'oggetto viene segnato come restituito. Una bacheca raccoglie anche post su eventi e oggetti.

## Gruppo

Gruppo **MindHive** · Challenge 5

| Componente | Ruolo | Di cosa si occupa |
|---|---|---|
| Gioacchino | PM | Pianifica le attività, coordina il gruppo e tiene la board |
| Micaela | Backend | Python, logica del programma e database SQLite |
| Giusy | Frontend | Pagina web della dashboard e interfaccia |
| Danilo | Tester | Prove manuali con dati di test per trovare i problemi |

## Come funziona, in breve

```text
 Terminale (Python)            Database (SQLite)          Browser (HTML/CSS/JS)
 ┌──────────────────┐  salva  ┌──────────────────┐
 │ menu Python      │ ──────► │ findme.db        │
 │ (scelte 1-10)    │ ◄────── │ utenti, oggetti, │
 └────────┬─────────┘  legge  │ post             │
          │ scelta 8          └──────────────────┘
          ▼
   output/report.json  ──── lo selezioni a mano ────►  dashboard con numeri,
                                                       elenco e riepilogo
```

1. Con il **programma Python** nel terminale si registrano, cercano e restituiscono gli oggetti.
2. I dati vengono salvati nel **database SQLite**, quindi restano anche dopo aver chiuso il programma.
3. Con la scelta **8** Python crea un file **JSON** con il riepilogo.
4. La **dashboard** nel browser apre quel file e lo mostra in modo leggibile.

## Tecnologie usate

| Tecnologia | A cosa serve, in parole semplici |
|---|---|
| **Python 3.10+** | Il linguaggio del programma principale. Mostra il menu, controlla i dati inseriti, applica le regole (es. un oggetto non può essere restituito due volte) e calcola i riepiloghi. |
| **`match` / `case`** | Lo "switch" di Python: in base al numero scelto nel menu esegue l'operazione giusta. Serve Python 3.10 o più recente. |
| **SQLite** (modulo `sqlite3`) | Il database: un unico file (`findme.db`) che conserva utenti, oggetti e post in tabelle, come fogli di calcolo collegati tra loro. È già incluso in Python, non va installato nulla. |
| **SQL** | Il linguaggio per parlare con il database: `INSERT` per aggiungere, `SELECT` per leggere, `UPDATE` per modificare. Le tabelle sono definite in `backend/storage.py`, i dati di prova in `infrastructure/seed.sql`. |
| **JSON** (modulo `json`) | Un formato di testo per scambiare dati. Python salva il report in `output/report.json` e il browser lo legge. |
| **`pathlib`** | Trova i file del progetto partendo dalla posizione del programma, così funziona da qualunque cartella venga avviato. |
| **`datetime`** | Gestisce le date: data di oggi, controllo del formato AAAA-MM-GG, date nel futuro non ammesse. |
| **HTML** | La struttura della pagina della dashboard: titoli, riquadri, filtri, tabella. |
| **CSS** | L'aspetto grafico: colori, schede, impaginazione che si adatta anche al telefono. |
| **JavaScript** | Rende la pagina interattiva: legge il file scelto, controlla che sia un report valido, mostra i dati e applica i filtri di ricerca. Non fa calcoli: i numeri arrivano già pronti da Python. |
| **File API** (`<input type="file">`) | Permette al browser di aprire un file scelto dall'utente, senza server e senza internet. |
| **Git e GitHub** | Salvano la storia delle modifiche e permettono al gruppo di lavorare sullo stesso codice. |
| **DBeaver** (facoltativo) | Un programma per guardare dentro il database e vedere le tabelle. Non serve per usare FindMe. |

Non servono librerie esterne, server o connessione a internet.

## Requisiti

- Python **3.10 o successivo**. Verifica con `python --version` (su macOS `python3 --version`).
- Un browser moderno (Chrome, Edge, Firefox, Safari).

## Avvio del programma

Dalla cartella del progetto:

```bash
cd backend
python main.py
```

Su macOS il comando può chiamarsi `python3`.

Al primo avvio viene creato il database `infrastructure/findme.db` e vengono caricati i dati di prova di `infrastructure/seed.sql` (solo se il database è vuoto). Per ripartire da zero basta cancellare `infrastructure/findme.db`.

Utente di prova: `mario.rossi` / `password123`.

## Menu

La colonna **Login** indica se per quella scelta bisogna prima aver fatto l'accesso (scelta 10).

| Scelta | Operazione | Login |
|---|---|---|
| 1 | Visualizza elenco oggetti | no |
| 2 | Cerca oggetti per parole, luogo e stato | no |
| 3 | Aggiungi oggetto trovato | sì |
| 4 | Segna oggetto come restituito | sì |
| 5 | Riepilogo per luogo e numero di oggetti da restituire | no |
| 6 | Visualizza bacheca post (filtro per categoria) | no |
| 7 | Pubblica post (evento o oggetto) | sì |
| 8 | Esporta il report in `output/report.json` | no |
| 9 | Registrati | no |
| 10 | Login / Logout | no |
| 0 | Esci | no |

## Dashboard nel browser

1. Nel programma Python scegli **8** per creare `output/report.json`.
2. Apri `frontend/index.html` con doppio clic.
3. Premi il pulsante del file e seleziona `output/report.json`.

Vedrai il numero di oggetti da restituire, l'elenco degli oggetti con ricerca e filtri e il riepilogo per luogo. Se il file non è valido compare un messaggio che spiega il problema. Dopo nuove modifiche in Python rigenera il report (scelta 8) e selezionalo di nuovo.

Per provare la dashboard senza avviare Python c'è già un report di esempio: `frontend/report_di_prova.json`.

## Dati

- **Database:** `infrastructure/findme.db`, con le tabelle `utenti`, `oggetti_smarriti` e `post`.
- **Report esportato:** `output/report.json`. Esempio:

```json
{
  "generato_il": "2026-11-09T10:45:00",
  "oggetti_aperti": 50,
  "riepilogo_per_luogo": [{"luogo": "Aula 1", "da_restituire": 5, "restituiti": 1}],
  "oggetti": [{"id": 1, "descrizione": "Zaino viola", "luogo": "Biblioteca", "id_utente": 4, "stato": "trovato", "data_ritrovamento": "2026-11-05"}]
}
```

Per guardare il database con DBeaver: nuova connessione **SQLite**, con URL
`jdbc:sqlite:/percorso/del/progetto/FindMe/infrastructure/findme.db`.

## Struttura

```text
backend/          main.py (menu), logic.py (regole), storage.py (database e JSON)
frontend/         index.html, js/app.js, style.css (dashboard) e report_di_prova.json
infrastructure/   seed.sql (dati di prova) e findme.db (creato all'avvio)
docs/             Requisiti, guide e presentazione
output/           report.json (creato dalla scelta 8)
```

## Casi di prova

### Programma Python

| Caso | Input | Risultato atteso | Risultato osservato |
|---|---|---|---|
| Scelta sconosciuta | `abc` | "Scelta non valida." e il menu ricompare | OK |
| Uscita | `0` | "Arrivederci!", il programma termina | OK |
| Operazione senza login | `3` senza login | Richiesta di effettuare il login | OK |
| Login | `10`, `mario.rossi`, `password123` | "Benvenuto, mario.rossi!" | OK |
| Campi vuoti | `3` con descrizione vuota | "Descrizione e luogo sono obbligatori." | OK |
| Data nel futuro | `3` con data `2099-01-01` | "La data di ritrovamento non può essere nel futuro." | OK |
| Data errata | `3` con data `2026-13-40` | "Data non valida: usa il formato AAAA-MM-GG." | OK |
| Aggiunta oggetto | `3`, `Penna rossa`, `Aula 1`, invio | "Oggetto #81 registrato.", compare nell'elenco (1) | OK |
| ID non numerico | `4`, `xx` | "'xx' non è un numero valido." | OK |
| ID inesistente | `4`, `99999` | "Oggetto non trovato." | OK |
| Restituzione | `4`, `81` | "Oggetto #81 segnato come restituito." | OK |
| Doppia restituzione | `4`, `81` | "L'oggetto risulta già restituito." | OK |
| Stato non valido | `2`, `penna`, invio, `boh` | "Stato non valido: usa 'trovato' o 'restituito'." | OK |
| Post collegato | `7`, categoria `oggetto`, collega `81` | "Post #51 pubblicato.", visibile nella bacheca (6) | OK |
| Categoria errata | `6`, `boh` | "Categoria non valida: usa 'evento' o 'oggetto'." | OK |
| Username duplicato | `9`, `mario.rossi` | "Username già in uso." | OK |
| Riepilogo | `5` | Conteggi per luogo e totale da restituire (50 dopo la restituzione) | OK |
| Esportazione | `8` | `output/report.json` con i quattro campi | OK |
| Avvio da altra cartella | `python /percorso/FindMe/backend/main.py` | Usa comunque `infrastructure/` e `output/` del progetto | OK |

### Dashboard

| Caso | Input | Risultato atteso | Risultato osservato |
|---|---|---|---|
| Report valido | `report_di_prova.json` | 50 da restituire, 80 oggetti, 20 luoghi, 80 schede e 20 righe nel riepilogo | OK |
| Filtri | cerca `penna`, stato "Restituiti" | "1 di 80 oggetti" | OK |
| Nessun risultato | cerca `xyz` | "Nessun oggetto corrisponde ai filtri." | OK |
| JSON rotto | file con `{rotto` | "File non valido: non è un JSON leggibile." | OK |
| File vuoto | file senza contenuto | "File non valido: il file è vuoto." | OK |
| Campo mancante | JSON senza `oggetti` | "File non valido: manca il campo "oggetti"." | OK |
| Stato errato | un oggetto con stato `perso` | Messaggio con il numero dell'oggetto e lo stato non valido | OK |
| Errore dopo un report valido | prima il report, poi il JSON rotto | Messaggio di errore, i dati già caricati restano visibili | OK |
