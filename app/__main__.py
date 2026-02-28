"""Entry point: python -m app"""
from app.logging_config import setup_logging
from app.cli import app

setup_logging()

if __name__ == "__main__":
    app()
