#!/usr/bin/env python3
"""Vectorize SOP texts using TF-IDF for warm start recall."""
import json
import logging
from pathlib import Path
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer


HOME_DIR = Path.home()
SOAP_ROOT = Path.getenv("SOAP_ROOT")
if not SOAP_ROOT:
    SOAP_ROOT = HOME_DIR / "Soap"
else:
    SOAP_ROOT = Path(SOAP_ROOT)

VECTOR_DIR = SOAP_ROOT / "vector_store"
SOPS_DIR = SOAP_ROOT / "overlay" / "sops"
LOG_FILE = SOAP_ROOT / "data" / "logs" / "rag_vectorizer.log"

VECTOR_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=str(LOG_FILE), level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def load_documents() -> List[str]:
    docs = []
    for path in SOPS_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text())
            doc = " ".join(data.get("procedure", []))
            if doc:
                docs.append(doc)
        except Exception as exc:
            logger.warning("Failed to load %s: %s", path, exc)
    return docs


def vectorize() -> None:
    docs = load_documents()
    if not docs:
        logger.info("No SOP documents found for vectorization")
        return
    vec = TfidfVectorizer(stop_words='english')
    matrix = vec.fit_transform(docs)
    # Save artifacts
    vocab_path = VECTOR_DIR / "vocab.json"
    matrix_path = VECTOR_DIR / "matrix.npz"
    with open(vocab_path, 'w') as f:
        json.dump(vec.vocabulary_, f)
    from scipy import sparse
    sparse.save_npz(matrix_path, matrix, compressed=True)
    logger.info("Vector store updated with %d documents", len(docs))


if __name__ == "__main__":
    vectorize()
