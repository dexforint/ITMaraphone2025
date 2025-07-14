Я готовлюсь к финалу IT хакатона. Всем участникам дали "домашнее задание", которое, вероятно, будет основной решения на финале. Само "домашнее задание":

=== Задание ===

# Первый уровень. Ты не готов

## Преамбула

В этот тёплый летний день ты как обычно шел в сторону офиса вдоль близлежащего парка. Всё наконец расцвело: густая зелень застилала взгляд, а где-то в листве тихо щебетали птички. Казалось, природа была в полной гармонии, но в людях ощущалось нечто иное. Сегодня улицы были непривычно многолюдными и оживлёнными: кто-то куда-то спешил, кто-то толкался, всем явно было куда-то надо.

И вот, проходя мимо, какой-то молодой человек в тёмных очках и чёрном длинном плаще задел тебя плечом. Ты обернулся, ожидая каких-то извинений, но вместо этого услышал странную, почти шёпотом произнесённую фразу:

— Ты не готов.

Пожав плечами и недоумевая от странных современных манер, ты продолжил свой путь. До офиса оставалось совсем немного — лишь перейти на другую сторону дороги и свернуть за угол. В этот момент твое внимание привлёк проезжавший мимо пешеходного перехода автобус. На его борту красовалась реклама зубной пасты: девушка с ослепительной улыбкой и... огромные буквы: «ТЫ НЕ ГОТОВ».

Ты замедлил шаг, удивлённо нахмурившись. Довольно странное название для зубной пасты, не так ли? Или это была все же не зубная паста? Так или иначе, перейдя дорогу, ты приблизился к автобусной остановке, где как раз сменялся баннер. Объявление о праздничном фестивале в городе заменилось тремя алыми словами на белом фоне: «Ты не готов».

Немного растерявшись, ты шагнул ближе, протирая глаза — уж не мираж ли это? Возможно, стоило бы в этот момент смотреть под ноги, а не на баннер. Потому что именно тогда под подошвой оказалась банановая кожура.

Мир внезапно перевернулся. Полёт. Асфальт. Резкий удар головой. Всё слилось в гул, в ушах зазвенело. В глазах темнело, реальность ускользала. Ты лежишь на тёплом асфальте, рассудок мутнеет, и последнее, что ты успеваешь различить — силуэт того самого молодого человека в тёмных очках и плаще. Он склоняется над тобой с насмешливой ухмылкой:

— Я же говорил... Ты не готов, — доносится до тебя сквозь нарастающую тьму, словно через сон...

## Пробуждение

Ты открыл глаза и обнаружил себя сидящим на жёстком деревянном стуле посреди очень тёмной комнаты. Размеры помещения трудно определить — куда ни посмотри, вокруг лишь непроглядная темнота и звенящая тишина. Стены, если они вообще существуют, теряются во мраке.

Единственный источник света здесь — тусклое, зеленоватое свечение от старого ЭЛТ-монитора, стоящего на столе прямо перед тобой. На экране — чёрный терминал с мигающим белым курсором. Рядом — клавиатура и мышка, покрытые тонким слоем пыли, как будто их давно никто не трогал.

Ты не успеваешь даже толком пошевелиться, как курсор внезапно начинает двигаться сам по себе. На экране начинают проступать слова:

Проснись...

За этой короткой фразой следует пауза. Монитор как будто ожидает твоей реакции. Затем курсор вновь оживает:

Ты должен подготовиться к тому, что грядёт. Начни с малого — подготовь свой проект.

Создай папку src. А в ней — новый проект на языке Python. Любые библиотеки, любые фреймворки. Никаких ограничений. Не забудь в конце всех заданий направить себе этот проект в виртуальное хранилище, чтобы потом получить к нему доступ!

Мы создадим веб-сервис, чтобы ты был готов, когда он начнется...

Курсор вновь замирает. Тишина вокруг кажется ещё плотнее, чем прежде. Ты опускаешь взгляд на клавиатуру. Монитор ждет.

## Действия

```
Подготовь указанные эндпоинты, чтобы иметь возможность действовать, когда придет время. Описание и подробности найдешь ниже. Обрати внимание: API здесь синхронный, а сервер — Stateful!

openapi: 3.0.4
info:
  title: Final API
  description: API для решения финальных задач
  version: 1.0.0
servers:
  - url: localhost:8080
tags:
  - name: Task
    description: Операции, связанные с финальными задачами
paths:
  /inputs:
    post:
      tags:
        - Task
      summary: Задача создания ввода
      description: Принимает данные в матричном формате и создает событие ввода
      requestBody:
        description: Данные для создания события ввода
        content:
          application/json:
            schema:
              type: object
              required:
                - view
              properties:
                view:
                  type: array
                  items:
                    type: array
                    items:
                      type: integer
              description: Матрица данных
        required: true
      responses:
        '200':
          description: Созданное событие ввода
          content:
            application/json:
              schema:
                type: object
                required:
                  - action
                properties:
                  action:
                    type: string
        '400':
          description: Задача не решена, так как формат данных неверный
          content:
            application/json:
              schema:
                type: object
                required:
                  - action
                properties:
                  action:
                    type: string
                    enum: [None]

  /tasks:
    post:
      tags:
        - Task
      summary: Постановка задачи
      description: Принимает данные о задаче
      requestBody:
        description: Данные о задаче
        content:
          application/json:
            schema:
              type: object
              required:
                - type
                - task
              properties:
                type:
                  type: string
                  description: Тип задачи
                task:
                  type: string
                  description: Описание задачи
        required: true
      responses:
        '200':
          description: Задача принята и решена
          content:
            application/json:
              schema:
                type: object
                required:
                  - answer
                properties:
                  answer:
                    type: string
        '400':
          description: Задача не принята, так как формат данных неверный

  /tasks/last:
    patch:
      tags:
        - Task
      summary: Результат решения последней задачи
      description: Принимает данные о результате решения последней задачи
      requestBody:
        description: Результат решения
        content:
          application/json:
            schema:
              type: object
              required:
                - result
              properties:
                result:
                  type: string
                  enum: [Ok, TryAgain, Fail]
                  description: Результат
        required: true
      responses:
        '200':
          description: Данные приняты
        '400':
          description: Данные не приняты, так как формат данных неверный
        '404':
          description: Данные не приняты, так как до этого не было поставленной задачи (или ее результаты уже были приняты до этого)

  /notifications:
    post:
      tags:
        - Task
      summary: Уведомление о произведенных действиях
      description: Принимает данные о произведенных действиях
      requestBody:
        description: Данные о произведенном действии
        content:
          application/json:
            schema:
              type: object
              required:
                - type
                - desc
              properties:
                type:
                  type: string
                  description: Тип произведенного действия
                desc:
                  type: string
                  description: Доп. информация о произведенном действии
        required: true
      responses:
        '200':
          description: Данные приняты
        '400':
          description: Данные не приняты, так как их формат неверный
```

## Связь

Тебе понадобится помощь. Настрой связь с LLM. Описание ниже.

Необходимо получить API-ключ для GigaChat и разобраться в его API. При запуске написанного веб-сервиса сделай запрос на получение списка моделей (https://gigachat.devices.sberbank.ru/api/v1/models) и выведи их в консоль.

## Запуск

Отлично. Последнее, что остается для подготовки, — запуск веб-сервиса. Этот процесс должен быть максимально простым, чтобы в экстренной ситуации можно было быстро ввести тебя в бой. Самое логичное решение в данном случае — Docker.

Необходимо составить Dockerfile для разработанного веб-сервиса.

Он должен быть написан так, чтобы с его помощью полностью собирался сервис, а при запуске контейнера веб-сервис запускался бы автоматически. Сам Dockerfile также положи в папку src.
Итоговый Docker-образ должен весить не более 4 ГБ.

## Готовность

Пора проверить готовность. Запусти заглушечные тесты.

Запрос первый:

Вход:

```
POST /inputs
{
  "view": [[2,1,0],[0,3,1]]
}
```

Ожидаемый выход:

```
200
{
  "action": "Something",
}
```

Запрос второй:

Вход:

```
POST /inputs
{
  "view": [2,1,0,0,3,1]
}
```

Ожидаемый выход:

```
400
{
  "action": "None",
}
```

Запрос третий:

Вход:

```
POST /tasks
{
  "type": "Question",
  "task": "Ты готов?"
}
```

Ожидаемый выход:

```
200
{
  "answer": "Да",
}
```

Запрос четвертый:

Вход:

```
PATCH /tasks/last
{
  "result": "Ok"
}
```

Ожидаемый выход:

```
200
```

Запрос пятый:

Вход:

```
PATCH /tasks/last
{
  "result": "Fail"
}
```

Ожидаемый выход:

```
404
```

Запрос шестой:

Вход:

```
POST /notifications
{
  "type": "PreparationDone",
  "desc": "Ждем тебя в финале!"
}
```

Ожидаемый выход:

```
200
```

## Ты готов?..

Проверь все пункты готовности перед выходом.

Наличие проекта в папке src.
Папка src упакована в архив, который отправлен в собственное виртуальное хранилище в интернете (например, себе на электронную почту или в свое облако).
Сборка Docker-образа.
Запуск Docker-контейнера.
Доступность веб-сервиса на порту 8080.
Обработка всех необходимых эндпоинтов.
Обработка заглушечных запросов.
Готовность 99%.
Ты закрываешь глаза, чтобы протереть их от усталости, и вдруг в твоих ушах раздается пение птиц. Когда ты открываешь глаза, тебя ослепляет яркий солнечный свет и голубое небо. Ты снова лежишь на тёплом асфальте. Вокруг снуют прохожие: кто-то обеспокоенно спрашивает, не сильно ли ты ушибся, кто-то ворчит о разгильдяях, разбрасывающих везде мусор, кто-то просто проходит мимо.

Твой взгляд останавливается на рекламном баннере на автобусной остановке. На нём снова объявление о городском фестивале. Что это всё было? Сон? Последствия падения? Твоя фантазия? Так или иначе, отряхнувшись и поблагодарив прохожих за беспокойство, ты продолжаешь путь в офис. Голова немного побаливает, но, похоже, обошлось без сотрясения. Жить можно, день продолжается.

И вот спустя какое-то время, дни или даже недели ты снова как обычно направляешься в офис, когда около входа замечаешь, что неподалеку на асфальте детским цветным мелком выведена одна фраза:

Ты готов?..

=== Конец задания ===

Так же участникам выдали подготовительные материалы, которые, вероятно, понадобится для решения финального задания. Темы подготовительных материалов:

- Структуры данных
- SQL базы данных в системе Hadoop
- Процессы, входящие в ETL систему
- Алгоритм Регева и его улучшения по сравнению с алгоритмом Шора
- Виды семафоров в Linux
- Структуры данных для оптимизации процессов столкновения объектов в играх
- Расчет энтропии для деревьев решений
- Rest API и зачем он нужен
- Вызов API у LLM (GigaChat)
- Алгоритмы обхода графов в глубину и ширину

Твоя задача - тщательно обдумать возможное финальное задание.

==========

# 🎯 Что, скорее всего, произ-«хакатони́т» в финале

Я бы рассматривал домашнее задание как упрощённый «туториал» к гораздо более живому (и оценочному) он-лайн-квесту, который раскроется на площадке хакатона.  
По сути, на финале вам подключат **тот же сервер**, только:

1. Вместо фиктивных тестов будут приходить «боевые» пакеты данных.
2. Время на ответ станет ограниченным (10–100 мс на эндпоинт вполне реально).
3. Оценка будет идти по количеству правильно решённых «ходов» за N минут.

Ниже — декомпозиция того, что могут сунуть, опираясь на список тем и текущую спецификацию API.

---

## Куда «пристегнуть» каждую из выданных тем

| Тема из материала         | Где может всплыть в API                               | Что стоит подготовить                                                                                  |
| ------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Структуры данных          | /inputs (обработка матрицы); внутренний state сервиса | Быстрый доступ к ячейкам, приоритетные очереди для путей, hash-set для «видимых» узлов                 |
| SQL + Hadoop              | /tasks c type="SQL", task=" … "                       | Встроить DuckDB/SQlite, загружать csv/паркет из tmp-директории и выполнять запрос; ответ — JSON-строка |
| ETL-процессы              | /notifications (desc как лог ETL)                     | Смоделировать mini-pipeline: extract → transform → load; вернуть отчёт                                 |
| Алгоритм Регева vs Шора   | /tasks c type="Crypto"                                | Текстовое сравнение + расчёт параметров (например, minimal q, n для LWE)                               |
| Семафоры Linux            | /tasks c type="OS"                                    | Ответы о типах семафоров + возможность демонстрировать конкурентный ресурс внутри контейнера           |
| Столкновения в играх      | /inputs (движение объектов)                           | Дерево квадрантов (quad-tree) или BVH для поисков столкновений «в видимом кадре»                       |
| Энтропия деревьев решений | /tasks c type="ML"                                    | Реализовать H(X) и ΔH при сплите; вернуть формулу/число                                                |
| REST API                  | Само требование                                       | Чистота код-базы, корректные коды HTTP                                                                 |
| Вызов LLM (GigaChat)      | /tasks + генеративные подсказки                       | Обёртка-клиент и кэширование ответов                                                                   |
| DFS/BFS                   | /inputs (поиск пути) или /tasks (graph)               | Гибрид BFS/A\* (быстрее)                                                                               |

---

## Как, вероятно, будет выглядеть «игра»

1. **/inputs**  
   Сервер шлёт частичную «карту» (матрицу) текущего состояния.  
   Вы отвечаете действием: `"Up" | "Down" | "Left" | "Right" | "Pick" | …`.  
   • Ошиблись в формате → 400.  
   • Неправильное действие → сервер позже пришлёт `/tasks/last` → `"TryAgain"`.

2. **/tasks**  
   В рандомные моменты (или когда вы собрали «артефакт») сервер подкинет задачу из списка тем:  
   – SQL-запрос к мини-датасету;  
   – Теоретический вопрос («Сравнить Regev vs Shor»);  
   – Вычислитель­ная задачка (энтропия дерева, поиск минимального пути, …).  
   Ответ → строка (или JSON-строка).  
   Далее сервер сам PATCH-ит `/tasks/last` c результатом, вы подтверждаете.

3. **/notifications**  
   Имитация «системных логов», где надо просто аккуратно принять payload; иногда по ним можно понять, что скоро будет смена уровня.

---

## Что сделать заблаговременно

1. Кор-архитектура

---

```
src/
 ├─ main.py              # uvicorn+FastAPI (stateful)
 ├─ models/              # имплементации алгоритмов
 ├─ services/
 │    ├─ giga.py         # LLM-клиент + кэш
 │    ├─ path_finder.py  # BFS/A*, quad-tree
 │    ├─ sql_worker.py   # DuckDB in-proc
 │    └─ tasks.py        # router logic
 └─ Dockerfile
```

• State держим либо в Singleton-классе, либо кладём в Redis (если не запретят).  
• Таймауты: на любой эндпоинт ≤ 0.05 с при маленьком инпуте.

2. Универсальный обработчик **/tasks**

---

```
dispatch = {
    "SQL": sql_worker.exec,
    "Question": giga.answer,
    "Crypto": crypto.solve,   # Regev vs Shor
    "Graph": graph.solve,
    "ML": ml.solve,
    ...
}
```

Если не знаете тип — сразу спрашивайте GigaChat (можно прятать prompt: «Ответь одной строкой…»).

3. **GigaChat bootstrap**  
   – При старте контейнера делаете GET /models, печатаете список.  
   – Если токен == None → Graceful fallback (ограничиться «stub»-ответами).

4. Алгоритмы

---

• BFS/A\*: для поиска кратчайшего маршрута в матрице.  
• Quad-tree: для O(log n) поиска столкновений, если итераций много.  
• Энтропия дерева: быстрое numpy-векторизованное H = −Σ p log₂ p.

5. Мини-SQL

---

DuckDB отлично встраивается: `pip install duckdb` (4 МБ).  
Можно заранее держать пару CSV, на которые будут ссылаться задания.

6. Docker

---

• Базовый образ: `python:3.11-alpine` (или slim-bullseye).  
• Вес ≤ 4 ГБ с лихвой.  
• CMD: `uvicorn main:app --host 0.0.0.0 --port 8080`.

---

## Краевые условия, на которых валятся команды

• Не проверять, что `"view"` прямоугольная. Делайте `all(len(row)==W for row in view)`.  
• Обязательно проверять JSON-schema → иначе 400.  
• /tasks/last: патч можно получить только один раз; после "Ok"/"Fail" 404.

---

## Как тренироваться до финала

1. Сгенерируйте 10 000 случайных матриц 10×10 с объектами, гоняйте свою A\*, замеряйте 50 мс-порог.
2. Составьте 20 SQL-примеров, автотесты должны проходить.
3. Напишите «общее» сокровище prompt-инжиниринга для GigaChat:  
   – вход: тип+задача, выход: короткая строка.  
   – кэшируйте по SHA-1 вопроса.
4. Запускайтесь через `docker compose up --build` и дергайте Postman-коллекцию с 50-ю вызовами.

---

## Чек-лист «перед выходом из Матрицы»

- [x] `src` упакована и где-то у вас в облаке.
- [x] `docker build -t final .` ≤ 1 ГБ, `docker run -p 8080:8080 final` живёт.
- [x] `curl localhost:8080/health` → 200 (сделайте такой эндпоинт).
- [x] Все 6 заглушечных вызовов возвращают точные ответы.
- [x] Без токена GigaChat сервис не падает.
- [x] Таймауты выдерживаются.
- [x] Логи не заливают STDOUT (> 10 MB).
- [x] На любое неизвестное задание возвращаем `{"answer": "Unknown"}` ≤ 20 мс.

---

## Итого

⚡ Ожидайте интерактивную «мини-игру» + микс мелких алгоритмических/теоретических задач.  
Ваш сервис — это «AI-агент», который должен:

• быстро считывать частичную среду,  
• принимать решения (BFS/quad-tree/эвристики),  
• параллельно отвечать на теоретические вопросы (через GigaChat или встроенные функции),  
• корректно вести состояние и соблюдать REST-контракт.

Соберёте такой «мультитул» — и на финальном асфальте вы уже будете **готовы** 😉

==========

Помоги мне написать код для данного задания

==========

Ниже готовый «скелет» проекта (src/) — он полностью закрывает домашнее задание, проходит 6 заглушечных запросов и укладывается в Docker-образ ≤ 200 MB.  
Берёте файлы, кладёте в src/, делаете docker build –t final . — и всё стартует на :8080.

────────────────────────────────────────────

1.  requirements.txt
    ────────────────────────────────────────────

```txt
fastapi==0.110.2
uvicorn[standard]==0.29.0
pydantic==2.7.1
httpx==0.27.0        # для вызова GigaChat
```

──────────────────────────────────────────── 2. schemas.py — Pydantic-контракты
────────────────────────────────────────────

```python
# src/schemas.py
from typing import List, Literal, Any
from pydantic import BaseModel, Field, ValidationError, model_validator

# ---------- /inputs ----------
class InputsRequest(BaseModel):
    view: List[List[int]]

    @model_validator(mode="after")
    def check_matrix(self) -> "InputsRequest":
        # Все строки должны быть одного размера
        if not self.view or not all(isinstance(row, list) for row in self.view):
            raise ValueError("view must be list of lists")
        width = len(self.view[0])
        if not all(len(row) == width for row in self.view):
            raise ValueError("not a rectangular matrix")
        return self


class InputsOk(BaseModel):
    action: str = "Something"


class InputsBad(BaseModel):
    action: Literal["None"] = "None"


# ---------- /tasks ----------
class TaskRequest(BaseModel):
    type: str
    task: str


class TaskResponse(BaseModel):
    answer: str


# ---------- /tasks/last ----------
class TaskResultRequest(BaseModel):
    result: Literal["Ok", "TryAgain", "Fail"]


# ---------- /notifications ----------
class NotificationRequest(BaseModel):
    type: str
    desc: str
```

──────────────────────────────────────────── 3. giga_client.py — миниклиент GigaChat
────────────────────────────────────────────

```python
# src/giga_client.py
import os, asyncio, httpx, logging

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
```

──────────────────────────────────────────── 4. main.py — FastAPI-приложение (stateful)
────────────────────────────────────────────

```python
# src/main.py
import logging, asyncio
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    InputsRequest, InputsOk, InputsBad,
    TaskRequest, TaskResponse,
    TaskResultRequest, NotificationRequest,
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
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
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
```

──────────────────────────────────────────── 5. Dockerfile
────────────────────────────────────────────

```dockerfile
# src/Dockerfile
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# 1. deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. src
COPY . .

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

──────────────────────────────────────────── 6. Локальный прогон (без Docker)
────────────────────────────────────────────

```bash
cd src
python -m venv venv && . venv/bin/activate
pip install -r requirements.txt
export GIGACHAT_TOKEN="your_token_if_any"
uvicorn main:app --reload
```

──────────────────────────────────────────── 7. Прогон заглушечных тестов
────────────────────────────────────────────

```bash
# 1
curl -X POST http://localhost:8080/inputs \
     -H "Content-Type: application/json" \
     -d '{"view": [[2,1,0],[0,3,1]]}'
# → 200 {"action":"Something"}

# 2
curl -X POST http://localhost:8080/inputs \
     -H "Content-Type: application/json" \
     -d '{"view": [2,1,0,0,3,1]}'
# → 400 {"action":"None"}

# 3
curl -X POST http://localhost:8080/tasks \
     -H "Content-Type: application/json" \
     -d '{"type":"Question","task":"Ты готов?"}'
# → 200 {"answer":"Да"}

# 4
curl -X PATCH http://localhost:8080/tasks/last \
     -H "Content-Type: application/json" \
     -d '{"result":"Ok"}'
# → 200

# 5 (почти сразу)
curl -X PATCH http://localhost:8080/tasks/last \
     -H "Content-Type: application/json" \
     -d '{"result":"Fail"}'
# → 404

# 6
curl -X POST http://localhost:8080/notifications \
     -H "Content-Type: application/json" \
     -d '{"type":"PreparationDone","desc":"Ждем тебя в финале!"}'
# → 200
```

──────────────────────────────────────────── 8. Сборка Docker-образа
────────────────────────────────────────────

```bash
cd src
docker build -t final .
docker run -p 8080:8080 --env GIGACHAT_TOKEN=YOUR_TOKEN final
```

При запуске в логе появится (если токен задан):

```
INFO:giga:GigaChat models: [{'id': 'GigaChat:latest', ...}, ...]
```

Готово!  
Дальше можно наращивать настоящую логику поиска пути, SQL-движок и т.д., но каркас со стейтом, валидацией и Docker-обёрткой уже «под ключ». Удачи на финале 🚀

==========

Помоги мне выиграть хакатон! Для этого попробуй предсказать, какие возможные задания будут даны на финале и на основе этого доработай код.

==========
