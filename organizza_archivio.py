import json
import os
import shutil

def organizza_archivio(percorso_json, cartella_archivio="archivio"):
    # Carica il file JSON
    with open(percorso_json, "r", encoding="utf-8") as f:
        dati = json.load(f)

    doc_id = dati["id"]
    tipo_doc = dati["metadata"]["contestuale"]["tipo_documento"]
    data_creazione = dati["metadata"]["tecnico"]["data_creazione"]  # es. "2024-12-01"
    anno, mese, _ = data_creazione.split("-")
    nome_pdf_originale = dati["metadata"]["tecnico"]["filename"]

    cartella_destinazione = os.path.join(cartella_archivio, anno, mese, tipo_doc)
    os.makedirs(cartella_destinazione, exist_ok=True)

    # Percorsi definitivi
    nome_base = f"{doc_id}"
    percorso_pdf = os.path.join(cartella_destinazione, nome_base + ".pdf")
    percorso_json_nuovo = os.path.join(cartella_destinazione, nome_base + ".json")
    percorso_txt = os.path.join(cartella_destinazione, nome_base + ".txt")

    # Copia PDF originale
    shutil.copy(dati["tracciabilita"]["percorsi"]["originale"], percorso_pdf)

    # Scrivi file .txt con testo estratto
    with open(percorso_txt, "w", encoding="utf-8") as f_txt:
        f_txt.write(dati["contenuto"]["estratti"]["testo_raw"])

    # Aggiorna i percorsi nel JSON
    dati["tracciabilita"]["percorsi"]["originale"] = percorso_pdf
    dati["tracciabilita"]["percorsi"]["json"] = percorso_json_nuovo
    dati["tracciabilita"]["percorsi"]["estratti"] = percorso_txt

    # Scrivi JSON aggiornato nel nuovo percorso
    with open(percorso_json_nuovo, "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=2, ensure_ascii=False)

    print(f"✅ Archiviazione completata in: {cartella_destinazione}")


if __name__ == "__main__":
    # Usa r-string per evitare errori sui backslash
    organizza_archivio(r"output_json\db1bc871-e7e8-4305-95ed-a776194a5039.json")
    # Sostituisci con il tuo file JSON reale