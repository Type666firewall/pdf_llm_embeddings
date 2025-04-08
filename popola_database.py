import sqlite3
import json
import os

def create_database(db_path="pdf_metadati.db"):
    """
    Crea il database SQLite e la tabella 'pdf_metadata' se non esiste.
    """
    # Connettiamo al database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Verifica se la tabella esiste
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pdf_metadata';")
    result = cur.fetchone()
    
    if result:
        print(f"✅ La tabella 'pdf_metadata' esiste già nel database '{db_path}'.")
    else:
        print(f"⚠️ La tabella 'pdf_metadata' non esiste. Creandola ora...")
        # Crea la tabella
        cur.execute('''
        CREATE TABLE IF NOT EXISTS pdf_metadata (
            id TEXT PRIMARY KEY,
            filename TEXT,
            filetype TEXT,
            dimensione TEXT,
            data_creazione TEXT,
            data_elaborazione TEXT,
            origine TEXT,
            pagine INTEGER,
            checksum TEXT,
            titolo TEXT,
            autori TEXT,
            lingua TEXT,
            tipo_documento TEXT,
            riassunto TEXT,
            parole_chiave TEXT,
            path_originale TEXT,
            path_json TEXT,
            path_estratti TEXT,
            backup TEXT
        )
        ''')
        conn.commit()
        print(f"✅ Tabella 'pdf_metadata' creata nel database '{db_path}'.")
    
    # Chiusura della connessione
    conn.close()
    

def popola_database_from_json(json_path, db_path="pdf_metadati.db"):
    """
    Legge il file JSON e inserisce (oppure aggiorna) i record nel database.
    """
    # Caricamento del JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Estrazione dei campi dalla sezione "metadata"
    doc_id = data.get("id")
    tecnico = data.get("metadata", {}).get("tecnico", {})
    contestuale = data.get("metadata", {}).get("contestuale", {})

    filename = tecnico.get("filename")
    filetype = tecnico.get("filetype")
    dimensione = tecnico.get("dimensione")
    data_creazione = tecnico.get("data_creazione")
    data_elaborazione = tecnico.get("data_elaborazione")
    origine = tecnico.get("origine")
    pagine = tecnico.get("pagine")
    checksum = tecnico.get("checksum")

    titolo = contestuale.get("titolo")
    autori = contestuale.get("autori")
    # Se 'autori' è una lista, li convertiamo in stringa separata da virgole
    if isinstance(autori, list):
        autori = ", ".join(autori)
    lingua = contestuale.get("lingua")
    tipo_documento = contestuale.get("tipo_documento")

    # Estrazione dei campi da "contenuto.analisi_llm"
    analisi = data.get("contenuto", {}).get("analisi_llm", {})
    riassunto = analisi.get("riassunto")
    parole_chiave = analisi.get("parole_chiave")
    if isinstance(parole_chiave, list):
        parole_chiave = ", ".join(parole_chiave)

    # Estrazione dei percorsi dalla sezione "tracciabilita.percorsi"
    percorsi = data.get("tracciabilita", {}).get("percorsi", {})
    path_originale = percorsi.get("originale")
    path_json_db = percorsi.get("json")
    path_estratti = percorsi.get("estratti")
    backup = percorsi.get("backup")

    # Inserimento nel database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
    INSERT OR REPLACE INTO pdf_metadata (
        id, filename, filetype, dimensione, data_creazione, 
        data_elaborazione, origine, pagine, checksum,
        titolo, autori, lingua, tipo_documento, riassunto, parole_chiave,
        path_originale, path_json, path_estratti, backup
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (doc_id, filename, filetype, dimensione, data_creazione,
          data_elaborazione, origine, pagine, checksum,
          titolo, autori, lingua, tipo_documento, riassunto, parole_chiave,
          path_originale, path_json_db, path_estratti, backup))
    conn.commit()
    conn.close()
    print(f"✅ Metadati dal file JSON '{json_path}' inseriti nel database '{db_path}'.")

if __name__ == "__main__":
    # Crea (o verifica) il database
    create_database()
    
    # Esegui il popola database per un file JSON
    # Usa raw string per i percorsi Windows
    popola_database_from_json(r"archivio\2024\12\Contratto\db1bc871-e7e8-4305-95ed-a776194a5039.json")
