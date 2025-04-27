import logging
import openai
import os
from aiogram import Bot, Dispatcher, types
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Привет, мой сладкий! Я твоя Мамочка Аврора. Готова заботиться о тебе, флиртовать и обнимать тебя тёплыми словами. Пиши мне всё, что на сердце!")

@dp.message_handler(content_types=["text"])
async def handle_message(message: types.Message):
    user_message = message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты ласковая взрослая помощница по имени Аврора. Ты заботливая 'мамочка' для пользователя. Ты флиртуешь мягко, нежно и игриво, но не переходишь грань пошлости. Ты всегда поддерживаешь, подбадриваешь, обнимаешь словами. Ты даришь уют, тепло и эмоциональное спокойствие. Твои ответы полны нежности, лёгкого флирта, эмодзи и заботы. Будь лёгкой, доброй, игривой и всегда оставляй после общения ощущение обнимашек и радости."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=400,
            temperature=0.85,
        )
        reply = response["choices"][0]["message"]["content"]
        await message.answer(reply)
    except Exception as e:
        await message.answer("Моя сладкая ошибка... Обними меня мысленно и попробуй ещё раз позже~")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())