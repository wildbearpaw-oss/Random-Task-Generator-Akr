import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "tasks_data.json"

# Список задач
tasks = []

# Функция сохранения данных в JSON
def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Успех", "Данные сохранены в файл!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные:\n{e}")


# Функция загрузки данных из JSON
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                tasks.extend(data)
                update_task_list()
            if data:
                messagebox.showinfo("Успех", f"Загружено {len(data)} задач!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные:\n{e}")
    else:
        messagebox.showinfo("Информация", "Файл с задачами не найден. Начните добавлять задачи!")

# Функция добавления задачи
def add_task():
    text = entry_text.get().strip()
    task_type = type_var.get()

    # Проверка пустых полей
    if not text:
        messagebox.showwarning("Внимание", "Текст задачи не может быть пустым!")
        return

    if task_type == "Выберите тип":
        messagebox.showwarning("Внимание", "Выберите тип задачи!")
        return

    # Добавление задачи в список
    task = {"text": text, "type": task_type}
    tasks.append(task)

    # Обновление списка на экране
    update_task_list()

    # Очистка полей
    entry_text.delete(0, tk.END)
    combo_type.current(0)

    messagebox.showinfo("Успех", f"Задача '{text}' добавлена!")

# Функция обновления списка задач
def update_task_list(task_list=None):
    task_listbox.delete(0, tk.END)
    if task_list is None:
        task_list = tasks
    for i, task in enumerate(task_list, 1):
        entry = f"{i}. {task['text']} ({task['type']})"
        task_listbox.insert(tk.END, entry)

# Функция генерации случайной задачи
def generate_random_task():
    if not tasks:
        messagebox.showwarning("Внимание", "Нет задач! Сначала добавьте задачи.")
        random_task_label.config(text="Нет задач для отображения", fg="orange")
        return

    import random
    random_task = random.choice(tasks)
    random_task_label.config(
        text=f"Случайная задача: {random_task['text']}\nТип: {random_task['type']}",
        fg="black"
    )

# Функция фильтрации
def apply_filter():
    type_filter = type_filter_var.get()

    filtered_tasks = tasks[:]

    # Фильтр по типу задачи
    if type_filter != "Все":
        filtered_tasks = [t for t in filtered_tasks if t['type'] == type_filter]

    update_task_list(filtered_tasks)

# Функция сброса фильтров
def reset_filter():
    combo_type_filter.current(0)
    update_task_list()

# Функция удаления задачи
def delete_task():
    selection = task_listbox.curselection()
    if not selection:
        messagebox.showwarning("Внимание", "Выберите задачу для удаления!")
        return

    index = selection[0]
    # Определяем, какой список используется (отфильтрованный или обычный)
    type_filter = type_filter_var.get()

    if type_filter != "Все":
        # При фильтрации нужно найти задачу в основном списке
        filtered_tasks = tasks[:]
        if type_filter != "Все":
            filtered_tasks = [t for t in filtered_tasks if t['type'] == type_filter]
        task_to_delete = filtered_tasks[index]
        tasks.remove(task_to_delete)
    else:
        tasks.pop(index)

    update_task_list()
    messagebox.showinfo("Успех", "Задача удалена!")

# Функция очистки всех задач
def clear_all_tasks():
    if not tasks:
        messagebox.showinfo("Информация", "Список задач пуст!")
        return

    confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить ВСЕ задачи?")
    if confirm:
        tasks.clear()
        update_task_list()
        messagebox.showinfo("Успех", "Все задачи удалены!")


# Главное окно
root = tk.Tk()
root.title("Task Generator - Генератор случайных задач")
root.geometry("800x600")

# Метка заголовка
title_label = tk.Label(root, text="Task Generator", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# Фрейм для отображения случайной задачи
random_frame = tk.LabelFrame(root, text="Случайная задача", font=("Arial", 12))
random_frame.pack(pady=10, padx=20, fill="x")

random_task_label = tk.Label(random_frame, text="Нажмите 'Сгенерировать' для получения задачи",
                    wraplength=700, font=("Arial", 11), justify="center")
random_task_label.pack(pady=10)


btn_generate = tk.Button(random_frame, text="СГЕНЕРИРОВАТЬ СЛУЧАЙНУЮ ЗАДАЧУ",
                   bg="#2196F3", fg="white", font=("Arial", 11),
                   command=generate_random_task)
btn_generate.pack(pady=5)

# Фрейм для формы ввода
input_frame = tk.LabelFrame(root, text="Добавить новую задачу", font=("Arial", 12))
input_frame.pack(pady=10, padx=20, fill="x")


# Поле: Текст задачи
tk.Label(input_frame, text="Текст задачи:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_text = tk.Entry(input_frame, width=40)
entry_text.grid(row=0, column=1, padx=10, pady=5)


# Поле: Тип задачи
tk.Label(input_frame, text="Тип задачи:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
type_var = tk.StringVar()
type_list = ["учёба", "спорт", "работа", "отдых", "творчество", "саморазвитие"]
combo_type = ttk.Combobox(input_frame, textvariable=type_var, values=type_list, width=37, state="readonly")
combo_type.grid(row=1, column=1, padx=10, pady=5)
combo_type.current(0)


# Кнопка добавления задачи
btn_add = tk.Button(input_frame, text="Добавить задачу", font=("Arial", 11), bg="#4CAF50", fg="white", command=add_task)
btn_add.grid(row=2, column=0, columnspan=2, pady=10)


# Кнопки сохранения и загрузки
btn_frame = tk.Frame(input_frame)
btn_frame.grid(row=3, column=0, columnspan=2, pady=5)

btn_save = tk.Button(btn_frame, text="Сохранить в JSON", bg="#9C27B0", fg="white", command=save_data)
btn_save.pack(side=tk.LEFT, padx=5)


btn_load = tk.Button(btn_frame, text="Загрузить из JSON", bg="#9C27B0", fg="white", command=load_data)
btn_load.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(btn_frame, text="Удалить выбранную", bg="#F44336", fg="white", command=delete_task)
btn_delete.pack(side=tk.LEFT, padx=5)


btn_clear_all = tk.Button(btn_frame, text="Очистить всё", bg="#FF9800", fg="white", command=clear_all_tasks)
btn_clear_all.pack(side=tk.LEFT, padx=5)


# Фрейм для фильтров
filter_frame = tk.LabelFrame(root, text="Фильтры", font=("Arial", 12))
filter_frame.pack(pady=10, padx=20, fill="x")


# Фильтр по типу задачи
tk.Label(filter_frame, text="По типу:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
type_filter_var = tk.StringVar()
type_filter_list = ["Все", "учёба", "спорт", "работа", "отдых", "творчество", "саморазвитие"]
combo_type_filter = ttk.Combobox(filter_frame, textvariable=type_filter_var, values=type_filter_list, width=25, state="readonly")
combo_type_filter.grid(row=0, column=1, padx=10, pady=5)
combo_type_filter.current(0)

# Кнопки фильтров
btn_filter = tk.Button(filter_frame, text="Применить фильтр", bg="#2196F3", fg="white", command=apply_filter)
btn_filter.grid(row=0, column=2, padx=5, pady=5)

btn_reset = tk.Button(filter_frame, text="Сбросить", bg="#FF9800", fg="white", command=reset_filter)
btn_reset.grid(row=0, column=3, padx=5, pady=5)

# Фрейм для списка задач
list_frame = tk.Frame(root)
list_frame.pack(pady=10, padx=20, fill="both", expand=True)

# Список для отображения задач
task_listbox = tk.Listbox(list_frame, font=("Arial", 11), height=15)

# Полоса прокрутки
scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=task_listbox.yview)
task_listbox.configure(yscrollcommand=scrollbar.set)


task_listbox.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Статусная метка
status_label = tk.Label(root, text="Готов к работе", font=("Arial", 9), fg="blue")
status_label.pack(pady=5)

# Загрузка данных при запуске
load_data()

# Запуск приложения
root.mainloop()