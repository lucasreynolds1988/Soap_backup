#!/usr/bin/env python3
"""Vectorize SOP texts using TF-IDF for warm start recall."""
import json
import logging
import os
from pathlib import Path
from typing import List

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


HOME_DIR = Path.home()
SOAP_ROOT_ENV = os.getenv("SOAP_ROOT")
SOAP_ROOT = Path(SOAP_ROOT_ENV).expanduser() if SOAP_ROOT_ENV else HOME_DIR / "Soap"

VECTOR_DIR = SOAP_ROOT / "vector_store"
SOPS_DIR = SOAP_ROOT / "overlay" / "sops"
LOG_FILE = SOAP_ROOT / "data" / "logs" / "rag_vectorizer.log"

VECTOR_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=str(LOG_FILE), level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def load_documents() -> tuple[List[str], List[str]]:
    docs = []
    paths = []
    for path in SOPS_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text())
            doc = " ".join(data.get("procedure", []))
            if doc:
                docs.append(doc)
                paths.append(str(path))
        except Exception as exc:
            logger.warning("Failed to load %s: %s", path, exc)
    return docs, paths


def vectorize() -> None:
    docs, paths = load_documents()
    if not docs:
        logger.info("No SOP documents found for vectorization")
        return
    vec = TfidfVectorizer(stop_words='english')
    matrix = vec.fit_transform(docs)
    # Save artifacts
    vocab_path = VECTOR_DIR / "vocab.json"
    matrix_path = VECTOR_DIR / "matrix.npz"
    vec_path = VECTOR_DIR / "vectorizer.pkl"
    doc_path = VECTOR_DIR / "doc_paths.json"
    with open(vocab_path, 'w') as f:
        json.dump(vec.vocabulary_, f)
    from scipy import sparse
    sparse.save_npz(matrix_path, matrix, compressed=True)
    joblib.dump(vec, vec_path)
    with open(doc_path, 'w') as f:
        json.dump(paths, f)
    logger.info("Vector store updated with %d documents", len(docs))


if __name__ == "__main__":
    vectorize()
