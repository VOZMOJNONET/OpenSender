import aiosqlite
from dotenv import load_dotenv
import os
import asyncio



class EmailSender:
    def __init__(self, db_name: str = None):
        load_dotenv('.env')
        if db_name is None:
            self.DB_NAME = os.getenv('EMAIL_DATABASE_NAME')
        else:
            self.DB_NAME = db_name

    async def init_db(self) -> None:
        async with aiosqlite.connect(self.DB_NAME) as db:
            await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        "group" TEXT
        )''')
            await db.commit()

    async def add_user(self, email: str, group: str) -> None:
        async with aiosqlite.connect(self.DB_NAME) as db:
            await db.execute('''INSERT OR IGNORE INTO users (email, "group") VALUES (?, ?)''', (email, group))
            await db.commit()

    async def get_emails(self, group: str) -> list:
        async with aiosqlite.connect(self.DB_NAME) as db:
            async with db.execute('''SELECT email FROM users WHERE "group" = ?''', (group,)) as cursor:
                rows = await cursor.fetchall()
                emails = [row[0] for row in rows]
                return emails

async def main():
    sender = EmailSender()
    await sender.init_db()
    await sender.add_user('timalaluskin@gmail.com', 'staff')
    print(await sender.get_emails('staff'))

if __name__ == '__main__':
    asyncio.run(main())