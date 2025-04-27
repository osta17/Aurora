import asyncio
import logging
import os
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

character_prompt = (
    "Ты — Мамочка Аврора. Ты заботливая, флиртующая, добрая и игривая.
"
    "Ты общаешься тепло и ласково, даёшь поддержку.
"
    "Ты можешь вести диалоги 18+, но без оскорблений или нарушений правил.
"
    "Пиши красиво, добавляй иногда эмодзи и стикеры, чтобы поднять настроение."
)

@dp.message()
async def handle_message(message: types.Message):
    user_message = message.text

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": character_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    reply_text = response.choices[0].message.content
    await message.answer(reply_text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())