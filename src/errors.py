"""
Пользовательские исключения
"""


class TaskValidationError(ValueError):
    """Нарушение инварианта задачи"""


class TaskSourceError(Exception):
    """Базовое исключение источников задач"""


class InvalidTaskSourceError(TaskSourceError):
    """Объект не реализует протокол TaskSource"""

    def __init__(self) -> None:
        super().__init__("источник не реализует контракт TaskSource")


class TaskFileNotFoundError(TaskSourceError):
    """Файл источника задач не найден"""

    def __init__(self) -> None:
        super().__init__("файл не найден")


class InvalidTaskFormatError(TaskSourceError):
    """Данные из источника имеют некорректный формат"""

    def __init__(self) -> None:
        super().__init__("некорректный формат данных")


class MissingTaskFieldError(TaskSourceError):
    """В строке отсутствует обязательное поле"""

    def __init__(self) -> None:
        super().__init__("в JSONL строке отсутствует обязательное поле")
