"""Accesso ai dati: database SQLite ed esportazione JSON. Nessuna regola di dominio."""

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # cartella principale del progetto
DB_PATH = BASE_DIR / "infrastructure" / "findme.db"
SEED_PATH = BASE_DIR / "infrastructure" / "seed.sql"
REPORT_PATH = BASE_DIR / "output" / "report.json"

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS utenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    ruolo TEXT NOT NULL DEFAULT 'user' CHECK (ruolo IN ('admin', 'user'))
);

CREATE TABLE IF NOT EXISTS oggetti_smarriti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descrizione TEXT NOT NULL,
    luogo TEXT NOT NULL,
    id_utente INTEGER NOT NULL,
    stato TEXT NOT NULL DEFAULT 'trovato' CHECK (stato IN ('trovato', 'restituito')),
    data_ritrovamento TEXT NOT NULL,
    FOREIGN KEY (id_utente) REFERENCES utenti(id)
);

CREATE TABLE IF NOT EXISTS post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titolo TEXT NOT NULL,
    descrizione TEXT NOT NULL,
    categoria TEXT NOT NULL CHECK (categoria IN ('evento', 'oggetto')),
    id_autore INTEGER NOT NULL,
    id_oggetto INTEGER,
    data_pubblicazione TEXT NOT NULL,
    FOREIGN KEY (id_autore) REFERENCES utenti(id),
    FOREIGN KEY (id_oggetto) REFERENCES oggetti_smarriti(id)
);
"""


@contextmanager
def _connessione():
    """Apre la connessione, salva le modifiche a fine blocco e la chiude."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Crea le tabelle; se il database è vuoto carica i dati di prova."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _connessione() as conn:
        conn.executescript(SCHEMA)
        vuoto = conn.execute("SELECT COUNT(*) FROM utenti").fetchone()[0] == 0
        if vuoto and SEED_PATH.exists():
            conn.executescript(SEED_PATH.read_text(encoding="utf-8"))


# ---------- utenti ----------

def inserisci_utente(username: str, password: str, ruolo: str) -> int | None:
    """Restituisce l'id del nuovo utente, oppure None se lo username esiste già."""
    try:
        with _connessione() as conn:
            cur = conn.execute(
                "INSERT INTO utenti (username, password, ruolo) VALUES (?, ?, ?)",
                (username, password, ruolo),
            )
            return cur.lastrowid
    except sqlite3.IntegrityError:
        return None


def trova_utente_per_credenziali(username: str, password: str) -> dict | None:
    with _connessione() as conn:
        riga = conn.execute(
            "SELECT id, username, ruolo FROM utenti WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()
    return dict(riga) if riga else None


def esiste_utente(id_utente) -> bool:
    with _connessione() as conn:
        riga = conn.execute("SELECT 1 FROM utenti WHERE id = ?", (id_utente,)).fetchone()
    return riga is not None


# ---------- oggetti smarriti ----------

def inserisci_oggetto(descrizione: str, luogo: str, id_utente: int,
                      stato: str, data_ritrovamento: str) -> int:
    with _connessione() as conn:
        cur = conn.execute(
            "INSERT INTO oggetti_smarriti (descrizione, luogo, id_utente, stato, data_ritrovamento) "
            "VALUES (?, ?, ?, ?, ?)",
            (descrizione, luogo, id_utente, stato, data_ritrovamento),
        )
        return cur.lastrowid


def leggi_oggetto(id_oggetto: int) -> dict | None:
    with _connessione() as conn:
        riga = conn.execute(
            "SELECT * FROM oggetti_smarriti WHERE id = ?", (id_oggetto,)
        ).fetchone()
    return dict(riga) if riga else None


def cerca_oggetti(parole: list[str], luogo: str | None, stato: str | None) -> list[dict]:
    """Ogni parola deve comparire nella descrizione o nel luogo. luogo e stato sono filtri esatti."""
    condizioni, parametri = [], []
    for parola in parole:
        condizioni.append("(LOWER(descrizione) LIKE ? OR LOWER(luogo) LIKE ?)")
        parametri += [f"%{parola.lower()}%"] * 2
    if luogo:
        condizioni.append("LOWER(luogo) = ?")
        parametri.append(luogo.lower())
    if stato:
        condizioni.append("stato = ?")
        parametri.append(stato)
    where = "WHERE " + " AND ".join(condizioni) if condizioni else ""
    with _connessione() as conn:
        righe = conn.execute(
            f"SELECT * FROM oggetti_smarriti {where} ORDER BY data_ritrovamento DESC, id DESC",
            parametri,
        ).fetchall()
    return [dict(r) for r in righe]


def aggiorna_stato_oggetto(id_oggetto: int, stato: str) -> None:
    with _connessione() as conn:
        conn.execute("UPDATE oggetti_smarriti SET stato = ? WHERE id = ?", (stato, id_oggetto))


def conta_oggetti_per_luogo_e_stato() -> list[dict]:
    """Una riga per ogni coppia luogo/stato con il numero di oggetti."""
    with _connessione() as conn:
        righe = conn.execute(
            "SELECT luogo, stato, COUNT(*) AS n FROM oggetti_smarriti "
            "GROUP BY luogo, stato ORDER BY luogo"
        ).fetchall()
    return [dict(r) for r in righe]


# ---------- post ----------

def inserisci_post(titolo: str, descrizione: str, categoria: str, id_autore: int,
                   id_oggetto: int | None, data_pubblicazione: str) -> int:
    with _connessione() as conn:
        cur = conn.execute(
            "INSERT INTO post (titolo, descrizione, categoria, id_autore, id_oggetto, data_pubblicazione) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (titolo, descrizione, categoria, id_autore, id_oggetto, data_pubblicazione),
        )
        return cur.lastrowid


def leggi_post(id_post: int) -> dict | None:
    with _connessione() as conn:
        riga = conn.execute("SELECT * FROM post WHERE id = ?", (id_post,)).fetchone()
    return dict(riga) if riga else None


def elenco_post(categoria: str | None = None) -> list[dict]:
    query = "SELECT * FROM post"
    parametri = []
    if categoria:
        query += " WHERE categoria = ?"
        parametri.append(categoria)
    query += " ORDER BY data_pubblicazione DESC, id DESC"
    with _connessione() as conn:
        righe = conn.execute(query, parametri).fetchall()
    return [dict(r) for r in righe]


# ---------- file ----------

def salva_json(dati, percorso: Path) -> None:
    percorso.parent.mkdir(parents=True, exist_ok=True)
    with open(percorso, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)
