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





class TodoList:
    def __init__(self, load_file = "" ):
        self.load_file = load_file
        self.tasks = None
        self.load_tasks()

    def __len__(self):
        return len(self.tasks) if self.tasks != None else 0

    def load_tasks(self):

        try:
            with open(self.load_file, 'r', encoding='utf-8') as f:
                list_of_dicts = json.load(f)
            self.tasks = [TodoItem.from_dict(d) for d in list_of_dicts]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

        return self.tasks    

    def save_tasks(self):
        with open(self.load_file, 'w', encoding='utf-8') as f:
            json.dump([item.to_dict() for item in self.tasks], f, ensure_ascii=False, indent=4)  


# load_tasks()

todo_list = TodoList("load_file.json")


print(f"\nЗагружено задач: {len(todo_list)} \n")


for i,task in enumerate(todo_list.tasks):
    print(f"Задача: {i+1} {task.name}")
    print(f"Описание: {task.description}")
    print(f"Статус: {task.status} \n")


todo_list.save_tasks()