import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# Database URL default to SQLite file in database directory
DEFAULT_DB_FILE = BASE_DIR / "nearthand.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_FILE}")

DEFAULT_MAX_CARETAKER_SENIORS = int(os.getenv("DEFAULT_MAX_CARETAKER_SENIORS", 5))
ENV = os.getenv("ENV", "development")
