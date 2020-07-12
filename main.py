import telebot
from config import TG_TOKEN
from config import file1
from config import in1

bot = telebot.TeleBot(TG_TOKEN)
comms = ['start', 'add', 'del', 'out', 'clear', 'save', 'help']


@bot.message_handler(commands=['start'])
def start(message):
    send_mess = f"<b>Привет {message.from_user.first_name} {message.from_user.last_name}</b>,\nя - бот" \
                f"-напоминатель, буду хранить в себе твои планы на ближайшее время\nНапиши " \
                f"/help, чтобы узнать о поддерживаемых мной командах"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['add'])
def add(message):
    get_message_bot = message.text.strip()
    pos = get_message_bot.find("add") + 4
    if get_message_bot[pos:] in in1:
        send_mess = "Такая запись уже есть в списке ваших планов"
    else:
        in1.append(get_message_bot[pos:])
        file1.write("%s\n" % get_message_bot[pos:])
        send_mess = f"Запись <b>{get_message_bot[pos:]}</b> добавлена"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['del'])
def delete(message):
    get_message_bot = message.text.strip()
    pos = get_message_bot.find("del") + 4
    get_message_bot = get_message_bot[pos:]
    if get_message_bot in in1:
        in1.remove(get_message_bot)
        send_mess = "Запись удалена"
    else:
        send_mess = "Такой записи нет в списке"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['out'])
def out(message):
    if in1:
        in1.sort()
        for elems in in1:
            send_mess = elems
            bot.send_message(message.chat.id, send_mess, parse_mode='html')
    else:
        send_mess = "Нет записей"
        bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['clear'])
def clear(message):
    file1.truncate(0)
    in1.clear()
    send_mess = "Все записи удалены"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['save'])
def save(message):
    file1.truncate(0)
    in1.sort()
    for elems in in1:
        file1.write("%s\n" % elems)
    file1.truncate()
    send_mess = "Записи сохранены"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    send_mess = f"Добро пожаловать в бот-напоминатель, который хранит твои планы на " \
                f"ближайшее время.\nПоддерживаемые команды:\n /start - начало работы бота\n" \
                f"/add - добавить запись \n/del - удалить запись\n/out - вывести планы\n" \
                f"/clear - очистить записи из списка\n/save - сохранить записи в файле\n"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(content_types=['text'])
def say_not_supported(message):
    if "/" in message.text:
        send_mess = f"Я не знаю такой команды\nДля работы со мной напиши /help"
    else:
        send_mess = f"Привет, я бот-напоминатель, я работаю с командами, попробуй написать /start"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


bot.polling(none_stop=True)
