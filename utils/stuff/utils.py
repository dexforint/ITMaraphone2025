from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests


def download_file(url, name=None):
    splits = url.split("/")
    filename = splits[-1]
    ext = filename.split(".")[-1]

    if not (name is None):
        filename = f"{name}.{ext}"

    save_path = os.path.join(os.getcwd(), filename)

    response = requests.get(url, stream=True)
    with open(save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    return save_path


def download_first_video(driver):
    video_element = driver.find_element(By.TAG_NAME, "video")

    # Получение значения атрибута src
    video_url = video_element.get_attribute("src")

    if video_url:
        save_path = download_file(video_url)
        return save_path
    else:
        print("Атрибут src не найден у тега video")


def download_all_videos(driver):
    video_elements = driver.find_elements(By.TAG_NAME, "video")

    videos = []

    for idx, video_element in enumerate(video_elements):
        # Получение значения атрибута src
        video_url = video_element.get_attribute("src")

        if video_url:
            save_path = download_file(video_url, name=str(idx))
            videos.append(save_path)
        else:
            videos.append(None)

    return videos
