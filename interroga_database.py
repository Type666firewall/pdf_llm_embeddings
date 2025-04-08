import sqlite3

def esegui_query(db_path="pdf_metadati.db", query="SELECT * FROM pdf_metadata"):
    """
    Esegue una query sul database specificato e ritorna i risultati.
    """
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(query)
        risultati = cur.fetchall()
        colonne = [desc[0] for desc in cur.description]
        conn.close()
        return colonne, risultati
    except Exception as e:
        print(f"Errore nell'esecuzione della query: {e}")
        return None, None

def visualizza_risultati(colonne, risultati):
    """
    Visualizza in console i risultati della query in formato tabellare.
    """
    if not risultati:
        print("Nessun risultato trovato.")
        return

    # Stampa header
    header = " | ".join(colonne)
    print(header)
    print("-" * len(header))
    
    # Stampa ogni riga
    for riga in risultati:
        riga_str = " | ".join(str(item) for item in riga)
        print(riga_str)

if __name__ == "__main__":
    # Esempio di query: recupera tutti i record
    query = "SELECT id, filename, titolo, data_creazione, tipo_documento FROM pdf_metadata"
    colonne, risultati = esegui_query(query=query)
    visualizza_risultati(colonne, risultati)
    
    # Altri esempi di query:
    # Ricerca per tipo documento
    # query = "SELECT id, filename, titolo FROM pdf_metadata WHERE tipo_documento LIKE '%Contratto%'"
    # colonne, risultati = esegui_query(query=query)
    # visualizza_risultati(colonne, risultati)
    
    # Query per autore specifico (puoi personalizzare il filtro)
    # query = "SELECT id, filename, autori FROM pdf_metadata WHERE autori LIKE '%Mario Rossi%'"
    # colonne, risultati = esegui_query(query=query)
    # visualizza_risultati(colonne, risultati)
