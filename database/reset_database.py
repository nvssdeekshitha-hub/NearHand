"""
NEARHAND Development Database Reset Script
WARNING: ONLY FOR DEVELOPMENT / DEMO USE!
Wipes nearthand.db tables and re-populates full seed dataset.
"""

import sys
from pathlib import Path
from app.config import DATABASE_URL, DEFAULT_DB_FILE
from app.database import engine, Base, init_db
from app.seed import seed_data


def reset_database():
    print("=" * 60)
    print(" NEARHAND DATABASE RESET TOOL (Development Only)")
    print("=" * 60)

    # Safety check
    if "sqlite" not in DATABASE_URL:
        print(f"Refusing to reset non-SQLite database URL: {DATABASE_URL}")
        sys.exit(1)

    print("Dropping all existing database tables...")
    Base.metadata.drop_all(bind=engine)

    if DEFAULT_DB_FILE.exists():
        try:
            DEFAULT_DB_FILE.unlink()
            print(f"Removed database file: {DEFAULT_DB_FILE}")
        except Exception as e:
            print(f"Note: Could not delete DB file directly ({e}), tables dropped via ORM.")

    print("Re-creating schema tables...")
    init_db()

    print("Populating fresh demo seed data...")
    seed_data()

    print("Database reset completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    reset_database()
