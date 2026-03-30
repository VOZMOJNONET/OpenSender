import aiosqlite
from dotenv import load_dotenv
import os
import asyncio
from email.message import EmailMessage
import aiosmtplib


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
        id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
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

    # async def send_mail(self, to: str) -> None:
    #     # Формируем структуру письма
    #     message = EmailMessage()
    #     message["From"] = "opensender@send.org"
    #     message["To"] = "timalaluskin@gmail.com"
    #     message["Subject"] = "Привет из асинхронности!"
    #     message.set_content("Это текст письма, отправленного через aiosmtplib.")
    #
    #     # Отправка
    #     await aiosmtplib.send(
    #         message,
    #         hostname=os.getenv('MAIL_HOST'),  # Замените на ваш SMTP-сервер
    #         port=int(os.getenv('MAIL_PORT')),
    #         username=os.getenv("MAIL_LOGIN"),
    #         password=os.getenv("MAIL_PASS"),
    #         use_tls=bool(os.getenv("TLS"))
    #     )


async def main():
    sender = EmailSender()
    await sender.init_db()
    await sender.add_user('timalaluskin@gmail.com', 'staff')
    await sender.add_user('ivanoduvan21@gmail.com', 'family')
    print(await sender.get_emails('staff'))
    print(await sender.get_emails('family'))
    # await sender.send_mail('LTE')


if __name__ == '__main__':
    asyncio.run(main())
