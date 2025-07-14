from pydantic import BaseModel, Field
from typing import List, Literal, Optional


# --- Модели для /inputs ---
class InputViewRequest(BaseModel):
    # Используем Field для более точной валидации: массив, содержащий массивы целых чисел
    view: List[List[int]]


class ActionResponse(BaseModel):
    action: str


class ActionNoneResponse(BaseModel):
    action: Literal["None"] = "None"


# --- Модели для /tasks ---
class TaskRequest(BaseModel):
    type: str
    task: str


class AnswerResponse(BaseModel):
    answer: str


# --- Модели для /tasks/last ---
class LastTaskResultRequest(BaseModel):
    result: Literal["Ok", "TryAgain", "Fail"]


# --- Модели для /notifications ---
class NotificationRequest(BaseModel):
    type: str
    desc: str
