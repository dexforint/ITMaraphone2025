from openai import OpenAI
import time


def get_cody_client():
    import httpx

    client = httpx.Client()

    response = client.post("https://cody.su/api/v1/get_api_key")
    response.raise_for_status()

    api_key = response.json()["api_key"]

    client = OpenAI(base_url="https://cody.su/api/v1", api_key=api_key)

    return client


def get_g4f_client():
    import subprocess
    import atexit

    # 'deepseek-v3',
    # 'deepseek-v3-0324',
    # 'deepseek-v3-0324-turbo',
    # 'gemini-2.0-flash',
    # 'gemini-2.0-flash-thinking',
    # 'gemini-2.0-flash-thinking-with-apps',
    # 'gemini-2.5-flash',
    # 'gemini-2.5-pro',
    # 'o1',
    # 'o1-mini',
    # 'o3-mini',
    # 'o3-mini-high',
    # 'o4-mini',
    # 'o4-mini-high',
    # 'gpt-4',
    # 'gpt-4.1',
    # 'gpt-4.1-mini',
    # 'gpt-4.1-nano',
    # 'gpt-4.5',
    # 'gpt-4o',
    # 'gpt-4o-mini',

    # Запускаем процесс
    process = subprocess.Popen(["python", "-m", "g4f.api.run"])

    # Функция для завершения процесса
    def cleanup():
        process.terminate()

    # Регистрируем функцию завершения
    atexit.register(cleanup)
    time.sleep(5)

    try:
        return OpenAI(
            api_key="AIzaSyCs_lOOs9zU7AwWEBpKlJoX5I39tDKOhxY",
            base_url="http://localhost:1337/v1",
        )
    finally:
        cleanup()


def get_gemini_client():
    # "gemini-2.5-flash"
    # "gemini-2.0-flash"
    return OpenAI(
        api_key="AIzaSyCs_lOOs9zU7AwWEBpKlJoX5I39tDKOhxY",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )


def get_rotated_invoke_function():
    pass
