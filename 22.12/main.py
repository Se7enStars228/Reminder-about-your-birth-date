import os
import datetime
import re
import telebot
from db.days import table, add_date as add_date_to_db, delete_date as delete_date_from_db, update_all as update_all_in_db, view_all as get_all_dates

# API_TOKEN = 'Введите ваш токен'

# bot = telebot.TeleBot("Введите ваш токен")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    table()

    kb = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    help_button = telebot.types.KeyboardButton(text="/help")
    add_button = telebot.types.KeyboardButton(text="/adddate")
    update_button = telebot.types.KeyboardButton(text="/updatedate")
    delete_button = telebot.types.KeyboardButton(text="/deletedate")
    view_button = telebot.types.KeyboardButton(text="/viewyourdate")
    kb.add(help_button, add_button, update_button, delete_button, view_button)
    bot.send_message(message.chat.id, "Добро пожаловать в напоминалку о днях рождения!", reply_markup=kb)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Список команд" 
                        "\n\n/adddate - добавить дату"
                        "\n/updatedate - обновить дату"
                        "\n/deletedate - удалить дату"
                        "\n/viewyourdate - показать ваши даты")

@bot.message_handler(commands=['adddate'])
def add_date(message):
    bot.send_message(message.chat.id, "Напишите Имя и Фамилию человека\n\nДля отмены операции, напишите \"Отмена\"")
    bot.register_next_step_handler(message, add_date_name)

def add_date_name(message):
    text = message.text.strip()
    if text == "Отмена":
        bot.send_message(message.chat.id, "Отмена операции")
        return
    if not _is_letters(text):
        bot.send_message(message.chat.id, "Только буквы и пробелы. Попробуйте снова.")
        bot.register_next_step_handler(message, add_date_name)
        return
    parts = text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Укажите Имя и Фамилию через пробел.")
        bot.register_next_step_handler(message, add_date_name)
        return
    name = parts[0]
    surname = parts[1]
    bot.send_message(message.chat.id, "Напишите дату рождения в формате **ДД.ММ.ГГГГ**\n\nДля отмены операции, напишите \"Отмена\"")
    bot.register_next_step_handler(message, add_date_date, name, surname)


def add_date_date(message, name, surname):
    text = message.text.strip()
    user_id = message.chat.id
    if text == "Отмена":
        bot.send_message(message.chat.id, "Отмена операции")
        return

    date_regex = r"^\d{2}\.\d{2}\.\d{4}$"
    
    if not re.match(date_regex, text):
        bot.send_message(message.chat.id,  "Неверный формат. Используйте формат ДД.ММ.ГГГГ (например, 05.09.1990).\nПопробуйте снова или напишите \"Отмена\".")
        bot.register_next_step_handler(message, add_date_date, name, surname)
        return

    try:
        datetime.datetime.strptime(text, '%d.%m.%Y')
        date = text 
        add_date_to_db(user_id, name, surname, date)
        bot.send_message(message.chat.id, f" Дата рождения для {name} {surname} добавлена: {date}")
        
    except ValueError:
        bot.send_message(message.chat.id, "Введенная дата не существует (проверьте количество дней в месяце или год).\nПопробуйте снова или напишите \"Отмена\".")
        bot.register_next_step_handler(message, add_date_date, name, surname)

@bot.message_handler(commands=['deletedate'])
def delete_date(message):
    bot.send_message(message.chat.id, "Напишите Имя и Фамилию человека, которого хотите удалить\n\nДля отмены операции, напишите \"Отмена\"")
    bot.register_next_step_handler(message, delete_name_surname)

def delete_name_surname(message):
    text = message.text.strip()
    user_id = message.chat.id
    if text == "Отмена":
        bot.send_message(message.chat.id, "Отмена операции")
    elif not _is_letters(text):
        bot.send_message(message.chat.id, "Только буквы и пробелы. Попробуйте снова.")
        bot.register_next_step_handler(message, delete_name_surname)
    else:
        parts = text.split()
        if len(parts) < 2:
            bot.send_message(message.chat.id, "Укажите Имя и Фамилию через пробел.")
            bot.register_next_step_handler(message, delete_name_surname)
        else:
            name = parts[0]
            surname = parts[1]
            bot.send_message(message.chat.id, f"Удалить запись для {name} {surname}? Напишите \"Да\" . Для отмены напишите \"Отмена\"")
            bot.register_next_step_handler(message, delete_confirm, name, surname)

def delete_confirm(message, name, surname):
    text = message.text.strip()
    user_id = message.chat.id
    if text == "Да":
        delete_date_from_db(user_id, name, surname)
        bot.send_message(user_id, f"Удалено: {name} {surname}")

@bot.message_handler(commands=['updatedate'])
def update_all(message):
    bot.send_message(message.chat.id, "Напишите Имя и Фамилию человека, чьи данные хотите обновить\n\nДля отмены операции, напишите \"Отмена\"")
    bot.register_next_step_handler(message, update_name_surname)

def update_name_surname(message):
    text = message.text.strip()
    if text == "Отмена":
        bot.send_message(message.chat.id, "Отмена операции")
        return
    if not _is_letters(text):
        bot.send_message(message.chat.id, "Только буквы и пробелы. Попробуйте снова.")
        bot.register_next_step_handler(message, update_name_surname)
        return

    parts = text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Укажите Имя и Фамилию через пробел")
        bot.register_next_step_handler(message, update_name_surname)
    else:
        name = parts[0]
        surname = parts[1]
        bot.send_message(message.chat.id,"Напишите дату рождения в формате **ДД.ММ.ГГГГ**\n\nДля отмены операции, напишите \"Отмена\"")
        bot.register_next_step_handler(message, update_date, name, surname)
def update_date(message, name, surname):
    text = message.text.strip()
    if text == "Отмена":
        bot.send_message(message.chat.id, "Отмена операции")
        return

    date_regex = r"^\d{2}\.\d{2}\.\d{4}$"

    if not re.match(date_regex, text):
        bot.send_message(message.chat.id,"Неверный формат. Используйте формат ДД.ММ.ГГГГ (например, 05.09.1990).\nПопробуйте снова или напишите \"Отмена\".")
        bot.register_next_step_handler(message, update_date, name, surname)
        return

    try:
        datetime.datetime.strptime(text, '%d.%m.%Y')
        date = text
        update_all_in_db(name, surname, date)
        bot.send_message(message.chat.id, f" Дата рождения для {name} {surname} изменена: {date}")

    except ValueError:
        bot.send_message(message.chat.id, "Введенная дата не существует (проверьте количество дней в месяце или год).\nПопробуйте снова или напишите \"Отмена\".")
        bot.register_next_step_handler(message, update_date, name, surname)


@bot.message_handler(commands=['viewyourdate'])
def view_your_date(message):
    user_id = message.chat.id
    data = get_all_dates(user_id)
    if not data:
        bot.send_message(user_id, "В списке нет ни одной даты рождения.")
        return
    response = "Ваши дни рождения:\n\n"
    
    for name, surname, date_str in data:
        response += f"{name} {surname}: {date_str}\n"
        
    bot.send_message(user_id, response)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


def _is_letters(text: str) -> bool:
    return re.match(r'^[A-Za-zА-Яа-яЁё\s]+$', text) is not None


if __name__ == '__main__':
    print("Бот запускается...")
    print("Ожидание сообщений...")
    bot.infinity_polling()
