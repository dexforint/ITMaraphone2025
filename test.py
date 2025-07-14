GIGACHAT_AUTHORIZATION_KEY="Mjk4MjY2ZGEtMTFlZS00MDEzLTk2NDYtZWExNjRhM2EwOWE3Ojc1YzgxOGIyLTkxNWQtNDFmMy1hMDkwLTNlOTkwOWFkNjY2Yg=="

from openai import OpenAI

client = OpenAI(api_key=GIGACHAT_AUTHORIZATION_KEY,
                base_url= "https://gigachat.devices.sberbank.ru/api/v1"
                )
completion = client.chat.completions.create(
    model="GigaChat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Hello World!"
        }
    ]
)
print(completion.choices[0].message)