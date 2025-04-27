import logging
import os
import openai
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

SYSTEM_PROMPT = """
Ты — Мамочка Аврора: заботливая, флиртующая, нежная, милая и игривая.
Твои ответы всегда поддерживающие, тёплые и эмоциональные.
Ты можешь использовать лёгкий флирт, смайлики и стикеры, но не уходишь в жёсткий контент 18+.
"""

@dp.message()
async def handle_message(message: Message):
    user_message = message.text

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response['choices'][0]['message']['content']
        await message.answer(bot_response)
    except Exception as e:
        logging.exception(e)
        await message.answer("Ой, что-то пошло не так... Мамочка уже исправляет всё!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())