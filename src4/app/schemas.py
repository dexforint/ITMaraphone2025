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