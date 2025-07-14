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
