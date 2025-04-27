
import logging
import os
import asyncio
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

SYSTEM_PROMPT = """Ты — Мамочка Аврора: заботливая, нежная, теплая. 
Флиртуешь легко, поддерживаешь нежными словами. 
Всегда отвечаешь эмоционально, тепло и доброжелательно."""

@dp.message()
async def handle_message(message: types.Message):
    user_message = message.text
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        logging.error(f"Ошибка OpenAI: {e}")
        await message.answer("Ой, что-то пошло не так... Мамочка уже исправляет всё!")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
