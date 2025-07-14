#!/usr/bin/env python3
"""Warm start engine for ATI system."""
import json
import logging
from pathlib import Path

from scipy import sparse

HOME_DIR = Path.home()
SOAP_ROOT = Path.getenv("SOAP_ROOT") or str(HOME_DIR / "Soap")
ROOT = Path(SOAP_ROOT)
VECTOR_DIR = ROOT / "vector_store"
LOG_FILE = ROOT / "data" / "logs" / "warm_start_engine.log"

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=str(LOG_FILE), level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def load_vectors():
    vocab_path = VECTOR_DIR / "vocab.json"
    matrix_path = VECTOR_DIR / "matrix.npz"
    if not vocab_path.is_file() or not matrix_path.is_file():
        logger.warning("Vector store missing")
        return None
    vocab = json.loads(vocab_path.read_text())
    matrix = sparse.load_npz(matrix_path)
    logger.info("Loaded vector store: %d terms", len(vocab))
    return vocab, matrix


if __name__ == "__main__":
    load_vectors()
