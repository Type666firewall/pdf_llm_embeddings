import requests
import json
import time
import os

# Funzione per inviare la richiesta al server LM Studio
def estrai_testo_con_llm(pdf_path):
    url = "http://127.0.0.1:1234"  # Indirizzo del server LM Studio
    headers = {"Content-Type": "application/json"}
    
    # Prepara i dati da inviare a LM Studio
    dati = {
        "action": "process_document",
        "document": {
            "type": "pdf",  # Tipo di documento
            "path": pdf_path
        },
        "model": "gemma-3-12b-it",  # Usa il modello gemma-3-12b-it
        "response_format": {
            "type": "json_object",
            "schema": "contratti.json"
        }
    }

    try:
        # Invia la richiesta al server LM Studio
        response = requests.post(url, json=dati, headers=headers)
        
        if response.status_code == 200:
            # Ricevi il JSON di risposta
            json_data = response.json()
            
            # Verifica se il modello ha prodotto una risposta valida
            if "contenuto" in json_data:
                estratto_testo = json_data['contenuto']['estratti']['testo_raw']
                return estratto_testo
            else:
                print("Errore: Il modello non ha prodotto un testo valido.")
                return None
        else:
            print(f"Errore nel contattare LM Studio: {response.status_code}")
            return None
    except Exception as e:
        print(f"Errore durante la richiesta: {e}")
        return None

# Funzione principale per elaborare il PDF
def elabora_pdf(pdf_path):
    print(f"Elaborando il file: {pdf_path} con LM Studio...")
    testo_estratto = estrai_testo_con_llm(pdf_path)
    
    if testo_estratto:
        print(f"Testo estratto: {testo_estratto[:500]}...")  # Stampa solo i primi 500 caratteri per controllo
        return testo_estratto
    else:
        print(f"Impossibile estrarre testo dal PDF: {pdf_path}")
        return None

if __name__ == "__main__":
    # Percorso del file PDF non nativo
    pdf_path = "percorso/del/pdf_non_nativo.pdf"
    
    # Esegui l'elaborazione del PDF
    testo_estratto = elabora_pdf(pdf_path)
    
    if testo_estratto:
        # Qui puoi continuare a processare il testo estratto, salvarlo o fare altre operazioni
        print("Testo estratto con successo!")
    else:
        print("L'elaborazione del PDF non ha avuto successo.")
