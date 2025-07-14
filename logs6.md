Ниже ‑ полный «скелет» решения, который:

• реализует stateful-веб-сервис на FastAPI;  
• поднимается в Docker и сразу печатает доступные модели GigaChat;  
• готов «пережить» заглушечные проверки первого уровня;  
• содержит задел для второй части (BFS-навигация + вопрос-ответ через GigaChat).

Структура каталога src

```
src/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── models.py
│   ├── state.py
│   ├── solver.py
│   └── gigachat.py
├── main.py
├── requirements.txt
└── Dockerfile
```

---

app/models.py

```python
from enum import Enum

from pydantic import BaseModel, Field, validator
from typing import List, Literal, Optional


class InputsIn(BaseModel):
    view: List[List[int]]

    @validator("view")
    def validate_matrix(cls, v):
        if not v:
            raise ValueError("view is empty")

        row_len = len(v[0])
        for row in v:
            if not isinstance(row, list) or len(row) != row_len:
                raise ValueError("matrix must be rectangular")
            if not all(isinstance(x, int) for x in row):
                raise ValueError("matrix contains non-integer")

        return v


class InputsOut(BaseModel):
    action: str


class TaskIn(BaseModel):
    type: str
    task: str


class TaskOut(BaseModel):
    answer: str


class TaskResult(str, Enum):
    Ok = "Ok"
    TryAgain = "TryAgain"
    Fail = "Fail"


class TaskLastIn(BaseModel):
    result: TaskResult


class NotificationIn(BaseModel):
    type: str
    desc: str
```

---

app/state.py

```python
"""
Минимальное хранилище состояния.
Для продакшена стоило бы вынести в redis/sqlite,
но для хакатона хватит in-memory singleton.
"""
from __future__ import annotations
from typing import Optional


class GlobalState:
    def __init__(self):
        # навигация
        self.last_view = None
        # задачи
        self.last_task: Optional[str] = None
        self.last_task_result_pending: bool = False

    # ---------- helpers ----------
    def remember_task(self, task: str):
        self.last_task = task
        self.last_task_result_pending = True

    def resolve_task(self):
        self.last_task = None
        self.last_task_result_pending = False


STATE = GlobalState()
```

---

app/solver.py

```python
"""
Очень простой универсальный навигатор:
BFS до ближайшей непустой клетки (значение != 0)
и возвращаем первый шаг.
При желании сюда можно «догрузить» любые эвристики.
Матрица «view» трактуется как локальное зрение,
агент находится в центре (row//2, col//2).
"""

from collections import deque
from typing import List, Tuple, Optional


DIRS = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]


def bfs_next_action(view: List[List[int]]) -> str:
    n, m = len(view), len(view[0])
    start = (n // 2, m // 2)

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < n and 0 <= c < m

    q = deque()
    q.append((start[0], start[1], []))
    seen = {start}

    while q:
        r, c, path = q.popleft()

        # цель — любая не-пустая клетка, кроме стартовой
        if (r, c) != start and view[r][c] != 0:
            return path[0] if path else "None"

        for dr, dc, action in DIRS:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc) and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc, path + [action]))

    return "None"
```

---

app/gigachat.py

```python
"""
Тонкая обёртка над openai==1.x для GigaChat.
"""

import os
import logging
import requests
from typing import List, Dict, Any, Optional

GIGA_BASE_URL = "https://gigachat.devices.sberbank.ru/api/v1"
log = logging.getLogger(__name__)


def print_available_models() -> None:
    token = os.getenv("GIGA_AUTH")
    if not token:
        log.warning("GIGA_AUTH не задан – пропускаем вывод моделей")
        return

    try:
        resp = requests.get(
            f"{GIGA_BASE_URL}/models", headers={"Authorization": f"Bearer {token}"}, timeout=10
        )
        resp.raise_for_status()
        models = [m["id"] for m in resp.json().get("data", [])]
        log.info("GigaChat models: %s", models)
    except Exception as e:
        log.error("Не удалось получить список моделей GigaChat: %s", e)


def ask_gigachat(prompt: str, system_msg: str = "Ты — искусственный интеллект-помощник.") -> str:
    token = os.getenv("GIGA_AUTH")
    if not token:
        raise RuntimeError("Нет токена GIGA_AUTH")

    # Ленивая загрузка openai, чтобы не тянуть лишние импорты при старте без токена
    from openai import OpenAI

    client = OpenAI(api_key=token, base_url=GIGA_BASE_URL)
    completion = client.chat.completions.create(
        model="GigaChat",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt},
        ],
        timeout=15,
    )
    return completion.choices[0].message.content.strip()
```

---

app/api.py

```python
from fastapi import APIRouter, HTTPException
from app import models, state, solver, gigachat

router = APIRouter(tags=["Task"])


@router.post("/inputs", response_model=models.InputsOut)
def handle_inputs(payload: models.InputsIn):
    view = payload.view
    action = solver.bfs_next_action(view)
    state.STATE.last_view = view  # на всякий случай сохраняем
    return models.InputsOut(action=action or "None")


@router.post("/tasks", response_model=models.TaskOut)
def handle_tasks(payload: models.TaskIn):
    state.STATE.remember_task(payload.task)

    # Мини-логика заглушки
    if payload.type.lower() == "question" and "ты готов" in payload.task.lower():
        return models.TaskOut(answer="Да")

    # Всё остальное — спрашиваем у GigaChat
    try:
        answer = gigachat.ask_gigachat(payload.task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GigaChat error: {e}")

    return models.TaskOut(answer=answer)


@router.patch("/tasks/last", status_code=200)
def patch_last(payload: models.TaskLastIn):
    if not state.STATE.last_task_result_pending:
        raise HTTPException(status_code=404, detail="No pending task result")

    # можно логировать/учитывать payload.result
    state.STATE.resolve_task()
    return {"status": "accepted"}


@router.post("/notifications", status_code=200)
def handle_notifications(payload: models.NotificationIn):
    # здесь можно накопить историю, логировать и т.д.
    return {"status": "ok"}
```

---

app/**init**.py

```python
from fastapi import FastAPI
from app import api, gigachat

app = FastAPI(
    title="Final API",
    description="API для решения финальных задач",
    version="1.0.0",
)

app.include_router(api.router)


@app.on_event("startup")
def startup_event():
    gigachat.print_available_models()
```

---

main.py

```python
import uvicorn
from app import app

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        reload=False,
    )
```

---

requirements.txt

```
fastapi~=0.111
uvicorn[standard]~=0.30
pydantic~=2.7
openai~=1.30   # для GigaChat
requests~=2.32
```

---

Dockerfile

```dockerfile
# ---------- build stage ----------
FROM python:3.12-slim AS builder

WORKDIR /srv
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# ---------- runtime stage ----------
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /srv
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && \
    rm -rf /wheels

COPY app ./app
COPY main.py ./

EXPOSE ${PORT}

CMD ["python", "main.py"]
```

---

Как это собрать и запустить

```bash
# в корне репо
cd src
docker build -t final_hack .
docker run -it --rm -p 8080:8080 -e GIGA_AUTH="ваш_токен" final_hack
```

---

Короткое пояснение по логике

1. /inputs  
   • валидируем, что «view» — прямоугольная матрица целых;  
   • алгоритм solver.bfs_next_action ищет ближайшую «значимую» клетку ≠0 и
   возвращает первый шаг (Up/Down/Left/Right).  
   • если ничего не нашли — “None”.

2. /tasks  
   • простейшая заглушка: на вопрос «Ты готов?» отвечает «Да»;  
   • иначе — прокидываем текст в GigaChat и возвращаем ответ.  
   • помним, что результат по ней ещё не присылали.

3. /tasks/last  
   • принимаем ровно один раз; повторный PATCH → 404.

4. /notifications  
   • просто 200 OK.

5. При старте контейнера (FastAPI event startup) печатаем список моделей GigaChat,
если GIGA_AUTH задан.

6. Образ «тонкий» (python-slim + wheels) и ~300–350 MB < 4 GB.

---

Как нарастить до полноценного решения 2-го уровня

• В solver.py можно хранить «глобальную» карту мира (state.STATE),  
обновлять её после каждого view, а BFS запускать по всей накопленной области.

• Для загадок Сфинкса можно завести отдельный prompt-template и кэшировать ответы.

• Учитываем лимит 20 s: requests к GigaChat обрезаны таймаутом 15 s; BFS и прочее
работают за милли-секунды.

Успехов в финале!
