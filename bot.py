from libraries import * # here are all required libraries for all files

import plotter # methods for plotting
import stocks # methods for finding stocks and making a plot of their dynamics

bot = telebot.TeleBot(config.token) # initializing bot-object via string token in config


# It sends greeting message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    '''
        :param message: message from user
        :return: nothing
    '''
    bot.reply_to(message, "Привет! Я бот-помощник. Я умею рисовать графики в /plot для лабораторных и прочего,\
а также могу рассказать про стоимость акций в /stocks")


# It sends help-info message
@bot.message_handler(commands=['help'])
def send_welcome(message):
    '''
        :param message: message from user
        :return: nothing.
    '''
    bot.reply_to(message, "Если хочешь, чтобы я нарисовал график по данным из excel-файла, набери /plot. \
Если хочешь узнать текущую стоимость акций, набери /stocks.")

# It handles start of stocks_mode and goes to stocks_mode
@bot.message_handler(commands=['stocks'])
def stocks_handler(message):
    '''
        :param message: message from user
        :return: nothing.
    '''
    bot.send_message(message.chat.id, "Пришли мне тикер акции, по которой нужна информация. \
Если не знаешь, что такое тикер, попробуй /stock_help")
    msg = bot.send_message(message.chat.id, "Для того, чтобы выйти из режима /stocks, набери /escape")

    # registers next message after msg and goes to stocks mode
    bot.register_next_step_handler(msg, stocks_mode)


# special mode that starts over after each step if not escaped
def stocks_mode(message):
    '''
        :param message: message from user
        :return: nothing
        /stock_help -- description and help
        /escape -- stop the mode
        else -- a ticker entered
    '''
    if message.text == '/stock_help':
        help_stocks(message) # the func sends help-info

        # moving to the next step of the mode
        msg = bot.send_message(message.chat.id, "Можешь ввести тикер или /escape")
        bot.register_next_step_handler(msg, stocks_mode)
    elif message.text == '/escape':
        #getting away
        bot.send_message(message.chat.id, "Выхожу из режима /stocks")
    else:
        bot.send_message(message.chat.id, "Ищу {}...".format(message.text))
        try:
            ticker = message.text
            bot.send_message(message.chat.id, stocks.company_name(ticker)) # sends conpany_name found in stocks.py
            df, start_date, end_date = stocks.main(ticker) # gives back found data and period of time of data

            # stocks.plot returns the last info about the stock and here we send it, starting plotting the data
            bot.send_message(message.chat.id, stocks.plot(message.chat.id, df, ticker, start_date, end_date))
            # start plotting figure with moving_mean
            stocks.moving_mean(message.chat.id, df, ticker)

            # stocks.plot user_id_ticker.png and user_id_ticker_mm.png -- moving mean in files_to_send for us -- we send it
            with open("files_to_send\\{}_{}.png".format(message.chat.id, ticker), 'rb') as file:
                bot.send_photo(message.chat.id, file)
            os.remove("files_to_send\\{}_{}.png".format(message.chat.id, ticker)) # deleting sent data

            with open('files_to_send\\{}_{}_mm.png'.format(message.chat.id, ticker), 'rb') as file:
                bot.send_photo(message.chat.id, file)
            os.remove('files_to_send\\{}_{}_mm.png'.format(message.chat.id, ticker)) # deleting sent plot

            # moving to the next step of the mode
            msg = bot.send_message(message.chat.id, "Введи новый тикер или /escape")
            bot.register_next_step_handler(msg, stocks_mode)
        except Exception as e:
            # moving to the next step of the mode if sth went wrong
            msg = bot.reply_to(message, "Что-то пошло не так(( Попробуй другой тикер.")
            bot.register_next_step_handler(msg, stocks_mode)


# sends help-info about stocks_mode
@bot.message_handler(commands=['stock_help'])
def help_stocks(message):
    '''
    :param message: user message
    :return: nothing
    '''
    bot.send_message(message.chat.id, "Напиши мне в режиме /stocks тикер акции, и я скажу тебе её текущую стоимость и покажу динамику акции за последний год.")
    bot.send_message(message.chat.id, "Например, пришли в /stocks \"NFLX\", чтобы спросить про Netflix, Inc.")
    bot.send_message(message.chat.id, "Для акций московской биржи добавляй .ME. Например, GAZP.ME")
    bot.send_message(message.chat.id, "Лучше всего смотри тикеры здесь: https://finance.yahoo.com/")
    bot.send_message(message.chat.id, "Для того, чтобы выйти из режима /stocks, набери /escape")


# makes a plot from received     excel file
@bot.message_handler(commands=['plot'])
def send_plot(message):
    '''
    :param message:
    :return:
    '''
    bot.reply_to(message, 'Лабы... Понимаю...')

    # sending example excel file
    f = open('example.xlsx', "rb")
    bot.send_document(message.chat.id, f)
    f.close()

    bot.send_message(message.chat.id, 'Отправь мне файл .xlsx или .xls как в example.xlsx и я пришлю тебе график.')

    @bot.message_handler(content_types=['document'])
    def handle_file(message):
        '''
        starts when a file received (can  be not excel -- then just escape)
        :param message:
        :return:
        '''
        try:
            # downloading received file to RAM
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            bot.reply_to(message, "Секундочку...")

            # future src of the file received
            src = "received\\" + str(message.chat.id) + "." + file_info.file_path.split(".")[-1]

            # saving file locally
            with open(src, 'wb+') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, 'Рисую...')

            # plotter.py starts with create_plot(src, user_id) and makes a plot
            response = plotter.create_plot(src, message.chat.id)
            if response: # if everything went OK there will be user_id.png and .pdf in files_to_send
                with open("files_to_send\\{}.png".format(message.chat.id), 'rb') as file:
                    bot.send_photo(message.chat.id, file)

                os.remove("files_to_send\\{}.png".format(message.chat.id)) # removing sent file

                with open("files_to_send\\{}.pdf".format(message.chat.id), 'rb') as file:
                    bot.send_document(message.chat.id, file)

                os.remove("files_to_send\\{}.pdf".format(message.chat.id)) # removing sent file
                os.remove(src) # removing received excel-file

        except Exception as e:
            # if exception thrown just escaping
            bot.reply_to(message, 'Что-то пошло не так... Попробуй поправить что-то в твоем файле.')


# if sth unknown sent we echo that we dont know what've received
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, 'Прости, пока не знаю, как на это ответить. Посмотри, что я могу в /help')


# the method starts polling of the object bot
bot.polling()
