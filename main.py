import json
import telebot
from telebot import types

#импорт доп файлов из папки нужны для токена и почт
import config
import utils


bot = telebot.TeleBot(config.BOT_TOKEN)

#выгрузка текста из файла /content.json
try:
    with open("content.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except Exception as e:
    print(f"Ошибка при чтении файла content.json: {e}")
    data = {}

#создание кнопок на клавиатуре
def create_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    #создание разделов информации обо мне
    btn_about = types.KeyboardButton("👋 О себе")
    btn_goal = types.KeyboardButton("🎯 Моя цель")
    btn_history = types.KeyboardButton("🚀 Как я пришел в IT")
    btn_mentor = types.KeyboardButton("👨‍🏫 Мой ментор")
    btn_progress = types.KeyboardButton("📈 Точка А -> Точка Б")
    btn_hobbies = types.KeyboardButton("🏀 Хобби и интересы")
    btn_works = types.KeyboardButton("💻 Мои работы")
    btn_github = types.KeyboardButton("🔗 Ссылка на GitHub")
    btn_email = types.KeyboardButton("✉️ Оставить контакт")
    
    #добавление кнопок в меню 
    markup.add(btn_about, btn_goal, btn_history, btn_mentor, btn_progress, btn_hobbies, btn_works, btn_github, btn_email)
    return markup

#ответ на команды /help & /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        f"Привет, {message.from_user.first_name}! Это бот-портфолио Тамирлана. Выбери интересующий раздел:", 
        reply_markup=create_keyboard()
    )

#ответы на кнопки их вытаскивает из файла /content.json если не находит нужного пишет заготовленый текст 
@bot.message_handler(content_types=['text'])
def handle_buttons(message):
    try:
        if message.text == "👋 О себе":
            bot.send_message(message.chat.id, data.get("about", "Информации пока нет."))
            
        elif message.text == "🎯 Моя цель":
            bot.send_message(message.chat.id, data.get("goal", "Информации пока нет."))
            
        elif message.text == "🚀 Как я пришел в IT":
            bot.send_message(message.chat.id, data.get("history", "Информации пока нет."))
            
        elif message.text == "👨‍🏫 Мой ментор":
            bot.send_message(message.chat.id, data.get("mentor", "Информации пока нет."))
            
        elif message.text == "📈 Точка А -> Точка Б":
            bot.send_message(message.chat.id, data.get("progress", "Информации пока нет."))
            
        elif message.text == "🏀 Хобби и интересы":
            bot.send_message(message.chat.id, data.get("hobbies", "Информации пока нет."))
            
        elif message.text == "💻 Мои работы":
            #РАБОТА 1: ИГРА НА PYGAME «ДИНО» (ВИДЕО)
            try:
                with open("dino_game.mp4", "rb") as video1:
                    bot.send_video(
                        message.chat.id, video1, 
                        caption="🕹️ **Проект 1: Игра на Pygame «Дино» (с аудиоэффектами)**\n\n"
                                "Описание: Аркадная игра со звуковым сопровождением. "
                                "Реализована обработка прыжков, анимация персонажей, генерация препятствий.\n"
                                "🎬 Посмотрите видео со звуком выше!"
                    )
            except FileNotFoundError:
                bot.send_message(message.chat.id, "🕹️ Проект 1: Видео dino_game.mp4 не найдено.")

            #РАБОТА 2: ОБУЧАЮЩИЕ КАРТОЧКИ (АЛЬБОМ ИЗ 2-Х КАРТИНОК)
            try:
                photo_c1 = open("python_cards_reg.png", "rb")
                photo_c2 = open("python_cards_vic.png", "rb")
                
                media_cards = [
                    types.InputMediaPhoto(photo_c1, caption="📇 **Проект 2: Программа «Обучающие карточки»**\n\n"
                                                            "Описание: Программа для эффективного запоминания любой информации. "
                                                            "Использует структуры данных (словари) и выводит статистику в конце."),
                    types.InputMediaPhoto(photo_c2)
                ]
                bot.send_media_group(message.chat.id, media_cards)
                
                photo_c1.close()
                photo_c2.close()
            except FileNotFoundError:
                bot.send_message(message.chat.id, "📇 Проект 2: Скриншоты карточек не найдены.")

            #РАБОТА 3: ТГ-БОТ НАПОМИНАНИЕ О ВОДЕ (ОДНА КАРТИНКА)
            try:
                with open("bot_reminder.png", "rb") as photo_w:
                    bot.send_photo(
                        message.chat.id, photo_w, 
                        caption="💧 **Проект 3: Telegram-бот «Water Reminder»**\n\n"
                                "Описание: Полезный бот, который помогает отслеживать дневную норму воды. "
                                "Реализованы команды /drank ... для отметки количества выпитой воды, "
                                "и /setreminder... для установки промежутка между напоминаниями выпить воды."
                    )
            except FileNotFoundError:
                bot.send_message(message.chat.id, "💧 Проект 3: Скриншот bot_reminder.png не найден.")
            
        elif message.text == "🔗 Ссылка на GitHub":
            bot.send_message(message.chat.id, data.get("github", "Информации пока нет."))
            
        elif message.text == "✉️ Оставить контакт":
            msg = bot.send_message(message.chat.id, "Пожалуйста, введите ваш email для связи:")
            bot.register_next_step_handler(msg, check_user_email)
            
        else:
            bot.send_message(message.chat.id, "Пожалуйста, выберите пункт из меню на кнопках.")
            
    except Exception as e:
        print(f"Произошла ошибка в обработчике: {e}")

#проверка почты пользователя 
def check_user_email(message):
    user_input = message.text
    
    #использование файла /utils.py для проверки структуры почты
    if utils.validate_email(user_input):
        bot.send_message(message.chat.id, f"✅ Спасибо! Email '{user_input}' успешно прошел валидацию.")
    else:
        bot.send_message(message.chat.id, "❌ Неверный формат email! Попробуйте заново через меню.")

#запуск бота и ожидание сообщений
if __name__ == "__main__":
    print("🤖 Бот успешно запущен локально...")
    bot.infinity_polling()
