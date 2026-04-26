from dataclasses import dataclass
from src.contracts.task import Task

@dataclass
class WrongSource:
    """Некорректный источник задач для тестов"""
    def get_task(self) -> list[Task]:
        task = Task(id=999, payload="wrong_protocol_task")
        return [task]