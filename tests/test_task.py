"""
Тесты для Task
"""
import pytest
from datetime import datetime
from src.contracts.task import Task
from src.errors import TaskValidationError


def test_task_default_creation():
    """Тест создания задачи с параметрами по умолчанию"""
    task = Task(id=1, payload="do something")
    assert task.id == 1
    assert task.payload == "do something"
    assert task.priority == 3
    assert task.status == "pending"


def test_task_full_creation():
    """Тест создания задачи со всеми параметрами"""
    task = Task(id=7, payload="critical fix", priority=5, status="in_progress")
    assert task.id == 7
    assert task.payload == "critical fix"
    assert task.priority == 5
    assert task.status == "in_progress"


def test_priority_descriptor_valid_range():
    """Тест дескриптора priority c граничными значениями"""
    task = Task(id=1, payload="x")
    for p in (1, 2, 3, 4, 5):
        task.priority = p
        assert task.priority == p


def test_priority_descriptor_too_low():
    """Тест дескриптора priority со значением ниже допустимого"""
    with pytest.raises(TaskValidationError):
        Task(id=1, payload="x", priority=0)


def test_priority_descriptor_too_high():
    """Тест дескриптора priority со значением выше допустимого"""
    with pytest.raises(TaskValidationError):
        Task(id=1, payload="x", priority=6)


def test_priority_descriptor_wrong_type():
    """Тест дескриптора priority с неверным типом"""
    with pytest.raises(TaskValidationError):
        Task(id=1, payload="x", priority="high")


def test_status_descriptor_invalid_value():
    """Тест дескриптора status с недопустимым значением"""
    with pytest.raises(TaskValidationError):
        Task(id=1, payload="x", status="cancelled")


def test_status_descriptor_wrong_type():
    """Тест дескриптора status с неверным типом"""
    with pytest.raises(TaskValidationError):
        Task(id=1, payload="x", status=42)


def test_id_is_readonly():
    """Тест того, что id нельзя изменить после создания"""
    task = Task(id=1, payload="x")
    with pytest.raises(AttributeError):
        task.id = 2 


def test_created_at_is_readonly():
    """Тест того, что created_at нельзя изменить"""
    task = Task(id=1, payload="x")
    with pytest.raises(AttributeError):
        task.created_at = datetime.now() 


def test_created_at_is_datetime():
    """Тест того, что created_at является datetime"""
    task = Task(id=1, payload="x")
    assert isinstance(task.created_at, datetime)


def test_payload_setter_valid():
    """Тест сеттера payload с корректным значением"""
    task = Task(id=1, payload="old")
    task.payload = "new"
    assert task.payload == "new"


def test_payload_setter_empty():
    """Тест сеттера payload с пустой строкой"""
    task = Task(id=1, payload="x")
    with pytest.raises(TaskValidationError):
        task.payload = ""


def test_payload_setter_wrong_type():
    """Тест сеттера payload с неверным типом"""
    task = Task(id=1, payload="x")
    with pytest.raises(TaskValidationError):
        task.payload = 123



def test_is_ready_false_wrong_status():
    """Тест is_ready статус не pending"""
    task = Task(id=1, payload="x", priority=5, status="done")
    assert task.is_ready is False


def test_summary_non_data_descriptor():
    """Тест дескриптора summary"""
    task = Task(id=1, payload="fix bug", priority=4)
    assert task.summary == "[P4] fix bug"


def test_summary_can_be_overridden():
    """Тест перекрытия дескриптора summary"""
    task = Task(id=1, payload="fix bug", priority=4)
    task.__dict__["summary"] = "custom label"
    assert task.summary == "custom label"


def test_task_invalid_id_type():
    """Тест создания задачи с неверным типом id"""
    with pytest.raises(TaskValidationError):
        Task(id="one", payload="x")


def test_task_empty_payload():
    """Тест создания задачи с пустым payload"""
    with pytest.raises(TaskValidationError):
        Task(id=1, payload="")


def test_task_repr():
    """Тест строкового представления задачи"""
    task = Task(id=1, payload="hello", priority=2, status="done")
    assert repr(task) == "Task(id=1, payload='hello', priority=2, status='done')"


def test_task_equality():
    """Тест равенства задач по id и payload"""
    t1 = Task(id=1, payload="x", priority=1, status="pending")
    t2 = Task(id=1, payload="x", priority=5, status="done")
    assert t1 == t2


def test_task_inequality():
    """Тест неравенства задач"""
    t1 = Task(id=1, payload="x")
    t2 = Task(id=2, payload="x")
    assert t1 != t2
