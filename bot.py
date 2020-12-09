from libraries import *
import plotter
import stocks

bot = telebot.TeleBot(config.token)

'''
@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    start_r = types.InlineQueryResultArticle(
        id='0', title="/start",
        input_message_content=types.InputTextMessageContent(
            message_text="{!s} * {!s} = {!s}".format(1, 2, 3))
    )
    bot.answer_inline_query(query.id, [start_r])
'''


@bot.message_handler(commands=['stock_help'])
def help_stocks(message):
    bot.send_message(message.chat.id, "Например, пришли \"NFLX\", чтобы спросить про Netflix, Inc.")
    bot.send_message(message.chat.id, "Для акций московской биржи добавляй .ME. Например, GAZP.ME")
    bot.send_message(message.chat.id, "Лучше всего смотри тикеры здесь: https://finance.yahoo.com/")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi! I'm a help-bot which will be able to plot some stuff. \
    For now I can only ask you to send me a file and receive it. Try now using /plot!")


@bot.message_handler(commands=['stocks'])
def stocks_handler(message):
    msg = bot.send_message(message.chat.id, "Пришли мне тикер акции, по которой нужна информация.")
    bot.register_next_step_handler(msg, ticker_handler)


def ticker_handler(message):

        bot.send_message(message.chat.id, "Ищу {}...".format(message.text))
        try:
            ticker = message.text
            bot.send_message(message.chat.id, stocks.company_name(ticker))
            df, start_date, end_date = stocks.main(ticker)
            bot.send_message(message.chat.id, stocks.plot(message.chat.id, df, ticker, start_date, end_date))
            with open("files_to_send\\{}_{}.png".format(message.chat.id, ticker), 'rb') as file:
                bot.send_photo(message.chat.id, file)
            os.remove("files_to_send\\{}_{}.png".format(message.chat.id, ticker))

        except Exception as e:
            bot.reply_to(message, e)



@bot.message_handler(commands=['plot'])
def send_file(message):
    bot.reply_to(message, 'Лабы... Понимаю...')

    f = open('example.xlsx', "rb")
    bot.send_document(message.chat.id, f)
    f.close()

    bot.send_message(message.chat.id, 'Отправь мне файл .xlsx или .xls как в example.xlsx и я пришлю тебе график.')

    @bot.message_handler(content_types=['document'])
    def handle_file(message):
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            bot.reply_to(message, "Секундочку...")

            #file can be saved locally
            src = "received\\" + str(message.chat.id) + "." + file_info.file_path.split(".")[-1]

            with open(src, 'wb+') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, 'Рисую...')

            response = plotter.create_plot(src, message.chat.id)

            #file to send: "{}.pdf".format(message.chat.id) "{}.png".format(message.chat.id)
            if response:
                with open("files_to_send\\{}.png".format(message.chat.id), 'rb') as file:
                    bot.send_photo(message.chat.id, file)

                os.remove("files_to_send\\{}.png".format(message.chat.id))

                with open("files_to_send\\{}.pdf".format(message.chat.id), 'rb') as file:
                    bot.send_document(message.chat.id, file)

                os.remove("files_to_send\\{}.pdf".format(message.chat.id))
                os.remove(src)

        except Exception as e:
            bot.reply_to(message, e)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, 'Прости, пока не знаю, как на это ответить. Посмотри, что я могу в /help')


bot.polling()
