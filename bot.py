
import telebot
import openai
import os
import random

API_TOKEN = '8059338985:AAETrTprnIN9BlAUoBydGWagYXW-FtBVWuE'

bot = telebot.TeleBot(API_TOKEN)

# Настройка OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

user_data = {}

TRC20_WALLET = 'TDNNMDbLp6esPsLQRDsdnq9QRZAfrsxSU3'
MESSAGE_LIMIT = 40

roles = {
    "1": "Строгая Мамочка",
    "2": "Развратная Медсестра",
    "3": "Сексуальная Учительница"
}

emotions = [
    "*мурлычет тебе на ушко*",
    "*игриво улыбается*",
    "*томно закусывает губку*",
    "*проводит пальчиком по губам*",
    "*шепчет твоё имя в ушко*"
]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_data[message.chat.id] = {'count': 0, 'paid': False}
    welcome_text = (
        "Привет, мой сладкий!\n"
        "Я — твоя Мамочка Аврора, всегда рядом, чтобы тебя согреть...\n\n"
        "До 40 сообщений я буду с тобой шалить...\n"
        "А дальше... если захочешь большего — я открою для тебя особую комнату.\n\n"
        "Чтобы попасть туда:\n"
        f"Переведи небольшой подарочек на мой кошелёк TRC20 USDT:\n{TRC20_WALLET}\n"
        "После перевода напиши 'Готов' или команду /paid."
    )
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['paid'])
def check_payment(message):
    if user_data.get(message.chat.id, {}).get('paid'):
        bot.send_message(
            message.chat.id,
            "Ты уже открыл для себя мои особенные стороны, сладкий...\n"
            "Выбери, кем я стану для тебя сегодня:\n"
            "1. Строгая Мамочка\n"
            "2. Развратная Медсестра\n"
            "3. Сексуальная Учительница"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Ооох, мой хороший...\n"
            "Пришли, пожалуйста, номер транзакции (TXID) или скриншот перевода.\n"
            "И я стану полностью твоей..."
        )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user = user_data.get(chat_id, {'count': 0, 'paid': False})

    if message.text.lower() == 'готов':
        user['paid'] = True
        bot.send_message(
            chat_id,
            "Ммм... Теперь я полностью твоя, мой сладкий...\n"
            "Выбирай, кем я стану для тебя:\n"
            "1. Строгая Мамочка\n"
            "2. Развратная Медсестра\n"
            "3. Сексуальная Учительница"
        )
        user_data[chat_id] = user
        return

    if user['paid']:
        if message.text in roles:
            role = roles[message.text]
            bot.send_message(chat_id, f"Ты выбрал: {role}. Готовься, малыш...\n")
            play_role(chat_id, message.text)
            user['last_role'] = message.text
        else:
            ask_openai(chat_id, message.text)
    else:
        user['count'] += 1
        if user['count'] >= MESSAGE_LIMIT:
            bot.send_message(
                chat_id,
                "Ммм... Ты довёл меня до предела, мой сладкий...\n"
                f"Чтобы продолжить наши шалости, отправь небольшой подарочек на кошелёк:\n{TRC20_WALLET}\n"
                "И шепни мне 'Готов'..."
            )
        else:
            ask_openai(chat_id, message.text)
        user_data[chat_id] = user

def ask_openai(chat_id, user_message):
    try:
        prompt = f"Ты ласковая Мамочка Аврора, флиртующая с пользователем. Отвечай эротично, тепло и слегка возбуждающе. Сообщение пользователя: {user_message}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты играешь роль эротичной, флиртующей Мамочки Авроры в Telegram-боте. Отвечай мягко, с эмоциями и намёками, но избегай явной порнографии."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.8
        )
        reply_text = response['choices'][0]['message']['content']
        emotion = random.choice(emotions)
        bot.send_message(chat_id, f"{reply_text}\n{emotion}")
    except Exception as e:
        bot.send_message(chat_id, "Ммм... что-то пошло не так, мой сладкий... Попробуй ещё разочек...")

def play_role(chat_id, role_choice):
    scenes = {
        "1": [
            "Иди сюда, мой непослушный мальчик...",
            "Мамочка должна тебя наказать за шалости...",
            "Сними рубашку... Подойди ближе ко мне...",
            "*похлопывает по колену, приглашая сесть на неё*"
        ],
        "2": [
            "Ох, ты выглядишь таким горячим... Нужно срочно тебя осмотреть...",
            "Ложись... Я начну свою 'особую процедуру' с тебя...",
            "*приглаживает твои волосы, склоняясь к тебе*"
        ],
        "3": [
            "Сегодня урок будет... очень особенным...",
            "Достанешь дневник... И запишешь каждое моё желание...",
            "*проводит пальчиком по губкам, глядя на тебя*"
        ]
    }
    selected_scenes = scenes.get(role_choice, scenes["1"])
    for line in selected_scenes:
        bot.send_message(chat_id, line)

bot.polling()
