import os, logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .schemas import (
    InputPayload, InputResponse,
    TaskPayload, TaskResponse,
    TaskResultPayload,
    NotificationPayload
)
from .state import app_state
from .agent import RandomAgent
from .giga.client import GigaChatClient

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Final API", version="1.0.0")

agent = RandomAgent()

# ------------------------------------------------------------------
# startup: печатаем список моделей GigaChat (если ключ имеется)
# ------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    if os.getenv("GIGA_AUTH"):
        try:
            client = GigaChatClient()
            models = await client.list_models()
            logging.info("GigaChat models: %s", models)
        except Exception as exc:
            logging.warning("Could not fetch GigaChat models: %s", exc)
    else:
        logging.warning("GIGA_AUTH not set – skip models request.")


# ------------------------------------------------------------------
# /inputs
# ------------------------------------------------------------------
@app.post("/inputs", response_model=InputResponse)
async def create_input(payload: InputPayload):
    # базовая проверка «матрицы» (у Pydantic уже проверился тип List[List])
    if not payload.view or not all(isinstance(r, list) for r in payload.view):
        return JSONResponse(status_code=400, content={"action": "None"})

    action = agent.next_action(payload.view)
    app_state.tick += 1
    return InputResponse(action=action)


# ------------------------------------------------------------------
# /tasks
# ------------------------------------------------------------------
@app.post("/tasks", response_model=TaskResponse)
async def post_task(payload: TaskPayload):
    app_state.last_task = payload
    app_state.last_task_answered = False

    answer = agent.solve_task(payload)
    return TaskResponse(answer=answer)


# ------------------------------------------------------------------
# /tasks/last
# ------------------------------------------------------------------
@app.patch("/tasks/last")
async def patch_last(payload: TaskResultPayload):
    if app_state.last_task is None or app_state.last_task_answered:
        raise HTTPException(status_code=404, detail="No pending task.")
    app_state.last_task_answered = True
    # Пока ничего внутри не делаем – просто подтверждаем
    return JSONResponse(status_code=200, content={"status": "accepted"})


# ------------------------------------------------------------------
# /notifications
# ------------------------------------------------------------------
@app.post("/notifications")
async def post_notification(payload: NotificationPayload):
    logging.info("Notification: %s", payload.model_dump())
    return JSONResponse(status_code=200, content={"status": "accepted"})