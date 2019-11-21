import os
import numpy as np
from sklearn import model_selection
import cv2


def load_non_porn_images(root_path: str) -> (list, list):
    x = list()
    y = list()

    for file in os.listdir(root_path):
        try:
            image: np.ndarray = cv2.imread(os.path.join(root_path, file))

            if image is None:
                os.remove(os.path.join(root_path, file))
            else:

                x.append(cv2.resize(image, (200, 200), interpolation=cv2.INTER_AREA))
                y.append(0)

        except:
            print(file)
            exit(1)

    return x, y


def load_porn_images(root_path: str, size: int) -> (list, list):
    x = list()
    y = list()
    '''
          o número de fotos pornograficas são maiores do que as não pornográficas
          então limitei o valor para ficar iguais 
    '''
    number_of_porn_pictures = 0

    for file in os.listdir(root_path):

        if number_of_porn_pictures < size:
            image: np.ndarray = cv2.imread(os.path.join(root_path, file))

            if image is None:
                os.remove(os.path.join(root_path, file))
            else:

                x.append(cv2.resize(image, (200, 200), interpolation=cv2.INTER_AREA))
                y.append(1)
                number_of_porn_pictures += 1

    return x, y


def split_and_save_database(x: np.ndarray, y: np.ndarray, file_name: str):
    x_train, y_train, x_test, y_test = model_selection.train_test_split(x, y, test_size=0.4, random_state=42)

    np.savez(file_name, x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)


def build_database(file_name: str):
    non_porn_path = "dataset/nonPorn"
    porn_path = "dataset/porn"

    size = len(os.listdir(non_porn_path))

    print("Loading non porn images")
    x_non_porn, y_non_porn = load_non_porn_images(non_porn_path)

    print("Loading porn images")
    x_porn, y_porn = load_porn_images(porn_path, size)

    print("splitting and saving database")
    split_and_save_database(np.array(x_non_porn + x_porn), np.array(y_non_porn + y_porn), file_name)


'''
algoritmo feito para limpar datasets, após mineração de dados  
'''


def clearing_data(model: str, dataset_: str):
    pass


if __name__ == '__main__':
    build_database("Pornography_Database")
