import pathway as pw

def build_live_index(docs):
    return pw.ml.index.KNNIndex(docs, dims=1536, metric="cosine")
