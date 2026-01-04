import platform
if platform.system() != "Windows":
    try:
        import pathway as pw
    except ImportError:
        pw = None
else:
    pw = None

def pdf_stream(path="data/filings"):
    """
    Watches a folder for PDF files in real-time.
    Any new or updated PDF is streamed automatically.
    """
    if pw is None:
        return None

    return pw.io.fs.read(
        path,
        format="binary",
        with_metadata=True,
        mode="streaming"
    )
