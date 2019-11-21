from telegramBot.teddy_bear_bot import TeddyBearBot

from telegramBot.server import TeddyFilterServer

if __name__ == '__main__':
    teddy_filter = TeddyFilterServer("teddy_model")

    bot = TeddyBearBot("TOKKEN")

    teddy_filter.start_to_accept_connection()

    bot.start_bot()

    teddy_filter.start_to_receive_and_send_messages()
