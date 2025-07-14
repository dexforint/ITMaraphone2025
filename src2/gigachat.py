import os
import requests

GIGACHAT_API_URL = "https://gigachat.devices.sberbank.ru/api/v1/models"
# Рекомендуется хранить ключ в переменной окружения, а не в коде
# Создай в папке src файл .env и запиши туда GIGACHAT_API_KEY="ТВОЙ_КЛЮЧ"
API_KEY = os.getenv("GIGACHAT_API_KEY")


def get_available_models():
    """
    Получает список доступных моделей GigaChat и выводит их в консоль.
    """
    if not API_KEY:
        print("GigaChat API key not found. Skipping model list request.")
        print("Please set GIGACHAT_API_KEY environment variable.")
        return

    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(
            GIGACHAT_API_URL, headers=headers, verify=False
        )  # verify=False для отключения проверки SSL, если будут проблемы
        response.raise_for_status()  # Вызовет исключение для кодов 4xx/5xx
        models = response.json()
        print("--- Available GigaChat Models ---")
        for model in models.get("data", []):
            print(f"- {model.get('id')}")
        print("---------------------------------")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GigaChat models: {e}")
