from typing import runtime_checkable, Protocol
from src.contracts.task import Task


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> list[Task]:
        ...