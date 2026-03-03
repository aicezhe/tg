import os
import logging
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, Update
from aiogram.enums import ChatType

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ["TOKEN"]  # токен берём из переменной окружения

BAD_PHRASES = [
    "онлайн заработок",
    "онлайн заработка",
    "ищу людей для дистанционной работы",
    "удаленка",
    "attività lavorativa",
]

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
async def spam_filter(message: Message):
    if not message.text:
        return

    text = message.text.lower().strip()

    if any(phrase in text for phrase in BAD_PHRASES):
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id,
            )
        except Exception as e:
            logging.error(f"Не удалось удалить сообщение: {e}")

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я удаляю в группе сообщения с фразами: "
        "«онлайн заработок», «онлайн заработка», "
        "«ищу людей для дистанционной работы»."
    )

app = FastAPI()

@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/")
async def index():
    return {"status": "ok"}
