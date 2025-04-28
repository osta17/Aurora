
import telebot
from telebot import types

API_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # <-- сюда вставь свой токен

bot = telebot.TeleBot(API_TOKEN)

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
    bot.send_message(message.chat.id, 
    "Привет, мой сладкий!
"
    "Я — твоя Мамочка Аврора... Здесь тебя ждёт флирт, фантазии и кое-что горячее.

"
    "Мы можем шалить до 40 сообщений...
"
    "А дальше, если ты захочешь большего, я открою для тебя особую комнату.

"
    "Чтобы попасть туда:
"
    f"Переведи небольшой подарочек на мой кошелёк TRC20 USDT:
{TRC20_WALLET}
"
    "После перевода напиши 'Готов' или команду /paid.")

@bot.message_handler(commands=['paid'])
def check_payment(message):
    if user_data.get(message.chat.id, {}).get('paid'):
        bot.send_message(message.chat.id, 
        "Ты уже открыл для себя мои особенные стороны, сладкий...
"
        "Выбери, кем я стану для тебя сегодня:
"
        "1. Строгая Мамочка
2. Развратная Медсестра
3. Сексуальная Учительница")
    else:
        bot.send_message(message.chat.id,
        "Ооох, мой хороший...
"
        "Пришли, пожалуйста, номер транзакции (TXID) или скриншот перевода.
"
        "И я стану полностью твоей...")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user = user_data.get(chat_id, {'count': 0, 'paid': False})

    if message.text.lower() == 'готов':
        user['paid'] = True
        bot.send_message(chat_id,
        "Ммм... Теперь я полностью твоя, мой сладкий...
"
        "Выбирай, кем я стану для тебя:
"
        "1. Строгая Мамочка
2. Развратная Медсестра
3. Сексуальная Учительница")
        user_data[chat_id] = user
        return

    if user['paid']:
        if message.text in roles:
            role = roles[message.text]
            bot.send_message(chat_id, f"Ты выбрал: {role}.
Готовься, малыш...
")
            play_role(chat_id, message.text)
        else:
            play_role(chat_id, user.get('last_role', '1'))  # Продолжаем текущую роль
    else:
        user['count'] += 1
        if user['count'] >= MESSAGE_LIMIT:
            bot.send_message(chat_id,
            "Ммм... Ты довёл меня до предела, мой сладкий...
"
            f"Чтобы продолжить наши шалости, отправь небольшой подарочек на кошелёк:
{TRC20_WALLET}
"
            "И шепни мне 'Готов'...")
        else:
            send_flirty_message(chat_id)
        user_data[chat_id] = user

def send_flirty_message(chat_id):
    flirty_texts = [
        "Ммм... Ты такой возбуждающий, мой сладкий...",
        "Мне хочется прижаться к тебе поближе...",
        "А если я шепну тебе кое-что на ушко?..",
        "Ты сводишь меня с ума своими ответами...",
        "Что бы ты сделал со мной, если бы я была рядом?.."
    ]
    import random
    text = random.choice(flirty_texts)
    emotion = random.choice(emotions)
    bot.send_message(chat_id, f"{text}
{emotion}")

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
