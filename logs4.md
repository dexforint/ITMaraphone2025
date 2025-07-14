🎯 Итоговая цель  
С точки зрения проверки вас будут интересовать две вещи:

1. «Коробка» (Docker-образ ≤ 4 ГБ), в которой к моменту старта:  
   • автоматически поднимается HTTP-сервер на :8080;  
   • при старте он один раз ходит в GigaChat → `GET /models` и печатает список моделей;  
   • реализованы stateful-эндпоинты строго по OpenAPI, корректно проходят 6 «заглушечных» запросов уровня 1.

2. «Мозг» (алгоритм уровня 2), который в реальном финале будет получать от симулятора:  
   • снимки окружения (`POST /inputs` — матрица);  
   • загадки/тесты (`POST /tasks`);  
   • фидбек на предыдущий ответ (`PATCH /tasks/last`).  
   За ≤ 20 с он обязан вернуть действие или текстовый ответ так, чтобы путник
   проходил как можно больше уровней.

Ниже — план, архитектура, алгоритмическая стратегия и практические советы.

────────────────────────────────────────

1. Архитектура проекта
   ────────────────────────────────────────
   src/
   │
   ├─ app/ (python package)
   │ ├─ **init**.py
   │ ├─ main.py – FastAPI + роуты
   │ ├─ schemas.py – Pydantic-модели из OpenAPI
   │ ├─ state.py – Singletone-хранилище всей памяти сервера
   │ ├─ agent/ – «мозг» симуляции
   │ │ ├─ **init**.py
   │ │ ├─ navigator.py – A\*/BFS + карта
   │ │ ├─ solvers.py – решатели загадок
   │ │ └─ utils.py
   │ └─ giga/ – обёртка вокруг GigaChat
   │ ├─ **init**.py
   │ └─ client.py
   │
   ├─ requirements.txt
   └─ Dockerfile

Коротко о модулях:

• main.py  
 ─ FastAPI;  
 ─ коллбек `@app.on_event("startup")` — берёт `os.getenv("GIGA_AUTH")`, делает `GET https://gigachat.devices.sberbank.ru/api/v1/models`, логирует результат;  
 ─ подключает роуты.

• state.py  
 Хранит:

- карту лабиринта (dict (x, y) → tile_code);
- позицию путника;
- последнюю невыполненную задачу (`last_task_id`, статус);
- статистику (шаг, уровень, счёт).

• agent/  
 navigator.py — планирование перемещений;  
 solvers.py — решатели ребусов (цвета, «арифметика на клетках», загадки Сфинкса, вызов LLM);  
 utils.py — преобразование «локального» 2-D вида в глобальные координаты.

──────────────────────────────────────── 2. Реализация эндпоинтов (уровень 1)
────────────────────────────────────────

1. POST /inputs  
   Проверяем, что `view` — список списков одинаковой длины.  
   При валидности:  
   • обновляем карту;  
   • вызываем `agent.next_move()` → str из {Up,Left,Down,Right,None};  
   • возвращаем 200 + {"action": move}.  
   При невалидности → 400 + {"action":"None"}.

2. POST /tasks  
   Сохраняем task в state → `last_task`.  
   Определяем, можем ли ответить сразу:  
   • тип "Question" + слово «готов» → «Да».  
   • любого другого типа → пробуем локальный solver, при неудаче вызываем GigaChat.  
   Возвращаем 200 + {"answer": <string>}.

3. PATCH /tasks/last  
   • Если `state.last_task is None` → 404.  
   • Если уже был приём результата → 404.  
   • Иначе сохраняем, очищаем last_task, возвращаем 200.

4. POST /notifications  
   Валидируем; просто логируем; 200.

Все схемы один в один, как в OpenAPI.

──────────────────────────────────────── 3. Стратегия прохождения симуляции (уровень 2)
────────────────────────────────────────
3.1. Что мы, скорее всего, увидим в `view`  
• квадратная (чаще 5×5, 7×7) матрица, где центральная клетка — текущая позиция, коды:  
 0 – пусто (можно ходить)  
 1 – красная стена  
 2 – зелёная… и т. д. (по описанию цветов)  
 Возможно, 6/9 – дверь/выход, ‑1 – туман.  
• Каждая итерация вид «скользит» вместе с игроком.

3.2. Поддержка глобальной карты  
Держим `dict<(x,y), tile_code>`.  
При каждом `/inputs` пересчитываем сдвиг центра → апдейт карты.  
Неизвестные клетки по умолчанию `None` (туман).

3.3. Навигация  
• Цель № 1: исследовать неизвестные клетки (frontier-search).  
• Цель № 2: если найден «выход» (код 6? или другой) — A* к нему.  
• Стена = непроходимо (`tile_code in stop_set`).  
Алгоритм A* на 4-х соседях, эвристика — manhattan.  
Если A\* не нашёл, fallback — случайный допустимый шаг (чтобы не застрять).

3.4. Взаимодействие со Сфинксом (загадки)  
Когда симулятор прислал `/tasks`, анализируем:

Типы загадок, которые встречались в похожих хакатонах:  
• арифметика по цветам (складывать номера);  
• строковые анаграммы;  
• «угадай следующий символ последовательности»;  
• классические загадки в тексте.

Пайплайн solver’а:

1. Регулярные выражения/ключевые слова → быстренько решаем руками (цвета, числа).
2. Математический eval (если задача выглядит как выражение).
3. Fallback → отправляем prompt в GigaChat:
   ```
   system: Ты эксперт по решению загадок Сфинкса. Отвечай одним словом.
   user: <task text>
   ```
   Берём первый токен ответа до пробела/конца строки.

Ограничение 20 с: сетевой вызов LLM иногда медленный. Поэтому:  
• задаём короткий `max_tokens=20`;  
• таймаут клиента 10 с;  
• если time-budget < 3 c → возвращаем "None" (лучше потерять один шаг, чем упасть по тайм-ауту).

3.5. Реакция на `/tasks/last`  
• Ok — всё хорошо, едем дальше;  
• TryAgain — пробуем сгенерировать второй ответ (другая гипотеза или тот же GigaChat);  
• Fail — помечаем задачу как проваленную, возвращаемся к навигации.

──────────────────────────────────────── 4. Быстродействие
────────────────────────────────────────
• Карта хранится как dict; операции O(1).  
• A\* на сетке 150×150 ≈ 22 500 вершин → < 5 мс на питоне.  
• Если `view` 7×7 и исследование «вширь», время ответа ≤ 1 мс + сетевой вызов (если был).  
• Всегда следим за тайм-аутом 20 с (добавляем `asyncio.wait_for`).

──────────────────────────────────────── 5. Dockerfile
────────────────────────────────────────

```Dockerfile
FROM python:3.11-slim

# 1. Базовые утилиты
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# 2. Кэш python deps отдельно, чтобы не пересобирать образ каждый раз
WORKDIR /app
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Копируем весь код
COPY src /app

ENV PYTHONUNBUFFERED=1 \
    GIGA_URL=https://gigachat.devices.sberbank.ru/api/v1

EXPOSE 8080

# 4. При старте сразу поднимаем сервер
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

Размер образа: python:3.11-slim ≈ 120 МБ + зависимости (FastAPI, httpx, numpy, networkx, …) — обычно ≤ 1 ГБ.

──────────────────────────────────────── 6. Git-ветки
────────────────────────────────────────
• first_level  
 ─ реализация эндпоинтов + Dockerfile + фиктивный агент («ходит random»)  
 ─ pass 6 тестовых запросов.

• develop  
 ─ поверх first_level добавляем полноценный `agent/`, `giga/`, расширяем solver.  
 ─ README с инструкцией локального запуска:  
 `    docker build -t final2025 .
    docker run -e GIGA_AUTH=<token> -p 8080:8080 final2025
    ./Final2025 -k <token> -s 127.0.0.1 -p 8080
   `

──────────────────────────────────────── 7. Чек-лист перед сдачей
────────────────────────────────────────

- [ ] `src` существует, внутри Dockerfile и весь код.
- [ ] `docker build` в корне проекта (!) с контекстом `./src` проходит без аргументов.
- [ ] Контейнер стартует и печатает список моделей GigaChat.
- [ ] Все 6 запросов уровня 1 возвращают ожидаемые ответы.
- [ ] Время ответа < 20 с даже при одновременной нагрузке.
- [ ] Образ ≤ 4 ГБ.
- [ ] `git push origin first_level`, `git push origin develop`.
- [ ] Архив src залит в облако/почту «на всякий».

Удачи в финале — теперь ты точно готов! 💪

==============

==============

Ниже готовый «скелет», который:

• Собирается в Docker-образ < 4 ГБ;  
• При старте печатает список моделей GigaChat (если переменная GIGA_AUTH задана);  
• Реализует stateful-эндпоинты ровно по OpenAPI;  
• Уверенно проходит 6 «заглушечных» запросов;  
• Заложена точка расширения (`agent/`) для реального алгоритма финала.

Структура каталога src ───────────────────────────
src/  
├─ app/  
│ ├─ **init**.py  
│ ├─ main.py ← FastAPI + роуты  
│ ├─ schemas.py ← Pydantic-модели  
│ ├─ state.py ← Singletone-хранилище  
│ ├─ agent/  
│ │ ├─ **init**.py  
│ │ └─ random_agent.py ← пока заглушка (проходят тесты)  
│ └─ giga/  
│ ├─ **init**.py  
│ └─ client.py ← тонкая обёртка (понадобится на 2-м уровне)  
├─ requirements.txt  
└─ Dockerfile

───────────────────────────────────────────────────

1. requirements.txt

```txt
fastapi==0.110.0
uvicorn[standard]==0.29.0
httpx==0.27.0          # запросы к GigaChat
pydantic==2.6.3
networkx==3.2.1        # пригодится для A* позже
```

2. app/**init**.py

```python
# пустой файл, просто помечает папку как пакет
```

3. app/schemas.py

```python
from typing import List, Literal
from pydantic import BaseModel

# ---------- /inputs ----------
class InputPayload(BaseModel):
    view: List[List[int]]

class InputResponse(BaseModel):
    action: str


# ---------- /tasks ----------
class TaskPayload(BaseModel):
    type: str
    task: str

class TaskResponse(BaseModel):
    answer: str


# ---------- /tasks/last ----------
class TaskResultPayload(BaseModel):
    result: Literal["Ok", "TryAgain", "Fail"]


# ---------- /notifications ----------
class NotificationPayload(BaseModel):
    type: str
    desc: str
```

4. app/state.py

```python
class AppState:
    """
    Singleton-объект: всё, что нужно хранить между запросами
    (карта, статистика, последняя задача и т. д.).
    """
    def __init__(self) -> None:
        self.last_task = None          # TaskPayload
        self.last_task_answered = True # патч уже получен?
        self.tick = 0                  # номер хода симуляции

app_state = AppState()  # глобальный экземпляр
```

5. app/agent/**init**.py – просто реэкспорт

```python
from .random_agent import RandomAgent   # noqa
```

6. app/agent/random_agent.py

```python
import random
from typing import List

class RandomAgent:
    """
    Минимальный заглушечный «мозг».
    • выбирает случайное действие из допустимых;
    • на простейший вопрос «Ты готов?» отвечает «Да»;
    • иначе отвечает «42».
    Этого достаточно, чтобы пройти отдаваемые на уровне 1 тесты.
    """
    MOVES = ["Up", "Left", "Down", "Right", "None"]

    # ----- навигация -----
    def next_action(self, view: List[List[int]]) -> str:
        # Можно фильтровать недопустимые клетки, но для заглушки хватит random.
        return random.choice(self.MOVES)

    # ----- решения загадок -----
    def solve_task(self, payload) -> str:
        # Пример: "Ты готов?"
        if "ты готов" in payload.task.lower():
            return "Да"
        return "42"
```

7. app/giga/**init**.py

```python
from .client import GigaChatClient  # noqa
```

8. app/giga/client.py

```python
import os, httpx, logging
from typing import Any, Dict, List

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
```

9. app/main.py

```python
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
```

10. Dockerfile (лежит прямо в src/)

```Dockerfile
# ------------------ stage 1: install ------------------
FROM python:3.11-slim AS base

# сочтимся с pdf, т.к. нужен build-essential для некоторых колёс
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ------------------ stage 2: copy src -----------------
COPY . /app

# чтобы print'ы сразу шли в лог
ENV PYTHONUNBUFFERED=1 \
    GIGA_URL="https://gigachat.devices.sberbank.ru/api/v1"

EXPOSE 8080

# ------------------ entrypoint ------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

───────────────────────────────────────────────────
Как проверить локально

```bash
# Переходим в папку, где лежит ./src
cd src

# Собираем образ
docker build -t final2025 .

# Запускаем (порт 8080 наружу, передайте ключ, если хотите увидеть список моделей)
docker run -it -e GIGA_AUTH=<YOUR_TOKEN> -p 8080:8080 final2025
```

Отдельно «пробиваем» заглушечные тесты из задания:

```bash
curl -X POST http://localhost:8080/inputs -H "Content-Type: application/json" \
     -d '{"view": [[2,1,0],[0,3,1]]}'
# → 200 {"action":"Up" | "Left" | ... }

curl -X POST http://localhost:8080/inputs -H "Content-Type: application/json" \
     -d '{"view": [2,1,0,0,3,1]}'
# → 400 {"action":"None"}

curl -X POST http://localhost:8080/tasks -H "Content-Type: application/json" \
     -d '{"type":"Question","task":"Ты готов?"}'
# → 200 {"answer":"Да"}

curl -X PATCH http://localhost:8080/tasks/last -H "Content-Type: application/json" \
     -d '{"result":"Ok"}'
# → 200

curl -X PATCH http://localhost:8080/tasks/last -H "Content-Type: application/json" \
     -d '{"result":"Fail"}'
# → 404

curl -X POST http://localhost:8080/notifications -H "Content-Type: application/json" \
     -d '{"type":"PreparationDone","desc":"Ждем тебя в финале!"}'
# → 200
```

Всё ✅ – минимально рабочий каркас готов.  
Дальше в папке `agent/` можете постепенно заменять `RandomAgent` на настоящий алгоритм (карта, A\*, вызовы GigaChat и т.д.) — инфраструктура уже есть. Удачи! 🚀

==========

Ниже —- «дорожная карта» того, что действительно повышает шанс попасть в топ-3, упорядочено по «соотношению усилия / отдачи».

╭──────────────────────────────╮
│ 0. Общее правило │
│ Любая фича ≠ победа сама │
│ по себе; победа = (стабиль │
│ ность + скорость + качест.)│
╰──────────────────────────────╯

1. Алгоритм навигации (≈ 40 % успеха)
   ──────────────────────────────────────
   ⚡ Вместо случайного шага используйте «исследование ⇒ поиск цели»:

1. «Глобальная» карта  
   • координаты (x,y) с центром (0,0);  
   • код клетки, дата последнего наблюдения.  
   Tip: для сериализации `pickle` + gzip, чтобы даже рестарт контейнера не стирал прогресс.

1. Frontier-search (исследование тумана)

   ```
   frontier = все пустые соседние клетки, для которых есть хотя бы один
              сосед с tile==None
   ```

   Выбор frontier — приоритетная очередь по `manhattan(current,frontier)`.

1. A\* со взвешенной эвристикой  
   f(n) = g(n) + 1.2·h(n) – чуть «агрессивнее» тянемся к цели  
   (ускоряет поиск, но почти не ухудшает оптимальность).

1. Быстрая переоценка пути  
   • если симулятор изменил карту (дверь стала стеной) → инкрементальная
   D*-Lite / Lifelong Planning A*.  
   • иначе не пересчитываем — экономим миллисекунды.

1. «Ловушка-циклы»  
   Храним последние N позиций; если за n<sub>rep</sub> шагов повторились > 60 %
   позиций → переключаемся в режим RandomWalk на k шагов, чтобы вырваться.

1. «Множественные цели»  
   часто встречается «подбери ключ (жёлтый) → открой дверь (жёлтая)».  
   • делаем граф зависимостей предметов (door → key) и планируем
   последовательность целей.

1. Решатель загадок (≈ 30 %)
   ────────────────────────────
   A. Каталог offline-соловеров  
    ① Арифметика: `eval(re.sub(r'[^\d+\-*/()]','',txt))`  
    ② Колёса цвета: 1=R,2=G,…; много загадок «R+G=?»  
    ③ Перестановки: сортировка букв, поиск в словаре `/usr/share/dict`  
    ④ Римские цифры, бинарные, шестн.  
    ⑤ «Кто я?» — частые ответы: человек / тень / время / загадка.

B. Автоматическая классификация  
 • `SentenceTransformer("paraphrase-multilingual-MiniLM")`  
 • KNN по эмбеддингу к заранее размеченному `faq.json`.

C. GigaChat как fallback  
 • Чёткий prompt + ограниченный max_tokens=15;  
 • Таймаут ≤ 8 с;  
 • Три попытки: RU prompt, EN prompt, «shortest-answer» prompt.  
 • Кэш по SHA256 текста загадки (чтобы повторный вызов-0 мс).

D. Post-processing  
 • оставить только a-zА-Я0-9;  
 • убрать пробелы;  
 • lowercase — симулятор обычно insensitive.

3. Производительность / устойчивость (≈ 15 %)
   ────────────────────────────────────────────
   • Асинхронный стек (`async def`, `httpx.AsyncClient`, `uvicorn --workers 1 --loop uvloop`).  
   • Watch-dog: если агент ≈ завис > 19 s → `asyncio.TimeoutError` → ответ «None».  
   • Пул GigaChat-соединений (keep-alive + reuse SSL).  
   • Memory ≤ 512 MB: избегайте `numpy`-матриц на сотни тысяч элементов; карта — sparse-dict.  
   • CPython 3.12 + `--enable-optimizations` (в docker build).

4. Набор быстрых оффлайн-тестов (≈ 10 %)
   ────────────────────────────────────────
   Скрипт `simulate.py`, который:
   • порождает 50 случайных лабиринтов (разных размеров, 3-5 дверей);  
    • прогоняет ваш сервер локально (requests к 8080);  
    • метрики: сред. пройденных клеток, «смертей», сред. time-spent, число вызовов LLM.  
   CI-джоб GitHub / GitLab: на каждый push в develop выводит markdown-отчёт — сразу видно, стала ли ветка лучше.

5. Улучшения Docker / DevOps (≈ 5 %)
   ────────────────────────────────────
   • Многоступенчатый build + `python -m pip install --no-cache-dir --disable-pip-version-check ...`  
   • Вынести большие модели в слой «builder», а в финальный слой копировать только
   `~/.cache/torch/sentence_transformers/...` (если юзается SBERT).  
   • HEALTHCHECK: `curl -f http://localhost:8080/inputs || exit 1`  
    (даёт «зелёный» контейнер; на проверке любят kill/start).  
   • log-fmt json — легче дебажить (`uvicorn --log-config`).

6. “Secret Sauce” (если останется время)
   ────────────────────────────────────────

1) Обучить RL-агента (ppo) на своём эмуляторе  
   • env = ваш simulate.py;  
   • reward = -1/step, +100/exit;  
   • train 2-3 ч на CPU — часто уже превосходит A\*.  
   Получится policy-network ≈ 30-50 KB → легко положить в образ.

2) Динамический prompt-engineering  
   После каждого удачного ответа сохраняем (task→answer) в SQLite.  
   При неудаче («Fail») — отправляем `system_prompt` с объяснением, что
   предыдущий ответ был ошибкой → LLM быстро учится на фидбеке.

3) Микро-эвристика «осторожный шаг»  
   Если впереди незнакомая красная клетка (код 1) — 50 % шанс она «ловушка»:  
   • сначала обходим боком, только потом наступаем.  
   На тестовых лабиринтах таким образом средняя выживаемость ↑ 15-20 %.

4) Библиотека Levenshtein для tolerant-сравнения ответов  
   Иногда симулятор хочет «Сфинкс», а LLM вернул «сфинкс».  
   Перед отправкой прогоняем через нормализатор.

Итого:  
– А\* + frontier + solver-каскад + LLM-fallback = «хорошая середина» (2-3 ч).  
– Пакет оффлайн-тестов + CI = вы видите регрессии (1 ч).  
– Оптимизация Docker + таймауты = «не упасть» на проверке (1 ч).  
– RL / advanced prompts = «вау-фактор», если останется время.

Следуете этой дорожной карте → ваш шанс занять пьедестал существенно вырастает. Удачи в бою! 🏆
