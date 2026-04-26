"""
Классы задачи и дескрипторов
"""
from datetime import datetime

from src.errors import TaskValidationError


class _PriorityDescriptor:
    """Data descriptor для валидации приоритета"""

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr = f"_{name}"

    def __get__(self, obj: object, objtype: type | None = None) -> "int | _PriorityDescriptor":
        if obj is None:
            return self
        return getattr(obj, self._attr)

    def __set__(self, obj: object, value: int) -> None:
        if not isinstance(value, int):
            raise TaskValidationError("priority должен быть int")
        if not (0 < value < 6):
            raise TaskValidationError("priority должен быть в диапазоне от 1 до 5")
        setattr(obj, self._attr, value)


class _StatusDescriptor:
    """Data descriptor для валидации статуса задачи"""

    _VALID: set[str] = {"pending", "in_progress", "done"}

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr = f"_{name}"

    def __get__(self, obj: object, objtype: type | None = None) -> "str | _StatusDescriptor":
        if obj is None:
            return self
        return getattr(obj, self._attr)

    def __set__(self, obj: object, value: str) -> None:
        if not isinstance(value, str):
            raise TaskValidationError("status должен быть str")
        if value not in self._VALID:
            raise TaskValidationError("недопустимый статус")
        setattr(obj, self._attr, value)


class _SummaryDescriptor:
    """Non-data descriptor для краткого описания задачи"""

    def __get__(self, obj: object, objtype: type | None = None) -> "str | _SummaryDescriptor":
        if obj is None:
            return self
        return f"[P{obj.priority}] {obj.payload[:30]}" 


class Task:
    """Класс задачи"""

    priority: int = _PriorityDescriptor()
    status: str = _StatusDescriptor()
    summary: str = _SummaryDescriptor()

    def __init__(
        self,
        id: int,
        payload: str,
        priority: int = 3,
        status: str = "pending",
        created_at: datetime | None = None,
    ) -> None:
        if not isinstance(id, int):
            raise TaskValidationError("id должен быть int")
        if not isinstance(payload, str):
            raise TaskValidationError("payload должен быть str")
        if not payload:
            raise TaskValidationError("payload не должен быть пустым")
        self._id: int = id
        self._payload: str = payload
        self.priority = priority
        self.status = status
        if created_at is not None:
            self._created_at: datetime = created_at
        else:
            self._created_at: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self._id

    @property
    def payload(self) -> str:
        return self._payload

    @payload.setter
    def payload(self, value: str) -> None:
        if not isinstance(value, str):
            raise TaskValidationError("payload должен быть str")
        if not value:
            raise TaskValidationError("payload не должен быть пустым")
        self._payload = value

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def is_ready(self) -> bool:
        return self.status == "pending" and self.priority > 2

    def __repr__(self) -> str:
        return (
            f"Task(id={self._id!r}, payload={self._payload!r}, "
            f"priority={self.priority!r}, status={self.status!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return self._id == other._id and self._payload == other._payload
