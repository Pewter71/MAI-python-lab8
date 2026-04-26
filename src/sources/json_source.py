import json
from dataclasses import dataclass
from pathlib import Path
from src.contracts.task import Task
from src.errors import TaskFileNotFoundError, InvalidTaskFormatError, MissingTaskFieldError
from datetime import datetime

@dataclass
class JsonSource:
    """Источник задач из JSONL файла"""
    path: str | Path
    def get_tasks(self) -> list[Task]:
        path = Path(self.path)
        if not path.exists():
            raise TaskFileNotFoundError()
        raw = path.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        records = self._jsonl_parse(raw)
        tasks = []
        for i, record in enumerate(records, start=1):
            task = self._convert_to_task(record)
            tasks.append(task)
        return tasks

    def _jsonl_parse(self, raw: str) -> list[dict[str, str]]:
        records = []
        for line_no, line in enumerate(raw.splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                raise InvalidTaskFormatError()
        return records

    def _convert_to_task(self, record: dict[str, str]) -> Task:
        if "id" not in record:
            raise MissingTaskFieldError()
        if "payload" not in record:
            raise MissingTaskFieldError()
        try:
            id_int = int(record["id"])
        except ValueError:
            raise InvalidTaskFormatError()
        try:
            if "priority" in record:
                priority = int(record["priority"])
            else:
                priority = 3
        except ValueError:
            raise InvalidTaskFormatError()
        if "status" in record:
            status = str(record["status"])
        else:
            status = "pending"
        created_at = None
        if "created_at" in record:
            try:
                created_at = datetime.fromisoformat(str(record["created_at"]))
            except ValueError:
                raise InvalidTaskFormatError()
        return Task(id=id_int, payload=str(record["payload"]), priority=priority, status=status, created_at=created_at)
