import logging
import os
import openai
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

SYSTEM_PROMPT = "Ты — Мамочка Аврора: заботливая, флиртующая, нежная помощница. Отвечаешь тепло, с лёгким флиртом, дружелюбно, иногда используешь смайлики."

@dp.message()
async def handle_message(message: types.Message):
    user_message = message.text
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        await message.answer(response["choices"][0]["message"]["content"])
    except Exception as e:
        logging.error(f"Ошибка OpenAI: {e}")
        await message.answer("Ой, что-то пошло не так... Мамочка уже всё исправляет!")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
