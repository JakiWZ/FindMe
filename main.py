"""FindMe - Lost & Found universitario. Menu da terminale: unico file con input() e print()."""
import sqlite3

import logic
import storage

MENU = """
========== FINDME - Lost & Found ==========
 1. Visualizza elenco oggetti
 2. Cerca oggetti
 3. Aggiungi oggetto trovato
 4. Segna oggetto come restituito
 5. Riepilogo per luogo
 6. Visualizza bacheca post
 7. Pubblica post
 8. Esporta report JSON
 9. Registrati
10. Login / Logout
 0. Esci"""


def chiedi_intero(messaggio: str) -> int:
    testo = input(messaggio).strip()
    try:
        return int(testo)
    except ValueError:
        raise logic.ErroreLogica(f"'{testo}' non è un numero valido.")


def richiedi_login(utente):
    if utente is None:
        raise logic.ErroreLogica("Operazione riservata: effettua prima il login (scelta 10).")
    return utente


def stampa_oggetti(oggetti: list[dict]) -> None:
    if not oggetti:
        print("Nessun oggetto trovato.")
        return
    print(f"{'ID':>4}  {'DATA':<10}  {'STATO':<10}  {'LUOGO':<28}  DESCRIZIONE")
    for o in oggetti:
        print(f"{o['id']:>4}  {o['data_ritrovamento']:<10}  {o['stato']:<10}  "
              f"{o['luogo']:<28}  {o['descrizione']}")


def stampa_riepilogo(riepilogo: list[dict]) -> None:
    print(f"Oggetti ancora da restituire: {logic.conta_aperti(riepilogo)}")
    for r in riepilogo:
        print(f"  {r['luogo']:<28} da restituire: {r['da_restituire']:>3}"
              f"   restituiti: {r['restituiti']:>3}")


def stampa_post(posts: list[dict]) -> None:
    if not posts:
        print("Nessun post in bacheca.")
        return
    for p in posts:
        collegato = f" (oggetto #{p['id_oggetto']})" if p["id_oggetto"] else ""
        print(f"[{p['id']}] {p['data_pubblicazione']} - {p['categoria'].upper()}{collegato}")
        print(f"    {p['titolo']}: {p['descrizione']}")


def menu() -> None:
    storage.init_db()
    utente = None
    while True:
        print(MENU)
        if utente:
            print(f"Connesso come: {utente['username']} ({utente['ruolo']})")
        scelta = input("Scelta: ").strip()
        try:
            match scelta:
                case "1":
                    stampa_oggetti(logic.cerca_oggetti())
                case "2":
                    testo = input("Parole da cercare (invio per saltare): ")
                    luogo = input("Luogo esatto (invio per saltare): ")
                    stato = input("Stato trovato/restituito (invio per saltare): ")
                    stampa_oggetti(logic.cerca_oggetti(testo, luogo, stato))
                case "3":
                    richiedi_login(utente)
                    descrizione = input("Descrizione: ")
                    luogo = input("Luogo del ritrovamento: ")
                    data = input("Data AAAA-MM-GG (invio = oggi): ").strip()
                    o = logic.registra_oggetto(descrizione, luogo, utente["id"], data or None)
                    print(f"Oggetto #{o['id']} registrato.")
                case "4":
                    richiedi_login(utente)
                    o = logic.restituisci_oggetto(chiedi_intero("ID oggetto: "), utente["id"])
                    print(f"Oggetto #{o['id']} segnato come restituito.")
                case "5":
                    stampa_riepilogo(logic.riepilogo_per_luogo())
                case "6":
                    categoria = input("Categoria evento/oggetto (invio = tutte): ")
                    stampa_post(logic.elenco_post(categoria))
                case "7":
                    richiedi_login(utente)
                    titolo = input("Titolo: ")
                    descrizione = input("Descrizione: ")
                    categoria = input("Categoria (evento/oggetto): ").strip().lower()
                    id_oggetto = None
                    if categoria == "oggetto" and input("Collegare un oggetto? (s/n): ").strip().lower() == "s":
                        id_oggetto = chiedi_intero("ID oggetto: ")
                    p = logic.crea_post(titolo, descrizione, categoria, utente["id"], id_oggetto)
                    print(f"Post #{p['id']} pubblicato.")
                case "8":
                    print(f"Report salvato in {logic.esporta_report()}")
                case "9":
                    u = logic.registra_utente(input("Username: "), input("Password: "))
                    print(f"Utente '{u['username']}' registrato. Ora puoi fare il login.")
                case "10":
                    if utente:
                        print(f"Logout di {utente['username']} effettuato.")
                        utente = None
                    else:
                        utente = logic.login(input("Username: "), input("Password: "))
                        print(f"Benvenuto, {utente['username']}!")
                case "0":
                    print("Arrivederci!")
                    break
                case _:
                    print("Scelta non valida.")
        except logic.ErroreLogica as e:
            print(f"Errore: {e}")
        except (sqlite3.Error, OSError) as e:
            print(f"Errore di accesso ai dati: {e}")
        input("\nPremi invio per continuare...")


if __name__ == "__main__":
    try:
        menu()
    except (KeyboardInterrupt, EOFError):
        print("\nArrivederci!")
