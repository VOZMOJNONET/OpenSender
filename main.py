from fastapi import FastAPI
from dotenv import load_dotenv
import asyncio
import aiosqlite as sq
import os

load_dotenv('.env')
DATABASE_NAME = os.getenv("DATABASE_NAME")
api = FastAPI()


async def init_db():
    async with sq.connect(DATABASE_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER UNIQUE,
        username TEXT
        )
        ''')
        await db.commit()


async def add_user(chat_id: int, username: str) -> None:
    async with sq.connect(DATABASE_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (chat_id, username) VALUES (?, ?)",
            (chat_id, username)
        )
        await db.commit()
        print(f"Юзер {username} обработан.")


async def main():
    await init_db()
    i, name = input().split()
    await add_user(int(i), name)


if __name__ == '__main__':
    asyncio.run(main())
