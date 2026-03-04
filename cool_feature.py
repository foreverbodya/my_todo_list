import json
import datetime



class TodoItem():
    def __init__(self, name = "", status = False, description = "", date_start = None, date_end = None):
        self.name = name
        self.status = status
        self.description = description
        self.date_start = self._to_datetime(date_start)
        self.date_end = self._to_datetime(date_end)

    def _to_datetime(self, date_str_or_obj):

        # if isinstance(date_str_or_obj, str) and date_str_or_obj:
        #     try:
        #         for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        #             try:
        #                 return datetime.datetime.strptime(date_str_or_obj, fmt)
        #             except ValueError:
        #                 pass
        #         print(f"Предупреждение: Не удалось разобрать дату: {date_str_or_obj}. Возвращено None.")
        #         return None
        #     except Exception as e:
        #         print(f"Ошибка при преобразовании даты '{date_str_or_obj}': {e}")
        #         return None
        # elif isinstance(date_str_or_obj, datetime.datetime):
        #     return date_str_or_obj
        return None
    
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
        return f"[{self.name}"





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
            print('\nСписок задач пуст')
            return

        print("\nВаши текущие задачи")
        for i, task in enumerate(self.tasks):
            status_text = "Выполнена" if task.status else "Не выполнена"
            start_date_str = task.date_start.strftime("%Y-%m-%d %H:%M") if task.date_start else "Не указана"
            end_date_str = task.date_end.strftime("%Y-%m-%d %H:%M") if task.date_end else "Не указана"

            print(f"[{i + 1}] {task.name}")
            print(f"    Описание: {task.description if task.description else 'Нет описания'}")
            print(f"    Статус: {status_text}")
            print(f"    Начало: {start_date_str}")
            print(f"    Конец: {end_date_str} \n")
    
    # def _parse_date_input(self, date_str):
    #     if not date_str:
    #         return None
    #     for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
    #         try:
    #             return datetime.datetime.strptime(date_str, fmt)
    #         except ValueError:
    #             pass
    #     print(f"Некорректный формат даты '{date_str}'. Используйте гггг-мм-дд чч:мм или гггг-мм-дд.")
    #     return None

    def new_task(self):

        print('\nДобавление новой задачи')
        task_name = input('Имя задачи: ').strip()
        if not task_name:
            print("Имя задачи не может быть пустым. Отмена.")
            return

        task_description = input('Описание: ').strip()

        while True:
            status_input = input('Статус (выполнена/не выполнена): ').strip().lower()
            if status_input in ["выполнена", "да", "true"]:
                task_status = True
                break
            elif status_input in ["не выполнена", "нет", "false", ""]:
                task_status = False
                break
            else:
                print("Некорректный ввод. Пожалуйста, введите 'выполнена' или 'не выполнена'.")

        # task_date_start_str = input('Дата начала (гггг-мм-дд чч:мм, необязательно): ').strip()
        # task_date_start = self._parse_date_input(task_date_start_str)

        # task_date_end_str = input('Дата окончания (гггг-мм-дд чч:мм, необязательно): ').strip()
        # task_date_end = self._parse_date_input(task_date_end_str)

        # task = TodoItem(task_name, task_status, task_description, task_date_start, task_date_end)
        task = TodoItem(task_name, task_status, task_description)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Задача '{task.name}' успешно добавлена и сохранена.")

    def delete_task(self):
        self.list_tasks()

        try:
            task_index_to_delete = int(input('Введите номер задачи, которую хотите удалить: ')) - 1
            if 0 <= task_index_to_delete < len(self.tasks):
                selected_task = self.tasks[task_index_to_delete]
                print(f'Выбрана задача: {selected_task}')
                
                confirmation = input('Вы уверены, что хотите удалить эту задачу? (Да/Нет): ').lower()
                
                if confirmation in ["да", "конечно"]:
                    del self.tasks[task_index_to_delete]
                    self.save_tasks()
                    print(f'Задача "{selected_task.name}" успешно удалена f')
                else:
                    print('\nУдаление отменено ')
            else:
                print('Такой задачи под этим номером нет. Пожалуйста, введите корректный номер')

        except ValueError:
            print('Ошибка: Пожалуйста, введите числовой номер задачи')
        except Exception as e:
            print(f'Произошла неожиданная ошибка: {e}')
    def _get_task_index(self, prompt_message):
        while True:
            try:
                task_index = int(input(prompt_message)) - 1
                if 0 <= task_index < len(self.tasks):
                    return task_index
                else:
                    print('Такой задачи под этим номером нет. Пожалуйста, введите корректный номер.')
            except ValueError:
                print('Ошибка: Пожалуйста, введите числовой номер задачи')

    def edit_task(self):
        self.list_tasks()
        if not self.tasks:
            return

        task_index_to_edit = self._get_task_index('Введите номер задачи, которую хотите редактировать: ')
        if task_index_to_edit is None:
            return

        task = self.tasks[task_index_to_edit]
        print(f"\nРедактирование задачи: {task.name}")
        print("Оставьте поле пустым, чтобы не изменять его")

        new_name = input(f"Новое имя (текущее: {task.name}): ").strip()
        if new_name:
            task.name = new_name

        new_description = input(f"Новое описание (текущее: {task.description if task.description else 'Нет описания'}): ").strip()
        if new_description:
            task.description = new_description

        while True:
            status_current = "выполнена" if task.status else "не выполнена"
            status_input = input(f"Новый статус (выполнена/не выполнена, текущий: {status_current}): ").strip().lower()
            if status_input == "выполнена":
                task.status = True
                break
            elif status_input == "не выполнена":
                task.status = False
                break
            elif not status_input: 
                break
            else:
                print("Некорректный ввод. Пожалуйста, введите 'выполнена' или 'не выполнена'.")

        # start_date_current = task.date_start.strftime("%Y-%m-%d %H:%M") if task.date_start else "Не указана"
        # new_start_date_str = input(f"Новая дата начала (гггг-мм-дд чч:мм, текущая: {start_date_current}): ").strip()
        # if new_start_date_str:
        #     parsed_date = self._parse_date_input(new_start_date_str)
        #     if parsed_date:
        #         task.date_start = parsed_date

        # end_date_current = task.date_end.strftime("%Y-%m-%d %H:%M") if task.date_end else "Не указана"
        # new_end_date_str = input(f"Новая дата окончания (гггг-мм-дд чч:мм, текущая: {end_date_current}): ").strip()
        # if new_end_date_str:
        #     parsed_date = self._parse_date_input(new_end_date_str)
        #     if parsed_date:
        #         task.date_end = parsed_date

        self.save_tasks()
        print(f"Задача '{task.name}' успешно обновлена.")


def todo_brains():
    todo_list = TodoList("load_file.json")
    print(f"\nЗагружено задач: {len(todo_list)}.")

    while True:
        print("\n   Меню To-Do списка    \n")
        print("1. Показать все задачи")
        print("2. Добавить новую задачу")
        print("3. Удалить задачу")
        print("4. Редактировать задачу")
        print("5. Изменить статус задачи (выполнена/не выполнена)")
        print("6. Выйти")

        choice = input('Че выбираешь, братишка? Введи номер: ').strip()

        if choice == '1':
            todo_list.list_tasks()
        elif choice == '2':
            todo_list.new_task()
        elif choice == '3':
            todo_list.delete_task()
        elif choice == '4':
            todo_list.edit_task()
        elif choice == '5':
            todo_list.toggle_task_status()
        elif choice == '6':
            print("До встречи, братишка! Задачи сохранены.")
            break
        else:
            print("Некорректный выбор. Пожалуйста, введите число от 1 до 6.")

if __name__ == "__main__":
    todo_brains()




# def todo_brains():
#     i = input('Че выбираешь братишка: ')

# todo_list = TodoList("load_file.json")


# print(f"\nЗагружено задач: {len(todo_list)} \n")


# for i,task in enumerate(todo_list.tasks):
#     print(f"Задача: {i+1} {task.name}")
#     print(f"Описание: {task.description}")
#     print(f"Статус: {task.status} \n")

# todo_list.save_tasks()


# Надо обернуть соусом логики
# new_task = TodoItem("Изучить ООП", status = None)
# todo_list.tasks.append(new_task)


# ======================
#  Призыв новой таски и
#   сохранение списка:
#  todo_list.new_task()
# ======================\



# Novii_task = TodoItem("Новая таска",status=False,description="Новая таска", date_start="04.03.2026" , date_end="04.03.2027")
