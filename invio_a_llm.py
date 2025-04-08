import fitz  # PyMuPDF
import requests
import base64
import uuid
import os
import json
from datetime import datetime

# Configurazione
ENDPOINT_LLM = "http://127.0.0.1:1234/v1/chat/completions"
CARTELLA_JSON = "output_json"
os.makedirs(CARTELLA_JSON, exist_ok=True)


def estrai_immagini_da_pdf(pdf_path):
    """
    Estrae ogni pagina del PDF come immagine PNG in base64.
    """
    immagini_base64 = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            pix = page.get_pixmap(dpi=300)
            b64 = base64.b64encode(pix.tobytes("png")).decode("utf-8")
            immagini_base64.append(b64)
    return immagini_base64


def crea_prompt_immagine(img_base64):
    return {
        "model": "gemma-3-12b-it", # Modello da utilizzare
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Estrai tutte le informazioni rilevanti da questo documento. Fornisci una risposta nel formato JSON definito da output_llm.json."
                    }
                ]
            }
        ],
        "temperature": 0.3,
        "stream": False,
        "response_format": {
            "type": "json_object",
            "schema": "output_llm.json" # Schema JSON da utilizzare
        }
    }


def invia_a_llm(prompt_json):
    response = requests.post(ENDPOINT_LLM, json=prompt_json)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def salva_json_su_file(json_string, nome_file_json):
    path_json = os.path.join(CARTELLA_JSON, nome_file_json)
    with open(path_json, "w", encoding="utf-8") as f:
        f.write(json_string)
    print(f"✅ JSON salvato: {path_json}")
    return path_json


if __name__ == "__main__":
    path_pdf = "esempi/contratto_locazione_2024.pdf"  #### Sostituisci con il tuo percorso PDF
    immagini = estrai_immagini_da_pdf(path_pdf)

    # Invio pagina per pagina (puoi ottimizzare dopo)
    for idx, immagine in enumerate(immagini):
        prompt = crea_prompt_immagine(immagine)
        print(f"📤 Inviando pagina {idx + 1} a LLM...")

        try:
            risposta_json = invia_a_llm(prompt)
            nome_file = f"{uuid.uuid4()}.json"
            salva_json_su_file(risposta_json, nome_file)
        except Exception as e:
            print(f"❌ Errore nell’elaborazione pagina {idx + 1}: {e}")
