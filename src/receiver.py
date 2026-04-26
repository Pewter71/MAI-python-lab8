"""
Получение задач из источников
"""
from src.contracts.task import Task
from src.contracts.task_source import TaskSource
from src.errors import InvalidTaskSourceError


def receive_tasks(task_source: TaskSource) -> list[Task]:
    if not isinstance(task_source, TaskSource):
        raise InvalidTaskSourceError()
    return task_source.get_tasks()
    

