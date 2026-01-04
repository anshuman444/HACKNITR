import platform

HAS_PATHWAY = False
if platform.system() != "Windows":
    try:
        import pathway as pw
        HAS_PATHWAY = True
    except (ImportError, ModuleNotFoundError):
        pass
else:
    pw = None

from ingestion.pdf_stream import pdf_stream
from parsing.pdf_parser import parse_pdf

class WindowsFallbackPipeline:
    def __init__(self, path="data/filings"):
        self.path = path

    def for_each(self, callback):
        import os
        if not os.path.exists(self.path):
            print(f"⚠️ Directory {self.path} not found. Skipping ingestion.")
            return

        for file_name in os.listdir(self.path):
            if file_name.endswith(".pdf"):
                file_path = os.path.join(self.path, file_name)
                with open(file_path, "rb") as f:
                    content = f.read()
                doc = parse_pdf(content, file_name)
                callback(doc)

def build_ingestion_pipeline():
    if HAS_PATHWAY:
        files = pdf_stream()

        parsed_docs = files.select(
            file_name=files.metadata["path"],
            content=files.data,
        ).map(
            lambda row: parse_pdf(row["content"], row["file_name"])
        )

        return parsed_docs
    else:
        print("🪟 Windows detected: Using fallback ingestion (No Pathway)")
        return WindowsFallbackPipeline()

