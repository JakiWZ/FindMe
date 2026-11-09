# Project Brief e piano

Compilatelo insieme all'inizio: serve per il CP1. Sostituite ogni `…` con una risposta vera.

## 1. Gruppo e ruoli

| Nome del gruppo | Progetto | Challenge |
|---|---|---|
| MindHive | FindMe | Challenge 5 |

| Componente | Ruolo |
|---|---|
| Gioacchino | PM: coordinamento, board e documentazione |
| Micaela | Backend: Python, logica del programma e database SQLite |
| Giusy | Frontend: pagina web e interfaccia |
| Danilo | Tester: prove manuali con dati di test |

In tre unite Frontend e Coordinamento e documentazione.

## 2. Problema e target

| Problema | Target |
|---|---|
| Le informazioni sugli eventi universitari e sugli oggetti smarriti o ritrovati possono essere difficili da trovare perché sono distribuite su diversi canali. | Studenti, docenti e altri membri della comunità universitaria. |

Domanda guida: «Come potremmo aiutare chi, a fare cosa, attraverso cosa?»

| Aiutare chi | A fare cosa | Attraverso cosa |
|---|---|---|
| La comunità universitaria | Trovare informazioni sugli eventi e segnalare oggetti smarriti o ritrovati | Una dashboard interattiva |

| Cosa escludiamo |
|---|
| Chat interattiva tra la comunità universitaria |

## 3. Obiettivi

Ogni obiettivo ha una prova che si può eseguire. Esempio: «L'utente può registrare un lotto»; prova: «inserisco il lotto A con valore 18,5 e compare nel file».

| ID | Obiettivo | Prova |
|---|---|---|
| O1 | L'utente può aggiungere un oggetto ritrovato | Faccio il login come `mario.rossi`, scelgo 3 e inserisco "Penna rossa" in "Aula 1": compare "Oggetto #81 registrato." e l'oggetto è nell'elenco (scelta 1) |
| O2 | L'utente può consultare la bacheca e cercare gli oggetti | Scelgo 6 e vedo i post; scelgo 2, cerco "penna" e compaiono solo gli oggetti che contengono "penna" |
| O3 | L'utente può segnare un oggetto come restituito, senza cancellarlo | Scelgo 4 con l'ID 81: compare "segnato come restituito" e nel riepilogo (scelta 5) gli oggetti da restituire scendono di 1 |

## 4. MVP: le tre operazioni

| Operazione | Input | Risultato |
|---|---|---|
| 1. Aggiunta oggetto | Descrizione, luogo, data (AAAA-MM-GG, vuota = oggi), con login | Oggetto salvato nel database con stato "trovato" e messaggio con il suo ID |
| 2. Restituzione oggetto | ID dell'oggetto, con login | Stato cambiato in "restituito"; errore se l'ID non esiste o se era già restituito |
| 3. Riepilogo ed esportazione | Scelta 5 oppure 8 | Conteggio per luogo degli oggetti da restituire e restituiti; con la scelta 8 il file `output/report.json` |

## 5. Dati

| Voce | Risposta |
|---|---|
| File di input e formato | Database SQLite `infrastructure/findme.db`, riempito al primo avvio con i dati di `infrastructure/seed.sql` |
| Record di esempio in input | Tabella `oggetti_smarriti`: `id=1, descrizione="Zaino viola", luogo="Biblioteca", id_utente=4, stato="trovato", data_ritrovamento="2026-11-05"` |
| File di output | `output/report.json` (JSON), creato con la scelta 8 e caricato dalla dashboard in `frontend/index.html` |
| Un record di esempio in output | `{"luogo": "Aula 1", "da_restituire": 5, "restituiti": 1}` (una riga di `riepilogo_per_luogo`) |

## 6. Piano delle attività

Priorità: Must (indispensabile), Should (importante), Could (se avanza tempo), Won't (non lo facciamo).

| ID | Attività | Priorità | Responsabile |
|---|---|---|---|
| A1 | Creare il database e le funzioni per aggiungere e leggere oggetti | Must | Micaela (supporto: Danilo) |
| A2 | Dashboard che carica il report esportato dal backend | Must | Giusy |
| A3 | Test su aggiunta e dati | Should | Danilo |
| A4 | Documentazione e istruzioni d'uso | Should | Gioacchino |
| A5 | Modifica dello stato di un oggetto (restituito) | Could | Micaela (supporto: Giusy) |
| A6 | Autenticazione chat | Won't | Nessuno |

Feature freeze: dopo il CP3 solo correzioni, test e documentazione.

## Pronto per CP1?

- [x] Nomi e ruoli sono scritti
- [x] Problema, target e domanda guida sono completi
- [x] Tre obiettivi con prova e tre operazioni con input e risultato
- [x] Dati e piano delle attività con priorità e responsabili
- [x] Nessun `…` è rimasto nel file
