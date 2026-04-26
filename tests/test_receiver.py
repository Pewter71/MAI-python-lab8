"""
Тесты для функции receive_tasks
"""
import pytest
from src.receiver import receive_tasks
from src.sources.generator_source import GeneratorSource
from src.sources.json_source import JsonSource
from src.sources.wrong_source import WrongSource
from src.errors import InvalidTaskSourceError


def test_receive_tasks_from_generator():
    """Тест получения задач от генератора"""
    source = GeneratorSource(count=5)
    tasks = receive_tasks(source)
    assert len(tasks) == 5



def test_receive_tasks_from_json_source(tmp_path):
    """Тест получения задач из JSONL источника"""
    path = tmp_path / "tasks.jsonl"
    path.write_text(
        '{"id": "1", "payload": "a"}\n{"id": "2", "payload": "b"}\n',
        encoding="utf-8",
    )
    tasks = receive_tasks(JsonSource(path=str(path)))
    assert len(tasks) == 2
    assert tasks[0].payload == "a"
    assert tasks[1].payload == "b"


def test_receive_tasks_from_wrong_source():
    """Тест получения задач от некорректного источника"""
    with pytest.raises(InvalidTaskSourceError):
        receive_tasks(WrongSource())


def test_receive_tasks_from_non_source_object():
    """Тест передачи объекта, не являющегося источником задач"""
    with pytest.raises(InvalidTaskSourceError):
        receive_tasks("not a source")



def test_receive_tasks_from_int():
    """Тест передачи числа вместо источника"""
    with pytest.raises(InvalidTaskSourceError):
        receive_tasks(42)


def test_receive_tasks_empty_generator():
    """Тест получения задач от пустого генератора"""
    tasks = receive_tasks(GeneratorSource(count=0))
    assert tasks == []