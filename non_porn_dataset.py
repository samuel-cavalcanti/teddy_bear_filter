from google_images_download.google_images_download import googleimagesdownload
from concurrent.futures import ThreadPoolExecutor


def download_images(arguments: dict):
    response = googleimagesdownload()
    response.download(arguments)


def download_non_porn_database():
    keywords = ["wrestling", "beach clothes", "swimming", "breastfeeding", "games", "cat", "gym clothes"]

    arguments_list = [{"keywords": keyword, "limit": int(1e5), "print_urls": True, "chromedriver": "/bin/chromedriver"}
                      for keyword in keywords]

    with ThreadPoolExecutor(max_workers=8) as executor:
        for _ in executor.map(download_images, arguments_list):
            pass


if __name__ == '__main__':
    download_non_porn_database()
