from ingestion.ingest_pipeline import build_ingestion_pipeline
from indexing.document_store import store_document

docs = build_ingestion_pipeline()

docs.for_each(store_document)

print("📡 AuditFlow ingestion pipeline is LIVE")
