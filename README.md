# FindMe

Applicazione Lost & Found da terminale per la comunità universitaria: chi trova un oggetto lo registra, chi l'ha perso lo cerca e, alla consegna, l'oggetto viene segnato come restituito. Una bacheca raccoglie post su eventi e oggetti.

## Requisiti

- Python **3.10 o successivo** (il menu usa `match`/`case`). Verifica con `python3 --version`.
- Nessuna dipendenza da installare: SQLite è incluso in Python (`sqlite3`).

## Avvio

Dalla cartella del progetto:

```bash
python main.py
```

Al primo avvio viene creato il database `data/findme.db` e vengono caricati i dati di prova di `data/seed.sql` (solo se il database è vuoto). Per ripartire da zero basta cancellare `data/findme.db`.

Utente di prova: `mario.rossi` / `password123`.

## Menu

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

## Dati

- **Persistenza:** database SQLite `data/findme.db` con le tabelle `utenti`, `oggetti_smarriti`, `post`.
- **Esportazione:** `output/report.json`, rigenerato con la scelta 8. Esempio:

```json
{
  "generato_il": "2026-11-09T10:45:00",
  "oggetti_aperti": 50,
  "riepilogo_per_luogo": [{"luogo": "Aula 1", "da_restituire": 5, "restituiti": 1}],
  "oggetti": [{"id": 1, "descrizione": "Zaino viola", "luogo": "Biblioteca", "id_utente": 4, "stato": "trovato", "data_ritrovamento": "2026-11-05"}]
}
```

## Struttura

```text
main.py      Menu, input e messaggi
logic.py     Regole, controlli e riepiloghi
storage.py   Database SQLite ed esportazione JSON
data/        seed.sql (dati di prova) e findme.db (creato all'avvio)
output/      report.json (creato dalla scelta 8)
```

## Casi di prova

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
| Avvio da altra cartella | `python /percorso/FindMe/main.py` | Usa comunque `data/` e `output/` del progetto | OK |
