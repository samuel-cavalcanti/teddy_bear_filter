import csv
import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor
import kaggle


def check_status_code(url) -> requests.request:
    result = requests.get(url, stream=True)

    while result.status_code != 200:

        if result.status_code >= 400:
            print("code: {}, URL: {}".format(result.status_code, url))
            return None

        time.sleep(1)
        result = requests.get(url)

    return result


def fetch_url(urls_and_titles):
    url, title, dataset_dir = urls_and_titles

    root_path = os.path.join(dataset_dir, "porn")

    try:

        result = check_status_code(url)

        create_dir(root_path)

        title = ''.join(e for e in title if e.isalnum())

        file_path = os.path.join(root_path, "{}.jpg".format(title))

        open(file_path, "wb").write(result.content)

    except:
        print("Erro no request !!")


def create_dir(dir_name: str):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)


def dowload_kaggle_dataset(database_dir: str):
    kaggle.api.authenticate()

    kaggle.api.dataset_download_files("ljlr34449/porn-data", path=database_dir, unzip=True)


def download_dataset_from_csv(dataset_dir: str):
    csv_file_name = os.listdir(dataset_dir)[0]

    if len(os.listdir(dataset_dir)) != 1:
        print("Esse diretório só deveira ter 1 arquivo, o arquivo csv !!")
        return

    csv_file = csv.reader(open(os.path.join(dataset_dir, csv_file_name)), delimiter=",")

    url_index = 1

    title_index = 5

    number_of_workers = 8

    urls_and_titles = [(row[url_index], row[title_index], dataset_dir) for row in csv_file]

    with ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        for _ in executor.map(fetch_url, urls_and_titles):
            pass


def main():
    dataset_dir = "database"

    create_dir(dataset_dir)

    dowload_kaggle_dataset(dataset_dir)

    download_dataset_from_csv(dataset_dir)


if __name__ == '__main__':
    main()
