import socket
import keras
import numpy as np
import cv2
from queue import Queue
import json
import threading


class TeddyFilterServer:
    __port = 5354

    def __init__(self, model_path: str):
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        orig = ("", self.__port)
        self.__tcp.bind(orig)
        self.__tcp.listen(1)
        self.__model: keras.models.Model = keras.models.load_model(model_path)
        self.__queue = Queue(100)
        self.__accept_thread: threading.Thread
        self.__receive_messages_thread: threading.Thread
        self.__telegram_bot_connection = None

    def __predict(self, path: str) -> bool:
        image = cv2.imread(path)

        resized = cv2.resize(image, (200, 200))

        input_data = np.array([resized]).astype("float32") / 255

        predict = self.__model.predict(input_data)[0]

        return bool(np.argmax(predict))

    def __accept_connection(self):
        print("start to accept connections\n")

        self.__telegram_bot_connection, address = self.__tcp.accept()

        print("accept telegram")

    def start_to_receive_and_send_messages(self):
        client_socket: socket.socket

        print("start to receive messages")

        while True:
            json_data = json.loads(self.__telegram_bot_connection.recv(2048).decode())

            predict = self.__predict(json_data["image_path"])

            del json_data["image_path"]

            json_data["predict"] = predict

            if predict:
                print("it's a Porn picture")
            else:
                print("it's not a Porn picture")

            message = json.dumps(json_data)

            self.__telegram_bot_connection.sendall(message.encode())

    def start_to_accept_connection(self):
        self.__accept_thread = threading.Thread(target=self.__accept_connection, name="Accept Thread")

        self.__accept_thread.start()

    def __del__(self):
        self.__accept_thread.join()

        self.__tcp.close()
