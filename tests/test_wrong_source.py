"""
Тесты для класса WrongSource
"""
from src.sources.wrong_source import WrongSource
from src.contracts.task_source import TaskSource


def test_wrong_source_create():
    """Тест создания некорректного источника"""
    source = WrongSource()
    assert source is not None


def test_wrong_source_protocol():
    """Тест того, что WrongSource не удовлетворяет протоколу TaskSource"""
    source = WrongSource()
    assert not isinstance(source, TaskSource)