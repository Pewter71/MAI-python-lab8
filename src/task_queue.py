"""
Класс очереди задач
"""
from typing import Generator
from src.contracts.task import Task
from src.errors import TaskValidationError


class _TaskQueueIterator:
    """Итератор для TaskQueue"""
    def __init__(self, tasks: list[Task]) -> None:
        self._tasks = tasks
        self._index = 0

    def __iter__(self) -> "_TaskQueueIterator":
        return self

    def __next__(self) -> Task:
        if self._index >= len(self._tasks):
            raise StopIteration
        task = self._tasks[self._index]
        self._index += 1
        return task


class TaskQueue:
    """Очередь задач"""
    def __init__(self, tasks: list[Task] | None = None) -> None:
        if tasks is not None:
            self._tasks: list[Task] = list(tasks)
        else:
            self._tasks: list[Task] = []

    def add(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TaskValidationError("можно добавлять только объекты Task")
        self._tasks.append(task)

    def __iter__(self) -> _TaskQueueIterator:
        return _TaskQueueIterator(self._tasks)

    def __len__(self) -> int:
        return len(self._tasks)

    def __repr__(self) -> str:
        return f"TaskQueue(size={len(self._tasks)})"

    def filter_by_status(self, status: str) -> Generator[Task, None, None]:
        """Ленивая фильтрация задач по статусу"""
        for task in self._tasks:
            if task.status == status:
                yield task

    def filter_by_priority(self, min_priority: int) -> Generator[Task, None, None]:
        """Ленивая фильтрация задач по минимальному приоритету"""
        for task in self._tasks:
            if task.priority >= min_priority:
                yield task

    def stream(self) -> Generator[Task, None, None]:
        """Потоковая обработка задач"""
        yield from self._tasks
