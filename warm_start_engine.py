#!/usr/bin/env python3
"""Warm start engine for ATI system."""
import json
import logging
import os
from pathlib import Path

import joblib
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

HOME_DIR = Path.home()
SOAP_ROOT_ENV = os.getenv("SOAP_ROOT")
SOAP_ROOT = Path(SOAP_ROOT_ENV).expanduser() if SOAP_ROOT_ENV else HOME_DIR / "Soap"
ROOT = SOAP_ROOT
VECTOR_DIR = ROOT / "vector_store"
LOG_FILE = ROOT / "data" / "logs" / "warm_start_engine.log"

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=str(LOG_FILE), level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

_vectorizer = None
_matrix = None
_doc_paths = None


def load_vectors():
    """Load TF-IDF vectorizer and matrix."""
    global _vectorizer, _matrix, _doc_paths
    vec_path = VECTOR_DIR / "vectorizer.pkl"
    matrix_path = VECTOR_DIR / "matrix.npz"
    doc_path = VECTOR_DIR / "doc_paths.json"
    if not vec_path.is_file() or not matrix_path.is_file() or not doc_path.is_file():
        logger.warning("Vector store missing")
        return None
    _vectorizer = joblib.load(vec_path)
    _matrix = sparse.load_npz(matrix_path)
    _doc_paths = json.loads(doc_path.read_text())
    logger.info("Loaded vector store with %d documents", len(_doc_paths))
    return _vectorizer, _matrix


def search_similar(text: str, top_k: int = 3) -> list[str]:
    """Return paths to top_k similar SOPs for the given text."""
    if _vectorizer is None or _matrix is None:
        if not load_vectors():
            return []
    query_vec = _vectorizer.transform([text])
    scores = cosine_similarity(query_vec, _matrix).flatten()
    order = scores.argsort()[::-1]
    results = []
    for idx in order[:top_k]:
        if scores[idx] <= 0:
            continue
        results.append(_doc_paths[idx])
    return results


if __name__ == "__main__":
    load_vectors()
