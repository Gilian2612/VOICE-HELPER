"""Configuración central: variables de entorno, rutas y constantes."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# --- API keys ---
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# --- Rutas ---
CVS_DIR = BASE_DIR / "cvs"
CHROMA_DIR = BASE_DIR / "data" / "chroma"

# --- Audio ---
SAMPLE_RATE = 16_000  # Hz que se envían a Deepgram
CHANNELS = 1
CHUNK_MS = 100  # tamaño de cada bloque de audio enviado

# --- LLM ---
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")


def require_keys() -> None:
    """Falla temprano si faltan las API keys."""
    missing = [
        name
        for name, value in (
            ("DEEPGRAM_API_KEY", DEEPGRAM_API_KEY),
            ("ANTHROPIC_API_KEY", ANTHROPIC_API_KEY),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(f"Faltan variables en .env: {', '.join(missing)}")
