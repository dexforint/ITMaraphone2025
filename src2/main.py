from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv

from models import (
    InputViewRequest,
    ActionResponse,
    ActionNoneResponse,
    TaskRequest,
    AnswerResponse,
    LastTaskResultRequest,
    NotificationRequest,
)
from state import app_state
from gigachat import get_available_models

# Загружаем переменные окружения из файла .env (для GIGACHAT_API_KEY)
load_dotenv()

app = FastAPI(
    title="Final API", description="API для решения финальных задач", version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    """
    Эта функция выполняется один раз при запуске сервера.
    Идеальное место для запроса к GigaChat.
    """
    print("Server is starting up...")
    get_available_models()
    print("Server is ready to accept requests.")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Кастомный обработчик ошибок валидации.
    По заданию, для /inputs при неверном формате нужно вернуть 400 и {"action": "None"}.
    Стандартный обработчик FastAPI возвращает 422.
    """
    if request.url.path == "/inputs":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"action": "None"},
        )
    # Для всех остальных эндпоинтов оставляем стандартное поведение
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


@app.post(
    "/inputs",
    response_model=ActionResponse,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_400_BAD_REQUEST: {"model": ActionNoneResponse}},
)
def create_input(data: InputViewRequest):
    """
    Принимает данные в матричном формате.
    В 'домашнем задании' логика не требуется, просто отвечаем заглушкой.
    Валидация происходит автоматически благодаря модели InputViewRequest.
    """
    # В финале здесь будет логика анализа `data.view` и выработка `action`
    print(f"Received input view: {data.view}")
    return ActionResponse(action="Something")


@app.post("/tasks", response_model=AnswerResponse, status_code=status.HTTP_200_OK)
def create_task(task_data: TaskRequest):
    """
    Принимает новую задачу и сохраняет ее в состоянии.
    """
    print(f"Received new task: Type='{task_data.type}', Task='{task_data.task}'")
    # Сохраняем задачу в глобальном состоянии
    app_state.set_new_task(task_data)
    # В финале здесь будет логика решения задачи, возможно с вызовом LLM
    return AnswerResponse(answer="Да")


@app.patch("/tasks/last", status_code=status.HTTP_200_OK)
def patch_last_task_result(result_data: LastTaskResultRequest):
    """
    Принимает результат выполнения последней задачи.
    Проверяет, была ли задача и не был ли результат уже принят.
    """
    print(f"Received result for last task: {result_data.result}")
    if not app_state.can_accept_result():
        # Если задачи не было или результат уже получен, возвращаем 404
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": "No task awaiting for result or result already received"
            },
        )

    # Если все ок, "принимаем" результат (меняем флаг в состоянии)
    app_state.accept_last_task_result()
    # Возвращаем пустой ответ с кодом 200
    return {}


@app.post("/notifications", status_code=status.HTTP_200_OK)
def create_notification(notification_data: NotificationRequest):
    """
    Принимает уведомления. Пока просто выводим их в консоль.
    """
    print(
        f"Received notification: Type='{notification_data.type}', Desc='{notification_data.desc}'"
    )
    # В финале эти данные могут менять внутреннее состояние агента
    return {}
