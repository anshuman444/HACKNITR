from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
import tempfile
import os

# Initialize converter as a global to avoid overhead of re-creating it 
# for every document in a stream.
_CONVERTER = None

def get_converter():
    global _CONVERTER
    if _CONVERTER is None:
        # Simplest possible initialization to avoid internal attribute errors on Windows
        _CONVERTER = DocumentConverter()
    return _CONVERTER

def parse_pdf(file_bytes: bytes, file_name: str):
    """
    Parses a PDF into structured markdown text using Docling.
    """
    converter = get_converter()

    # Save temp file (Docling expects a file)
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file_name)
    
    try:
        with open(temp_path, "wb") as f:
            f.write(file_bytes)

        result = converter.convert(temp_path)

        # In latest docling, metadata might be in the result object or nested differently
        # We focus on the high-fidelity markdown export as requested.
        return {
            "file_name": file_name,
            "text": result.document.export_to_markdown(),
            "metadata": {}  # Simplified for version stability
        }
    except Exception as e:
        print(f"❌ Docling Error parsing {file_name}: {e}")
        return {
            "file_name": file_name,
            "text": f"Error parsing PDF: {str(e)}",
            "metadata": {}
        }
    finally:
        # Cleanup temp file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
