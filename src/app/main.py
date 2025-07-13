import os
import logging
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from .models import (
    InputRespOk,
    InputBody,
    InputRespBad,
    TaskResp,
    TaskBody,
    PatchBody,
    NotificationBody,
)


# ---------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Подключение к GigaChat при старте и отключение при выходе
    """
    token = os.getenv("GIGACHAT_API_KEY")
    if not token:
        logging.warning("GIGACHAT_API_KEY not set")
    else:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://gigachat.devices.sberbank.ru/api/v1/models",
                headers={"Authorization": f"Bearer {token}"},
            )
            logging.info("GigaChat models: %s", r.text)
    yield
    # Можно добавить код для graceful shutdown


app = FastAPI(title="Final API", lifespan=lifespan)


# ---------------------------------------------------------------
from .state import STATE


@app.post(
    "/inputs", responses={200: {"model": InputRespOk}, 400: {"model": InputRespBad}}
)
def create_input(body: InputBody):
    return InputRespOk()


# при ошибке валидации InputBody сама FastAPI вернёт 422 (можно
# перехватить и переделать в 400, если это критично для тестов)


@app.post("/tasks", response_model=TaskResp)
def create_task(body: TaskBody):
    STATE.last_task = body
    STATE.result_received = False
    return TaskResp(answer="Да")


from typing import Any


@app.patch("/tasks/last")
def patch_last(body: PatchBody) -> dict[str, Any]:
    if STATE.last_task is None or STATE.result_received:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    STATE.result_received = True
    return {}  # 200 без тела


@app.post("/notifications")
def notify(body: NotificationBody) -> dict[str, Any]:
    return {}
