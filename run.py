from uvicorn import run

from app import app
from app.db import AsyncDB


if __name__ == "__main__":
    AsyncDB.migrate()
    run("run:app", port=8000)