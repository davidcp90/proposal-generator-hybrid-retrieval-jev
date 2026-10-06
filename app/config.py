"""Settings, read from environment variables (app/.env is loaded if present)."""
import os
from pathlib import Path

from dotenv import load_dotenv

APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
load_dotenv(APP_DIR / ".env")

# Models (same defaults as the notebook)
MODEL = os.getenv("MODEL", "gpt-6-luna")                     # chat model with tool calling
EFFORT = os.getenv("EFFORT", "medium")                       # reasoning: "low" is cheaper and faster
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "gpt-image-2.5-flare")
SLIDE_QUALITY = os.getenv("SLIDE_QUALITY", "medium")         # "low" to save money
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")           # "turbo" if you have a GPU

# Jev guardrails
JEV_URL = os.getenv("JEV_URL", "https://jevtypesafeai.com/api/v1/decide")
PRICES_MIN = float(os.getenv("PRICES_MIN", "0.5"))           # below this, the answer is blocked
CONSTRAINTS_MIN = float(os.getenv("CONSTRAINTS_MIN", "0.5")) # below this, a proposal gets a warning

# Data
OKF_DIR = Path(os.getenv("OKF_DIR", ROOT / "okf"))
DATA_DIR = Path(os.getenv("DATA_DIR", APP_DIR / "data"))     # uploads and generated images
PRELOAD_TRANSCRIPT = os.getenv("PRELOAD_TRANSCRIPT", "")     # e.g. transcripcion_respaldo.json
PRELOAD_CLIENT = os.getenv("PRELOAD_CLIENT", "ritmofit")

# Server
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5002"))

UPLOAD_DIR = DATA_DIR / "uploads"
IMG_DIR = DATA_DIR / "images"


def require_keys():
    missing = [k for k in ("OPENAI_API_KEY", "JEV_API_KEY") if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing {', '.join(missing)}: copy app/.env.example to app/.env and fill it in")
