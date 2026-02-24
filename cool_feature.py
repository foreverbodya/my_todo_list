import json
import datetime



class TodoItem():
    def __init__(self, name = "", status = None, description = "", date_start = None, date_end = None):
        self.name = name
        self.status = status
        self.description = description
        self.date_start = date_start
        self.date_end = date_end

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return TodoItem(
            name=data.get("name"),
            status=data.get("status"),
            description=data.get("description"),
            date_start=data.get("date_start"),
            date_end=data.get("date_end")
        )
    def __repr__(self):
        status_icon = "✓" if self.status else "✗"
        return f"[{status_icon}] {self.name}"






def load_tasks(load_file):
    with open(load_file, 'r', encoding='utf-8') as f:
        list_of_dicts = json.load(f)
    task_as_objects = [TodoItem.from_dict(d) for d in list_of_dicts]
    return task_as_objects

# load_tasks()

print("Загружаем задачи из файла...")
my_tasks = load_tasks("load_file.json")

if my_tasks:
    print(f"Загружено задач: {len(my_tasks)}")

    first_task = my_tasks[0]

    print(f"Первая таска: {first_task}")
    print(f"Название: {first_task.name}")
    print(f"Статус: {first_task.status}")
else:
    print("Не удалось загрузить задачи или файл пуст.")