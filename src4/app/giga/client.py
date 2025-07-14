import os, httpx, logging
from typing import Any, Dict, List
from openai import OpenAI

class GigaChatClient:
    """
    Минимальная обёртка, пока используется только для запроса `/models`.
    Пригодится на втором уровне, чтобы получать ответы от LLM.
    """
    BASE_URL = "https://gigachat.devices.sberbank.ru/api/v1"

    def __init__(self):
        token = os.getenv("GIGA_AUTH")
        if not token:
            raise RuntimeError("GIGA_AUTH env var is required to talk to GigaChat")
        self.headers = {"Authorization": f"Bearer {token}"}

    async def list_models(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{self.BASE_URL}/models", headers=self.headers)
            resp.raise_for_status()
            return resp.json()
        
    def invoke(self, prompt):
        client = OpenAI(api_key= "{token}",
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

    