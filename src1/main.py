# src/main.py
import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    InputsRequest,
    InputsOk,
    InputsBad,
    TaskRequest,
    TaskResponse,
    TaskResultRequest,
    NotificationRequest,
)
from giga_client import list_models

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("app")

app = FastAPI(
    title="Final API stub",
    version="1.0.0",
    description="Stateful stub for the hackathon",
)

# Разрешаем всё — удобнее дебажить
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


# ---------- GLOBAL STATE ----------
class State:
    last_task: TaskRequest | None = None
    last_task_answer: str | None = None
    accepted_result: bool = False


state = State()


# ---------- STARTUP: опрашиваем GigaChat ----------
@app.on_event("startup")
async def _startup() -> None:
    await list_models()


# ---------- /inputs ----------
@app.post("/inputs", response_model=InputsOk, responses={400: {"model": InputsBad}})
async def create_input(req: InputsRequest):
    # Здесь реальная логика — пока просто эхо
    log.info("Matrix %dx%d received", len(req.view), len(req.view[0]))
    return InputsOk()


# ---------- /tasks ----------
@app.post("/tasks", response_model=TaskResponse, status_code=200)
async def post_task(req: TaskRequest):
    log.info("Task received: %s - %s", req.type, req.task)
    # Сохраняем как «последнюю»
    state.last_task = req
    state.accepted_result = False

    # Заглушка: на фразу "Ты готов?" отвечаем "Да"
    if req.task.strip().lower() in ("ты готов?", "ты готов?"):
        answer = "Да"
    else:
        answer = "Unknown"

    state.last_task_answer = answer
    return TaskResponse(answer=answer)


# ---------- /tasks/last ----------
@app.patch("/tasks/last", status_code=200)
async def patch_task_result(req: TaskResultRequest):
    if state.last_task is None or state.accepted_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    log.info("Result %s accepted for task [%s]", req.result, state.last_task.task)
    state.accepted_result = True
    return JSONResponse(status_code=200, content={"status": "accepted"})


# ---------- /notifications ----------
@app.post("/notifications", status_code=200)
async def post_notification(req: NotificationRequest):
    log.info("Notification: %s | %s", req.type, req.desc)
    return JSONResponse(status_code=200, content={"status": "noted"})


# ---------- health-check ----------
@app.get("/health", include_in_schema=False)
async def _health():
    return {"ok": True}
