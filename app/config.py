"""Load configuration from .env and expose model + API settings."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (parent of app/)
_root = Path(__file__).parent.parent
load_dotenv(_root / ".env")

APP_ENV: str = os.environ.get("APP_ENV", "dev").lower()

ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")

MODEL_TUTOR: str = os.environ.get("MODEL_TUTOR", "claude-sonnet-4-6")
MODEL_INTERVIEWER: str = os.environ.get("MODEL_INTERVIEWER", "claude-sonnet-4-6")
MODEL_GRADER: str = os.environ.get("MODEL_GRADER", "claude-sonnet-4-6")
MODEL_FIGURES: str = os.environ.get("MODEL_FIGURES", "claude-haiku-4-5-20251001")

LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
LOG_FILE: str = os.environ.get("LOG_FILE", "")

NOTES_DIR: Path = _root / "notes"
PROMPTS_DIR: Path = _root / "prompts"
PATTERNS_DIR: Path = _root / "patterns"
PROBLEMS_DIR: Path = _root / "problems"
DATA_DIR: Path = _root / "data"
MISTAKES_DIR: Path = _root / "mistakes"
DB_PATH: Path = DATA_DIR / "progress.db"
