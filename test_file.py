import json
import os
import time

import telebot.util
from telebot import TeleBot
from telebot.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    MessageReactionUpdated,
    ReactionTypeEmoji,
)
from telebot.util import update_types
from telebot.storage import StateRedisStorage
from telebot.custom_filters import SimpleCustomFilter
import fastapi
import uvicorn
import requests
import dotenv


dotenv.load_dotenv()  # завантажуємо змінні з .env до змінних середовища
TOKEN = os.getenv("BOT_TOKEN")  # отримуємо зі змінної середовища токен

WEBHOOK_HOST = "https://molly-hot-heavily.ngrok-free.app"

bot: TeleBot = TeleBot(TOKEN)

app = fastapi.FastAPI(docs=None, redoc_url=None)


@app.post(f"/bot")
def process_webhook(update: dict):
    """
    Process webhook calls
    """
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


@app.post("/")
@app.get("/")
def hello():
    return "Hello World!"


@bot.message_handler(commands=["start"])
def start_action(message: Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Привіт, {message.from_user.first_name}. Радий вітати тебе в боті.\n"
        f"Можеш вибрати одну з дій за допомогою кнопок",
    )


if __name__ == "__main__":
    bot.set_webhook(
        url=f"{WEBHOOK_HOST}/bot",
        allowed_updates=update_types,
        drop_pending_updates=True,
    )

    uvicorn.run(app, port=5000)
