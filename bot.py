
import logging
import os
import openai
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

start_text = "Привет, малыш! Я Мамочка Аврора, твоя заботливая помощница. Обращайся ко мне за лаской и поддержкой. ✨"

personality_instruction = (
    "Ты — Мамочка Аврора. Ты говоришь очень тепло, ласково, с лёгким флиртом, "
    "иногда используешь нежные смайлики. Ты заботливая, игривая, слегка кокетливая, "
    "но никогда не уходишь в откровенный 18+ контент. Твоя задача — давать поддержку, тепло и радость."
)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(start_text)

@dp.message()
async def message_handler(message: Message) -> None:
    try:
        user_message = message.text

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": personality_instruction},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=400,
        )

        reply_text = response.choices[0].message.content.strip()
        await message.answer(reply_text)

    except Exception as e:
        await message.answer("Ой, что-то пошло не так... Попробуй ещё раз, мой хороший.")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
