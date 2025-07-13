from typing import List, Literal, Any

from pydantic import BaseModel, field_validator


class InputBody(BaseModel):
    view: List[List[int]]

    # В pydantic v2 используем field_validator
    @field_validator("view", mode="before")
    @classmethod
    def check_matrix(cls, v: Any) -> list[Any]:
        if not isinstance(v, list) or not all(isinstance(row, list) for row in v):
            raise ValueError("Not a matrix")
        return v


class InputRespOk(BaseModel):
    action: str = "Something"


class InputRespBad(BaseModel):
    action: Literal["None"] = "None"


class TaskBody(BaseModel):
    type: str
    task: str


class TaskResp(BaseModel):
    answer: str


class PatchBody(BaseModel):
    result: Literal["Ok", "TryAgain", "Fail"]


class NotificationBody(BaseModel):
    type: str
    desc: str
