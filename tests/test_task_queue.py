"""
Тесты для класса TaskQueue
"""
import pytest
import types
from src.contracts.task import Task
from src.errors import TaskValidationError
from src.task_queue import TaskQueue


def _make_task(id: int, payload: str = "test", priority: int = 3, status: str = "pending") -> Task:
    return Task(id=id, payload=payload, priority=priority, status=status)


def test_task_queue_empty():
    """Тест создания пустой очереди"""
    queue = TaskQueue()
    assert len(queue) == 0


def test_task_queue_from_list():
    """Тест создания очереди из списка задач"""
    tasks = [_make_task(1), _make_task(2)]
    queue = TaskQueue(tasks)
    assert len(queue) == 2


def test_task_queue_add():
    """Тест добавления задачи в очередь"""
    queue = TaskQueue()
    queue.add(_make_task(1))
    assert len(queue) == 1


def test_task_queue_add_invalid():
    """Тест добавления не Task в очередь"""
    queue = TaskQueue()
    with pytest.raises(TaskValidationError):
        queue.add("not a task")


def test_task_queue_iter_for():
    """Тест обхода очереди через for"""
    tasks = [_make_task(i) for i in range(5)]
    queue = TaskQueue(tasks)
    result = [task.id for task in queue]
    assert result == [0, 1, 2, 3, 4]


def test_task_queue_iter_list():
    """Тест совместимости с list()"""
    tasks = [_make_task(1), _make_task(2)]
    queue = TaskQueue(tasks)
    assert list(queue) == tasks


def test_task_queue_iter_repeatable():
    """Тест повторного обхода очереди"""
    tasks = [_make_task(1), _make_task(2)]
    queue = TaskQueue(tasks)
    first = list(queue)
    second = list(queue)
    assert first == second


def test_task_queue_stop_iteration():
    """Тест корректного завершения итерации"""
    queue = TaskQueue([_make_task(1)])
    it = iter(queue)
    next(it)
    with pytest.raises(StopIteration):
        next(it)


def test_task_queue_filter_by_status():
    """Тест фильтрации по статусу"""
    tasks = [
        _make_task(1, status="pending"),
        _make_task(2, status="done"),
        _make_task(3, status="pending"),
    ]
    queue = TaskQueue(tasks)
    result = list(queue.filter_by_status("pending"))
    assert len(result) == 2
    assert all(t.status == "pending" for t in result)


def test_task_queue_filter_by_status_empty():
    """Тест фильтрации по статусу без совпадений"""
    queue = TaskQueue([_make_task(1, status="done")])
    result = list(queue.filter_by_status("in_progress"))
    assert result == []


def test_task_queue_filter_by_priority():
    """Тест фильтрации по приоритету"""
    tasks = [
        _make_task(1, priority=1),
        _make_task(2, priority=3),
        _make_task(3, priority=5),
    ]
    queue = TaskQueue(tasks)
    result = list(queue.filter_by_priority(3))
    assert len(result) == 2
    assert all(t.priority >= 3 for t in result)


def test_task_queue_filter_is_generator():
    """Тест того, что фильтры возвращают генераторы"""
    queue = TaskQueue([_make_task(1)])
    assert isinstance(queue.filter_by_status("pending"), types.GeneratorType)
    assert isinstance(queue.filter_by_priority(1), types.GeneratorType)


def test_task_queue_stream_is_generator():
    """Тест того, что stream() возвращает генератор"""
    queue = TaskQueue([_make_task(1)])
    assert isinstance(queue.stream(), types.GeneratorType)


def test_task_queue_stream_yields_all():
    """Тест потоковой обработки всех задач"""
    tasks = [_make_task(i) for i in range(10)]
    queue = TaskQueue(tasks)
    result = list(queue.stream())
    assert result == tasks


def test_task_queue_sum_priority():
    """Тест совместимости с sum()"""
    tasks = [_make_task(i, priority=i + 1) for i in range(5)]
    queue = TaskQueue(tasks)
    total = sum(task.priority for task in queue)
    assert total == 1 + 2 + 3 + 4 + 5


def test_task_queue_large_amount():
    """Тест работы с большим объёмом задач"""
    tasks = [_make_task(i, priority=(i % 5) + 1) for i in range(10000)]
    queue = TaskQueue(tasks)
    high_priority = list(queue.filter_by_priority(5))
    assert len(high_priority) == 2000


def test_task_queue_repr():
    """Тест строкового представления очереди"""
    queue = TaskQueue([_make_task(1), _make_task(2)])
    assert repr(queue) == "TaskQueue(size=2)"


def test_task_queue_not_editable():
    """Тест того, что изменение исходного списка не влияет на очередь"""
    tasks = [_make_task(1)]
    queue = TaskQueue(tasks)
    tasks.append(_make_task(2))
    assert len(queue) == 1
