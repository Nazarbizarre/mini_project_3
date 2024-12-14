import asyncio

from uvicorn import run

from app import app
from app.db import AsyncDB


async def db_migrate():
    await AsyncDB.migrate()


if __name__ == "__main__":
    asyncio.run(db_migrate())
    run("run:app", port=8000)
