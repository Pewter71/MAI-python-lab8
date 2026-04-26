"""
Тесты для класса GeneratorSource
"""
import random
from src.sources.generator_source import GeneratorSource
from src.contracts.task_source import TaskSource


def test_generator_source_protocol():
    """Тест того, что GeneratorSource реализует протокол TaskSource"""
    source = GeneratorSource(count=5)
    assert isinstance(source, TaskSource)


def test_generator_source_count():
    """Тест того, что генератор возвращает ровно count задач"""
    source = GeneratorSource(count=10)
    tasks = source.get_tasks()
    assert len(tasks) == 10


def test_generator_source_zero_count():
    """Тест генератора с нулевым количеством задач"""
    source = GeneratorSource(count=0)
    tasks = source.get_tasks()
    assert tasks == []


def test_generator_source_deterministic_with_seed():
    """Тест детерминированной генерации при фиксированном seed"""
    random.seed(1)
    tasks = GeneratorSource(count=3).get_tasks()

    assert len(tasks) == 3
    assert tasks[0].payload == "something wrong"
    assert tasks[1].payload == "look at me"
    assert tasks[2].payload == "tri tak tri"
