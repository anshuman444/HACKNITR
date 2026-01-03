import json
import os

STORE_FILE = "data/document_store.json"

def _load_store():
    if not os.path.exists(STORE_FILE):
        return {}
    try:
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def _save_store(store):
    os.makedirs(os.path.dirname(STORE_FILE), exist_ok=True)
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2)

def store_document(doc):
    store = _load_store()
    store[doc["file_name"]] = doc
    _save_store(store)
    print(f"📄 Ingested and Persisted: {doc['file_name']}")

def get_all_documents():
    return _load_store()
