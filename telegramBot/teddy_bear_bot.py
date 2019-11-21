from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters
from telegram.update import Update
from telegram.bot import Bot
import os
import shutil
import json
import socket


class TeddyBearBot:
    __teddy_bear_image = "https://github.com/samuel-cavalcanti/samuel-cavalcanti.github.io/raw/master/teddy_bear.jpg"
    __current_id_image = 0

    def __init__(self, token: str):
        self.__updater = Updater(token=token, workers=0)

        self.__dispatcher = self.__updater.dispatcher

        self.__bot = self.__updater.bot

        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__set_handlers()

    def __set_handlers(self):
        self.__dispatcher.add_handler(CommandHandler("start", self.__start))
        self.__dispatcher.add_handler(MessageHandler(Filters.photo, self.__photo_filter))

    def start_bot(self):
        self.__tcp.connect(("localhost", 5354))
        self.__updater.start_polling()
        print("Bot is started")

    def __start(self, bot: Bot, update: Update):
        print(update)

        bot.send_message(update.message.chat.id, text="please send-me an image")
        bot.delete_message(update.message.chat.id, update.message.message_id)

    def __photo_filter(self, bot: Bot, update: Update):
        print("get photo")
        new_file = bot.getFile(update.message.photo[-1].file_id)

        new_path = self.__generate_path()

        new_file.download(new_path)

        self.send_message(new_path, update.message.chat.id, update.message.message_id)

        self.receive_message()

    def __generate_path(self):
        temp_images_dir = os.path.join(os.path.split(__file__)[0], "tempImages")

        if self.__current_id_image > 100:
            shutil.rmtree(temp_images_dir, ignore_errors=True)
            self.__current_id_image = 0

        if not os.path.isdir(temp_images_dir):
            os.mkdir(temp_images_dir)

        path = os.path.join(temp_images_dir, "temp{}".format(self.__current_id_image))

        self.__current_id_image += 1

        return path

    def send_message(self, image_path: str, chat_id: str, message_id: str):

        json_file = {
            "image_path": image_path,
            "chat_id": chat_id,
            "message_id": message_id
        }
        message = json.dumps(json_file)

        self.__tcp.sendall(message.encode())

    def receive_message(self):
        json_data = json.loads(self.__tcp.recv(2048).decode())

        if json_data["predict"]:
            self.__bot.delete_message(json_data["chat_id"], json_data["message_id"])
            self.__bot.send_photo(json_data["chat_id"], self.__teddy_bear_image, "not Safe!")
