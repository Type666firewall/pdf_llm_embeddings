import fitz  # PyMuPDF

def is_pdf_nativo(file_path):
    try:
        doc = fitz.open(file_path)
        for page in doc:
            # Se la lunghezza del testo estratto è superiore a una soglia, ad es. 50 caratteri,
            # si ipotizza che ci sia testo nativo.
            text = page.get_text()
            if len(text.strip()) > 50:
                return True
        return False
    except Exception as e:
        # Gestione robusta degli errori
        print(f"Errore nell'apertura o lettura del PDF: {e}")
        return False

if __name__ == "__main__":
    # Inserisci qui il percorso del PDF da verificare
    path_pdf = input("Inserisci il percorso del PDF da verificare: ").strip("\"'")


    if is_pdf_nativo(path_pdf):
        print("✅ Il PDF è Nativo. Procedi con l’estrazione tramite PyMuPDF.")
    else:
        print("🧠 Il PDF è NON Nativo. Vai con l’elaborazione tramite Gemma.")
