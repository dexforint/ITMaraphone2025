from typing import Optional
from models import TaskRequest


class AppState:
    """
    Класс для хранения состояния приложения.
    Поскольку в Python модули являются синглтонами, объект app_state
    будет единым для всего приложения.
    """

    def __init__(self):
        # Храним информацию о последней полученной задаче
        self.last_task: Optional[TaskRequest] = None
        # Флаг, который показывает, был ли уже получен результат для последней задачи
        self.last_task_result_received: bool = True

    def set_new_task(self, task: TaskRequest):
        """Вызывается при получении новой задачи через /tasks."""
        self.last_task = task
        self.last_task_result_received = False
        print(f"New task received: {task}. Waiting for result.")

    def accept_last_task_result(self):
        """Вызывается при успешном получении результата через /tasks/last."""
        self.last_task_result_received = True
        print(f"Result for task '{self.last_task.task}' accepted.")

    def can_accept_result(self) -> bool:
        """Проверяет, можно ли принять результат для последней задачи."""
        return self.last_task is not None and not self.last_task_result_received


# Создаем единственный экземпляр состояния, который будет использоваться во всем приложении
app_state = AppState()
