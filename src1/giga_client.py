import os
import httpx
import logging

GIGACHAT_URL = "https://gigachat.devices.sberbank.ru/api/v1/models"
TOKEN_ENV = "GIGACHAT_TOKEN"

_log = logging.getLogger("giga")


async def list_models() -> None:
    token = os.getenv(TOKEN_ENV)
    if not token:
        _log.warning("GigaChat token not found in env %s, skip listing", TOKEN_ENV)
        return
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(GIGACHAT_URL, headers=headers)
            r.raise_for_status()
            models = r.json()
            _log.info("GigaChat models: %s", models)
        except Exception as e:
            _log.error("Cannot fetch models from GigaChat: %s", e)
