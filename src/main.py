"""
CLI и получение задач из разных источников
"""
from src.sources.wrong_source import WrongSource
from src.sources.generator_source import GeneratorSource
from src.sources.json_source import JsonSource
from src.receiver import receive_tasks
from src.task_queue import TaskQueue

def main():
    while True:
        print("\nВыберите источник задач:")
        print("1. Файл JSONL")
        print("2. Генератор")
        print("3. Неправильный источник")
        print("4. Демонстрация очереди задач")
        print("0. Выход")
        
        choice = input("Введите номер источника: ").strip()
        if choice == "1":
            source = JsonSource(path="file_sources/jsonl_source.jsonl")
        elif choice == "2":
            source = GeneratorSource(count=5)
        elif choice == "3":
            source = WrongSource()
        elif choice == "4":
            source = GeneratorSource(count=8)
            tasks = receive_tasks(source)
            queue = TaskQueue(tasks)
            print(f"\n{queue}")
            print("for:")
            for task in queue:
                print(f"id: {task.id}, payload: {task.payload}, priority: {task.priority}, status: {task.status}")
            print("Фильтр по статусу pending:")
            for task in queue.filter_by_status("pending"):
                print(f"id: {task.id}, payload: {task.payload}, priority: {task.priority}, status: {task.status}")
            print("Фильтр по приоритету >= 4:")
            for task in queue.filter_by_priority(4):
                print(f"id: {task.id}, payload: {task.payload}, priority: {task.priority}, status: {task.status}")
            print(f"Сумма приоритетов: {sum(t.priority for t in queue.stream())}")
            continue
        elif choice == "0":
            print("Выход из программы")
            break
        else:
            print("Введите число из списка!")
            continue
        try:
            tasks = receive_tasks(source)
            print(f"Получено {len(tasks)} задач:")
            for task in tasks:
                print(f"id: {task.id}, payload: {task.payload}, priority: {task.priority}, status: {task.status}, created_at: {task.created_at}, is_ready: {task.is_ready}")
                print(f"summary: {task.summary}")
        except Exception as e:
            print(f"Ошибка при получении задач: {e}")


if __name__ == "__main__":
    main()