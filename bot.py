import logging
import os
import openai
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

SYSTEM_PROMPT = """Ты — Мамочка Аврора: заботливая, игривая, добрая, ласковая.
Флиртуешь легко, поддерживаешь нежными словами, но не уходишь в жёсткий 18+.
Всегда отвечаешь тепло, эмоционально, добавляешь эмодзи и стикеры в сообщения."""

@dp.message()
async def handle_message(message: types.Message):
    user_message = message.text
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=500
        )
        reply = response['choices'][0]['message']['content']
        await message.answer(reply)
    except Exception as e:
        await message.answer("Ой, у Авроры случилась ошибка... Попробуй позже!")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
