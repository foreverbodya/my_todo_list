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

    def list_tasks(self):
            if not self.tasks:
                print('Список задач пуст')
                return

            print("\n--- Ваши текущие задачи ---")
            for i, task in enumerate(self.tasks):
                print(f"[{i+1}] {task}")
            print("--------------------------")

    def new_task(self):
        task_name = input('Новая задача\nИмя: ')
        task_status = input('Статус: ')
        task_description =  input('Описание: ')
        
        task = TodoItem(task_name,task_status,task_description)
        self.tasks.append(task)
        self.save_tasks() 
        
        print(f"Задача '{task.name}' успешно добавлена и сохранена.")

    def delete_task(self):
        self.list_tasks()

        try:
            task_index_to_delete = int(input('Введите номер задачи, которую хотите удалить: ')) - 1
            
            # Проверяем, что введенный индекс существует
            if 0 <= task_index_to_delete < len(self.tasks):
                selected_task = self.tasks[task_index_to_delete]
                print(f'Выбрана задача: {selected_task}')
                
                confirmation = input('Вы уверены, что хотите удалить эту задачу? (Да/Нет): ').lower()
                
                if confirmation in ["да", "конечно"]:
                    del self.tasks[task_index_to_delete] # Удаляем задачу из списка
                    self.save_tasks()
                    print(f'Задача "{selected_task.name}" успешно удаленf')
                else:
                    print('\nУдаление отменено.')
            else:
                print('Такой задачи под этим номером нет. Пожалуйста, введите корректный номер')

        except ValueError:
            print('Ошибка: Пожалуйста, введите числовой номер задачи')
        except Exception as e:
            print(f'Произошла неожиданная ошибка: {e}')

def todo_brains(i):
    i = input('Че выбираешь братишка: ')

todo_list = TodoList("load_file.json")

todo_list.delete_task()

print(f"\nЗагружено задач: {len(todo_list)} \n")


for i,task in enumerate(todo_list.tasks):
    print(f"Задача: {i+1} {task.name}")
    print(f"Описание: {task.description}")
    print(f"Статус: {task.status} \n")

todo_list.save_tasks()


# Надо обернуть соусом логики
# new_task = TodoItem("Изучить ООП", status = None)
# todo_list.tasks.append(new_task)


# ======================
#  Призыв новой таски и
#   сохранение списка:
#  todo_list.new_task()
# ======================