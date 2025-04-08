import json
import os
from datetime import datetime
import uuid

# Cartella dove salviamo i JSON
CARTELLA_JSON = "output_json"
os.makedirs(CARTELLA_JSON, exist_ok=True)

def mock_risposta_llm(pdf_path):
    oggi = datetime.now().isoformat()
    nome_file = os.path.basename(pdf_path)
    file_id = str(uuid.uuid4())

    dati = {
        "id": file_id,
        "metadata": {
            "tecnico": {
                "filename": nome_file,
                "filetype": "pdf",
                "dimensione": "2MB",
                "data_creazione": "2024-12-01",
                "data_elaborazione": oggi,
                "origine": "digitale",
                "pagine": 8,
                "checksum": "sha256:abc123..."
            },
            "contestuale": {
                "titolo": "Contratto di locazione",
                "autori": ["Mario Rossi", "Luca Bianchi"],
                "lingua": "it",
                "tipo_documento": "Contratto"
            }
        },
        "contenuto": {
            "estratti": {
                "testo_raw": "Contratto di locazione per un periodo di 4 anni con condizioni di pagamento mensili...",
                "metodo_estrazione": "Mock-LLM"
            },
            "analisi_llm": {
                "riassunto": "Contratto di locazione per un periodo di 4 anni...",
                "parole_chiave": ["locazione", "canone", "durata", "garanzie", "penali"],
                "entita": {
                    "persone": ["Mario Rossi", "Luca Bianchi"],
                    "luoghi": ["Roma"],
                    "date": ["2024-12-01"]
                },
                "categorie": ["Legale", "Contratti", "Locazione"],
                "score_rilevanza": 4,
                "clausole_critiche": [
                    "Obbligo di pagamento canone mensile",
                    "Penale per ritardo pagamento"
                ]
            }
        },
        "tracciabilita": {
            "percorsi": {
                "originale": pdf_path,
                "json": f"{CARTELLA_JSON}/{file_id}.json",
                "estratti": f"{CARTELLA_JSON}/{file_id}.txt",
                "backup": f"s3://archivio-backup/2024/12/{nome_file}"
            },
            "log": [
                {
                    "timestamp": oggi,
                    "evento": "mock_elaborazione_llm",
                    "status": "completato",
                    "modello": "mock-llm",
                    "tempo_esecuzione": "0.2s"
                }
            ]
        }
    }

    # Salvataggio su file
    path_json = os.path.join(CARTELLA_JSON, f"{file_id}.json")
    with open(path_json, "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=2, ensure_ascii=False)

    print(f"✅ Mock JSON creato in: {path_json}")


if __name__ == "__main__":
    # Sostituisci con il tuo file reale o di test
    mock_risposta_llm(r"C:\Users\Anton\Desktop\PDF\1. Definizione del Dominio del Sistema Ontologico (1).pdf")    
