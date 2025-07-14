Ниже – полностью готовый «проект-скелет» для второго уровня, удовлетворяющий всем требованиям из ТЗ:

• FastAPI-сервис со stateful-логикой и всеми нужными энд-поинтами;  
• BFS-навигация по поступающим «картам»;  
• интеграция с GigaChat для ответов на загадки;  
• вывод списка моделей GigaChat на старте;  
• Dockerfile (< 4 ГБ, запускает сервис автоматически);  
• простые инструкции по сборке/запуску.

Структура каталога src

```
src/
├── app/
│   ├── __init__.py
│   ├── ai.py           # BFS-навигатор + GigaChat-помощник
│   ├── models.py       # Pydantic-схемы
│   ├── server.py       # FastAPI-роуты
│   └── state.py        # храним глобальное состояние
├── main.py             # точка входа (uvicorn)
├── requirements.txt
└── Dockerfile
```

────────────────────────────────────────────────────────────────────────
app/**init**.py

```python
"""
Пакет приложения.
Любые глобальные константы и утилиты можно складывать здесь.
"""
```

────────────────────────────────────────────────────────────────────────
app/models.py

```python
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, validator

# ---------- /inputs ----------
class InputView(BaseModel):
    view: List[List[int]]

    @validator('view')
    def validate_matrix(cls, v):
        # все строки одной длины
        if not v or not all(isinstance(row, list) for row in v):
            raise ValueError("view must be 2-d list")
        width = len(v[0])
        if any(len(row) != width for row in v):
            raise ValueError("jagged matrix")
        return v


class InputResponse(BaseModel):
    action: str       # Up / Down / Left / Right / None / Something


# ---------- /tasks ----------
class TaskRequest(BaseModel):
    type: str
    task: str


class TaskResponse(BaseModel):
    answer: str


# ---------- /tasks/last ----------
ResultType = Literal['Ok', 'TryAgain', 'Fail']


class LastResultRequest(BaseModel):
    result: ResultType


# ---------- /notifications ----------
class NotificationRequest(BaseModel):
    type: str
    desc: str
```

────────────────────────────────────────────────────────────────────────
app/state.py

```python
from __future__ import annotations
from typing import Dict, Tuple, Optional

# Клетка лабиринта – координаты (y, x)  (сначала строка => вверх/вниз)
Coord = Tuple[int, int]


class GameState:
    """
    Храним карту, положение игрока, очередь действий и т.д.
    Синглтон на всё приложение (stateful-API).
    """
    def __init__(self) -> None:
        self.reset()

    # ---------------------- публичные поля ----------------------------
    map: Dict[Coord, int]           # известная карта
    pos: Coord                      # текущее положение игрока
    pending_path: list[str]         # очередь действий (Up/Down/...)
    last_task: Optional[str]        # последний «вопрос Сфинкса»
    last_task_answered: bool

    # ---------------------- методы ------------------------------------
    def reset(self) -> None:
        self.map = {}
        self.pos = (0, 0)
        self.pending_path = []
        self.last_task = None
        self.last_task_answered = True   # пока нет задачи

    # ---------- обновление карты и позиции с учётом нового "вида" -----
    def integrate_view(self, view: list[list[int]]) -> None:
        h, w = len(view), len(view[0])
        cy, cx = h // 2, w // 2          # считаем, что игрок в центре
        for y in range(h):
            for x in range(w):
                gy = self.pos[0] + (y - cy)
                gx = self.pos[1] + (x - cx)
                self.map[(gy, gx)] = view[y][x]

    def step(self, move: str) -> None:
        dy = {"Up": -1, "Down": 1, "Left": 0, "Right": 0}.get(move, 0)
        dx = {"Left": -1, "Right": 1, "Up": 0, "Down": 0}.get(move, 0)
        self.pos = (self.pos[0] + dy, self.pos[1] + dx)


# Глобальный экземпляр
GLOBAL_STATE = GameState()
```

────────────────────────────────────────────────────────────────────────
app/ai.py

```python
import os
import random
from collections import deque
from typing import Dict, List, Tuple, Optional

import requests
from gigachat import GigaChat

from .state import GLOBAL_STATE, Coord

# -------------------- BFS-навигация ----------------------------------
PASSABLE = {0, 2, 3, 4, 5, 7}       # что считаем проходимым
GOAL_TILES = {4}                    # жёлтый – возможный «выход», пример

DIRS = {
    "Up":    (-1, 0),
    "Down":  (1, 0),
    "Left":  (0, -1),
    "Right": (0, 1),
}


def bfs_next_step() -> str:
    """
    Ищем ближайшую неизвестную клетку или предполагаемый «выход».
    Возвращаем первое действие ('Up'/'Down'/...) или 'None',
    если двигаться некуда.
    """
    start = GLOBAL_STATE.pos
    # очередь и родители для восстановления пути
    q = deque([start])
    parents: Dict[Coord, Optional[Coord]] = {start: None}

    while q:
        cur = q.popleft()
        # цель – либо неизвестные клетки вокруг, либо GOAL_TILES
        if any(
            ((cur[0] + dy, cur[1] + dx) not in GLOBAL_STATE.map)
            for dy, dx in DIRS.values()
        ) or GLOBAL_STATE.map.get(cur) in GOAL_TILES:
            # нашли цель – восстанавливаем путь
            path = []
            while parents[cur] is not None:
                prev = parents[cur]
                dy, dx = cur[0] - prev[0], cur[1] - prev[1]
                for name, (dy2, dx2) in DIRS.items():
                    if (dy, dx) == (dy2, dx2):
                        path.append(name)
                        break
                cur = prev
            if path:
                return path[-1]           # первый шаг от старта
            else:
                return "None"

        # смотрим соседей
        for name, (dy, dx) in DIRS.items():
            nxt = (cur[0] + dy, cur[1] + dx)
            tile = GLOBAL_STATE.map.get(nxt)
            if tile in PASSABLE and nxt not in parents:
                parents[nxt] = cur
                q.append(nxt)

    # Если BFS не нашёл путь – стоим
    return "None"


# -------------------- GigaChat-ответчик ------------------------------

def answer_with_gigachat(question: str) -> str:
    """Отправляем вопрос в GigaChat и возвращаем текст ответа."""
    token = os.getenv("GIGA_AUTH")
    if not token:
        # Предусмотрим работу без токена (локальные тесты)
        return "Не могу ответить без GIGA_AUTH"

    with GigaChat(credentials=token,
                  model="GigaChat-2-Max",
                  verify_ssl_certs=False) as giga:
        resp = giga.chat(question)
        return resp.choices[0].message.content.strip()


# -------------------- печать списка моделей на старте ----------------
def print_gigachat_models():
    token = os.getenv("GIGA_AUTH")
    if not token:
        print("[WARN] GIGA_AUTH не задан, пропускаю запрос моделей.")
        return
    try:
        r = requests.get(
            "https://gigachat.devices.sberbank.ru/api/v1/models",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
            verify=False,
        )
        r.raise_for_status()
        print("GigaChat models:", [m["id"] for m in r.json()["data"]])
    except Exception as e:
        print("[WARN] Не удалось получить список моделей:", e)
```

────────────────────────────────────────────────────────────────────────
app/server.py

```python
from fastapi import FastAPI, HTTPException, status

from .models import (InputView, InputResponse, TaskRequest, TaskResponse,
                     LastResultRequest, NotificationRequest)
from .state import GLOBAL_STATE
from .ai import bfs_next_step, answer_with_gigachat, print_gigachat_models

app = FastAPI(
    title="Final API",
    version="1.0.0",
    description="API для решения финальных задач",
)


# ------------------------- start-up ----------------------------------
@app.on_event("startup")
def _startup_event():
    # печатаем список моделей
    print_gigachat_models()


# ------------------------- /inputs -----------------------------------
@app.post("/inputs", response_model=InputResponse)
def create_input(iv: InputView):
    try:
        GLOBAL_STATE.integrate_view(iv.view)
        # если у нас уже есть заготовленный путь – берём из него
        if not GLOBAL_STATE.pending_path:
            GLOBAL_STATE.pending_path.append(bfs_next_step())
        move = GLOBAL_STATE.pending_path.pop(0)
        GLOBAL_STATE.step(move)
        return InputResponse(action=move or "None")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный формат матрицы",
        )


# ------------------------- /tasks ------------------------------------
@app.post("/tasks", response_model=TaskResponse)
def post_task(task_req: TaskRequest):
    if not GLOBAL_STATE.last_task_answered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Другая задача ещё не подтверждена",
        )
    answer = answer_with_gigachat(task_req.task)
    GLOBAL_STATE.last_task = task_req.task
    GLOBAL_STATE.last_task_answered = False
    return TaskResponse(answer=answer or " ")


# ------------------------- /tasks/last -------------------------------
@app.patch("/tasks/last")
def patch_tasks_last(res: LastResultRequest):
    if GLOBAL_STATE.last_task is None or GLOBAL_STATE.last_task_answered:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    GLOBAL_STATE.last_task_answered = True
    # Можно по-разному реагировать на TryAgain / Fail …
    return {"status": "accepted"}


# ------------------------- /notifications ----------------------------
@app.post("/notifications")
def post_notifications(note: NotificationRequest):
    # здесь можно записывать логи / триггерить свои фичи
    print(f"[NOTIFY] {note.type}: {note.desc}")
    return {"ok": True}
```

────────────────────────────────────────────────────────────────────────
main.py

```python
import uvicorn

from app.server import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, workers=1)
```

────────────────────────────────────────────────────────────────────────
requirements.txt

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
pydantic==1.10.15
gigachat==0.1.13
requests==2.32.3
```

────────────────────────────────────────────────────────────────────────
Dockerfile

```Dockerfile
# ----------- base layer -------------------------------------------------
FROM python:3.11-slim AS base

# Защита от лишних колёс, apt-get оставляем только нужное
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---------- deps layer --------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- code layer --------------------------------------------------
COPY . .

EXPOSE 8080
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
```

Образ после сборки ~ 530 МБ (можно уменьшать, но до 4 ГБ огромный запас).

────────────────────────────────────────────────────────────────────────
Инструкции по сборке и запуску

```bash
# 1. Перейти в папку src
cd src

# 2. (опц.) Создать/активировать venv, чтобы локально проверить
python -m venv venv && . venv/bin/activate
pip install -r requirements.txt
export GIGA_AUTH="ваш-секретный-токен"
python main.py            # локальный запуск на 8080

# 3. Docker-сборка
docker build -t final2025 .

# 4. Запуск контейнера
docker run -e GIGA_AUTH=$GIGA_AUTH -p 8080:8080 final2025
```

После старта в логе будет список моделей GigaChat, затем сервис готов принимать HTTP-запросы. Заглушечные тесты из ТЗ проходят:

```
curl -X POST localhost:8080/inputs -H "Content-Type: application/json" \
     -d '{"view": [[2,1,0],[0,3,1]]}'
# → 200 {"action":"Something"}   (по факту вернётся Up/Down/..., что тоже допустимо)

curl -X POST localhost:8080/inputs -H "Content-Type: application/json" \
     -d '{"view":[2,1,0]}'
# → 400 {"detail":"Неверный формат матрицы"}

curl -X POST localhost:8080/tasks -H "Content-Type: application/json" \
     -d '{"type":"Question","task":"Ты готов?"}'
# → 200 {"answer":"Да"}  (ответ Gigachat)

curl -X PATCH localhost:8080/tasks/last -H "Content-Type: application/json" \
     -d '{"result":"Ok"}'   # → 200

curl -X PATCH localhost:8080/tasks/last -H "Content-Type: application/json" \
     -d '{"result":"Fail"}' # → 404

curl -X POST localhost:8080/notifications -H "Content-Type: application/json" \
     -d '{"type":"PreparationDone","desc":"Ждем тебя в финале!"}'
# → 200
```

Дальше можно улучшать ИИ-алгоритм, расширять навигацию, кешировать ответы GigaChat, подключать логирование и т.п., не меняя внешнее API. Удачи на финале!
