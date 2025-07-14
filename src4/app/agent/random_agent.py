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