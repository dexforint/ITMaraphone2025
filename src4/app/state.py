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