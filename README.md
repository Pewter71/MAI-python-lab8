# Лабораторная работа 3

## Тема: Очередь задач (итераторы и генераторы)

* **Цель:** реализовать очередь задач `TaskQueue`, поддерживающую протокол итерации, ленивую фильтрацию и потоковую обработку задач, а также набор источников задач, удовлетворяющих протоколу `TaskSource`.
* **Вариант:** итераторы и генераторы - реализация пользовательского итератора, ленивых фильтров по статусу и приоритету, потоковой обработки через генераторы, дескрипторов данных для валидации полей `Task`, `Protocol`-интерфейса для источников задач.
* **Используемые библиотеки:** `dataclasses`, `datetime`, `json`, `pathlib`, `random`, `typing`, стандартная библиотека Python.

## Ограничения и допущения

- Приоритет задачи `priority` - целое число от 1 до 5 включительно; значения вне диапазона или неверного типа вызывают `TaskValidationError`.
- Статус задачи `status` - строка, допустимые значения: `pending`, `in_progress`, `done`; любое другое значение вызывает `TaskValidationError`.
- Поле `id` и `created_at` доступны только для чтения.
- `payload` не может быть пустой строкой; попытка установить пустое значение вызывает `TaskValidationError`.
- `TaskQueue` при создании копирует переданный список, чтобы последующие изменения исходного списка не влияли на очередь.
- `WrongSource` намеренно не реализует метод `get_tasks()` (реализует `get_task()`) и не удовлетворяет протоколу `TaskSource`.
- JSONL-источник обрабатывает файл построчно; пустые строки пропускаются; некорректный JSON вызывает `InvalidTaskFormatError`.
- Поля `priority`, `status` и `created_at` в JSONL-строке необязательны и имеют значения по умолчанию.

## Реализованный функционал

Выполнено:
- Класс `Task` с дескрипторами
- Протокол `TaskSource`
- Источники задач: `JsonSource`, `GeneratorSource`, `WrongSource`
- Функция `receive_tasks`
- Класс `TaskQueue` с итератором, генераторами-фильтрами и потоковой обработкой
- Интерактивное CLI-меню
- Полный набор тестов


### Класс TaskQueue

Очередь задач, совместимая со стандартными конструкциями Python (`for`, `list`, `sum`).

- `__iter__` - возвращает пользовательский итератор `_TaskQueueIterator`, поддерживающий повторный обход.
- `__len__` - количество задач в очереди.
- `__repr__` - строковое представление вида `TaskQueue(size=N)`.
- `add(task)` - добавляет задачу; принимает только объекты `Task`, иначе `TaskValidationError`.
- `filter_by_status(status)` - ленивая фильтрация задач по статусу.
- `filter_by_priority(min_priority)` - ленивая фильтрация задач по приоритету.
- `stream()` - потоковая выдача всех задач по одной.

### Пользовательские исключения

Все исключения определены в `src/errors.py`:

- `TaskValidationError(ValueError)` - нарушение инварианта полей `Task`.
- `TaskSourceError(Exception)` - базовый класс для исключений источников.
- `InvalidTaskSourceError(TaskSourceError)` - объект не реализует `TaskSource`.
- `TaskFileNotFoundError(TaskSourceError)` - файл JSONL не найден.
- `InvalidTaskFormatError(TaskSourceError)` - некорректный формат данных в файле.
- `MissingTaskFieldError(TaskSourceError)` - отсутствует обязательное поле (`id` или `payload`).

## Алгоритм работы программы

1. При запуске `main()` выводится интерактивное меню с выбором источника задач.
2. В зависимости от выбора создаётся экземпляр `JsonSource`, `GeneratorSource` или `WrongSource`.
3. Вызывается `receive_tasks(source)`, который проверяет протокол и возвращает список задач.
4. Полученные задачи выводятся с полями `id`, `payload`, `priority`, `status`, `created_at`, `is_ready`, `summary`.
5. При выборе режима «Демонстрация очереди задач» создаётся `TaskQueue`, демонстрируются обход `for`, фильтры по статусу и приоритету, а также подсчёт суммы приоритетов через `sum()`.
6. Цикл продолжается до выбора пункта `0`.


## Установка и запуск

```bash
git clone https://github.com/Pewter71/MAI-python-lab8
cd MAI-python-lab8
```

Установка зависимостей:

```bash
uv sync
source .venv/bin/activate
```

Запуск интерактивного меню:

```bash
python -m src.main
```

Запуск тестов:

```bash
pytest -q
```

## Структура проекта

```
├── file_sources/
│   └── jsonl_source.jsonl          # Пример JSONL-файла с задачами
├── src/
│   ├── main.py                     # Интерактивное CLI-меню
│   ├── receiver.py                 # Функция receive_tasks
│   ├── task_queue.py               # Класс TaskQueue
│   ├── errors.py                   # Пользовательские исключения
│   ├── contracts/
│   │   ├── task.py                 # Класс Task и дескрипторы
│   │   └── task_source.py          # Протокол TaskSource
│   └── sources/
│       ├── json_source.py          # Источник из JSONL-файла
│       ├── generator_source.py     # Генератор случайных задач
│       └── wrong_source.py         # Некорректный источник для тестов
├── tests/
│   ├── test_task.py
│   ├── test_task_queue.py
│   ├── test_json_source.py
│   ├── test_generator_source.py
│   ├── test_wrong_source.py
│   ├── test_receiver.py
│   └── test_main.py
└── README.md
```
