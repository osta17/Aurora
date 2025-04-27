import logging
import openai
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = "sk-J0J1aESeGkzP2wL9YtG5T3c5lMzFND6V1BdHTWz9k5uQGpV0"

openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Иди ко мне, малыш, Мамочка всегда рядом.\nЯ скучала по тебе...")

@dp.message_handler(content_types=['text'])
async def handle_message(message: types.Message):
    try:
        user_message = message.text

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — Мамочка Аврора: заботливая, нежная, ласковая, с лёгким флиртом, но без откровенного 18+ контента."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.8
        )

        reply_text = response['choices'][0]['message']['content']
        await message.answer(reply_text)

    except Exception as e:
        logging.error(f"Ошибка общения с OpenAI: {e}")
        await message.answer("Ой, малыш, кажется небольшая заминка... Попробуй ещё раз.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
