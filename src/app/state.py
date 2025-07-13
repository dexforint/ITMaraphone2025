from .models import TaskBody


class State:
    last_task: TaskBody | None = None
    result_received: bool = False


STATE = State()
