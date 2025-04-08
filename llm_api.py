import requests
import json

LM_STUDIO_URL = "http://127.0.0.1:1234"

def predict_text(text, model="gemma-3-12b-it", schema="contratti.json"):
    """
    Invia il testo all'endpoint /api/v1/predict per ottenere una risposta strutturata.
    """
    url = f"{LM_STUDIO_URL}/api/v1/predict"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "text": text,
        "model": model,
        "response_format": "json_object",
        "schema": schema
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Errore predict: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Errore durante la richiesta predict: {e}")
        return None

def get_embeddings(text, model="gemma-3-12b-it"):
    """
    Invia il testo all'endpoint /api/v1/embeddings e restituisce gli embeddings.
    """
    url = f"{LM_STUDIO_URL}/api/v1/embeddings"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "text": text,
        "model": model
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            return json_data.get("embeddings", [])
        else:
            print(f"Errore embeddings: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Errore durante la richiesta embeddings: {e}")
        return None
