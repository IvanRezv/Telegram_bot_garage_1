import telebot
import time
from telebot import types
from string import Template
from re import *

# Назначаем боту наш токен
bot = telebot.TeleBot('1858986723:AAHq-n_dtq4QovlJ1s8lDGk6sbyVw2d-2MY')


inc_type = []  # Хранит в себе тип заявки
cli_num = []  # Хранит в себе номер телефона заявителя
cli_mail = []  # Хранит в себе почту заявителя
hello_count = []  # Хранит в себе данные о том нужно ли здороваться с пользователем


# Основной хендлер который реагирует на команду страт
@bot.message_handler(commands=['start'])
def statup(message):  # Здороваемся и просим ввести номер или почту
    key1 = types.ReplyKeyboardMarkup(True, False)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    key1.row(button_phone)
    key1.row('Ввести почту')
    key1.one_time_keyboard = True
    if len(hello_count) == 0:  # Проверяем здоровались ли мы ранее
        bot.send_message(message.chat.id,
                         "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, официальный чат-бот СТО "
                         "'Гараж 1'. "
                         " Отправте свой номер телефона или почту, чтоб я понял, что вы человек".format(
                             message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=key1)

    elif message.text == 'Ⓜ Главное меню':
        pre_main(message)

    else:
        bot.send_message(message.chat.id,
                         "Выберете средство для авторизации, чтоб начать работу ".format(
                             message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=key1)
    hello_count.insert(1, 1)  # Отмечаем факт приветствия


@bot.message_handler(content_types=['text', 'contact'])  # Основной обработчик
def phone_check(message):  # Уточняем у пользователя чем он с нами поделиться
    if message.text == None:  # Если пользователь нажал кнопку "Поделиться контактом" то текс будет None
        if message.contact.user_id == message.chat.id:  # Проверяем свой ли контакт дал пользователь
            cli_num.append(message.contact.phone_number)
            pre_main(message)
        else:
            bot.send_message(message.chat.id, 'Введите правильный номер телефона!')
            statup(message)
    elif message.text == "Ввести почту для авторизации":  # Перекидывает на ввод почты
        mail_check(message)
    elif message.text == 'Ⓜ Главное меню':
        pre_main(message)
    else:
        statup(message)


def mail_check(message):  # Функция ввода почты
    key1 = telebot.types.ReplyKeyboardMarkup(True, False)
    key1.row("Проверить")
    bot.send_message(message.chat.id, 'Введите вашу почту ⤵')
    if message.text == 'Ввести почту для обратной связи':
        bot.register_next_step_handler(message, mail_check2)
    elif message.text == 'Ⓜ Главное меню':
        pre_main(message)


def mail_check2(message):  # Проверка потчы на валидность
    pattern = compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')  # Проверяем совпадает ли паттерк
    is_valid = pattern.match(message.text)
    if is_valid:
        cli_mail.append(message.text)  # Записываем полученную почту
        pre_main(message)
    elif message.text == 'Ⓜ Главное меню':
        pre_main(message)
    else:
        bot.send_message(message.chat.id, "Почта введена неверно.")
        statup(message)


def pre_main(message):  # Основная функция
    inc_type.clear()  # Очищаем словарь с типом заявки
    key = types.ReplyKeyboardMarkup(True, False)
    key.row('Наши услуги и стоимость', "Контакты и адрес")
    key.row('Записаться', "Мы на карте")
    key.row('Наши соц сети')
    key.one_time_keyboard = True
    try:  # Спрашиваем что за инцент
        bot.send_message(message.chat.id,
                         "Итак, {0.first_name}!, что у вас случилось?.".format(
                             message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=key)
        print('No problem detected. Message send')
    except OSError:  # Спрашиваем что за инцент если предидущий вызвал ошибку таймаута
        print("ConnectionError - Sending again after 5 seconds!!!")
        time.sleep(5)
        bot.send_message(message.chat.id,
                         "Итак, {0.first_name}, что хотите узнать?]?.".format(
                             message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=key)
        print('Problem solved')
    bot.register_next_step_handler(message, main)


def main(message):  # Определяем тип инцидента и уточняем его подтип
    if message.text == 'Наши услуги и стоимость':
        bot.send_message(message.chat.id, 'Диагностика двигателя и электронных систем - от 500₽ до 1000₽''\n'
                                          'Чип-Тюнинг Автомобилей: увеличение мощности, перевод на Евро-2, '
                                          'отключение: EGR, DPF, EVAP, SCV, Adblue и пр. - От 2000₽ до 30000₽''\n '
                                          'Замена ГРМ, ремней генератора, помпы (водяного насоса), маслосъёмных '
                                          'колпачков, прокладки клапанной крышки, сальника распредвала, '
                                          'сальника коленвала, прокладки ГБЦ (Головки блока цилиндров). От 1000₽''\n '
                                          'Ремонт ГБЦ от 6000₽''\n'
                                          'Регулировка клапанов на автомобилях ВАЗ, Renault, Datsun, Mitsubishi, '
                                          'Great Wall, Honda- от 1000₽ до 1500₽''\n '
                                          'Промывка форсунок/инжектора на ультразвуковом стенде или без снятия с '
                                          'автомобиля - от 1000₽ (снятые форсунки) до 3000₽''\n '
                                          'Ремонт и настройка карбюраторов, систем зажигания. - от 500₽''\n')
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Ⓜ Главное меню')
        bot.send_message(message.chat.id, 'Возврат в главное меню ⤵', reply_markup=keyboard)
    elif message.text == 'Записаться':
        bot.send_message(message.chat.id, 'Хотите записаться?')
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Да')
        bot.register_next_step_handler(message, user_reg)
    elif message.text == 'Контакты и адрес':
        bot.send_message(message.chat.id, '📱 +79610218408 Сергей''\n'
                                          '📱 +79056379476 Никита''\n'
                                          'г. Ярославль, Ленинградский проспект 25А, Бокс №1')
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Ⓜ Главное меню')
        keyboard.one_time_keyboard = True
        bot.send_message(message.chat.id, 'Возврат в главное меню ⤵', reply_markup=keyboard)
    elif message.text == 'Наши соц сети':
        key = types.InlineKeyboardMarkup(row_width=2)
        inst = types.InlineKeyboardButton(text='Instagram', url='https://instagram.com/garage1_yar')
        vk = types.InlineKeyboardButton(text='Vkontakte', url='https://vk.com/garage1_yar')
        avito = types.InlineKeyboardButton(text='Avito', url='https://www.avito.ru/user/2ff12a1824cec4ae791ce715ef78ec7a/profile?src=sharing')
        yandex = types.InlineKeyboardButton(text='Yandex', url='https://uslugi.yandex.ru/profile/Garazh1-254534')
        key.add(inst, vk, avito, yandex)
        bot.send_message(message.chat.id, "Нажмите на кнопку и перейдите по ссылке", reply_markup=key)

        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Ⓜ Главное меню')
        keyboard.one_time_keyboard = True
        bot.send_message(message.chat.id, 'Возврат в главное меню ⤵', reply_markup=keyboard)
    elif message.text == 'Мы на карте':
        bot.send_location(message.chat.id, 57.671202, 39.828057)
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Ⓜ Главное меню')
        keyboard.one_time_keyboard = True
        bot.send_message(message.chat.id, 'Возврат в главное меню ⤵', reply_markup=keyboard)

    else:
        bot.send_message(message.chat.id, '🚫 Данные введены неверно 🚫')
        pre_main(message)


user_dict = {}


class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname', 'phone', 'driverSeria',
                'driverNumber', 'driverDate', 'car',
                'carModel', 'carColor', 'carNumber', 'carDate']

        for key in keys:
            self.key = None


def user_reg(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Ярославль')
    keyboard.row('Рыбинск')
    keyboard.row('Тутаев')
    keyboard.row('Кострома')
    keyboard.row('Иваново')
    msg = bot.send_message(message.chat.id, 'Выберите город ⤵', reply_markup=keyboard)
    bot.register_next_step_handler(msg, process_city_step)


def process_city_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Как к вам можно обращаться?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_fullname_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_fullname_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text

        msg = bot.send_message(chat_id, 'Телефон для связи с вами')
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_phone_step(message):
    try:
        int(message.text)

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Марка вашего автомобиля')
        bot.register_next_step_handler(msg, process_driverSeria_step)

    except Exception as e:
        msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите номер телефона.')
        bot.register_next_step_handler(msg, process_phone_step)


def process_driverSeria_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.driverSeria = message.text

        msg = bot.send_message(chat_id, 'Модель вашего автомобиля')
        bot.register_next_step_handler(msg, process_driverNumber_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_driverNumber_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.driverNumber = message.text

        msg = bot.send_message(chat_id, 'Тип кпп, объем двигателя')
        bot.register_next_step_handler(msg, process_driverDate_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_driverDate_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.driverDate = message.text

        msg = bot.send_message(chat_id, 'Год выпуска')
        bot.register_next_step_handler(msg, process_car_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_car_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.car = message.text

        msg = bot.send_message(chat_id, 'Укажите какая услуга вас интересует')
        bot.register_next_step_handler(msg, process_carColor_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_carColor_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.carModel = message.text

        msg = bot.send_message(chat_id, 'Удобное для вас время для записи - в формате дата(число), время?')
        bot.register_next_step_handler(msg, process_carNumber_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_carNumber_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.carNumber = message.text

        msg = bot.send_message(chat_id, 'Когда вам можно позвонить?')
        bot.register_next_step_handler(msg, process_carDate_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_carDate_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.carDate = message.text

        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, 'Ваша заявка', message.from_user.first_name), parse_mode="Markdown")
        # отправить в группу
        bot.send_message('-535132227', getRegData(user, 'Заявка от бота', bot.get_me().username),
                         parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template(
        '$title *$name* \n Город: *$userCity* \n Обращение: *$fullname* \n Телефон: *$phone*\n Телефон при '
        'авторизации: *$phoneUM* \n Марка автомобиля: *$driverSeria* \n Модель автомобиля: *$driverNumber* \n Тип кпп '
        'и объем двигателя: *$driverDate* \n Год выпуска: *$car* \n Услуга: *$carModel* \n Приблизительное время '
        'записи: *$carNumber* \n Когда можно позвонить клиенту: *$carDate* \n Спасибо за заявку, мы свяжемся с вами в '
        'ближайшее время!')

    return t.substitute({
        'title': title,
        'name': name,
        'userCity': user.city,
        'fullname': user.fullname,
        'phone': user.phone,
        'phoneUM': cli_num,
        'driverSeria': user.driverSeria,
        'driverNumber': user.driverNumber,
        'driverDate': user.driverDate,
        'car': user.car,
        'carModel': user.carModel,
        'carNumber': user.carNumber,
        'carDate': user.carDate,
    })


while True:  # Запускаем бота
    try:
        bot.polling(none_stop=True)
    except OSError:
        bot.polling(none_stop=True)
