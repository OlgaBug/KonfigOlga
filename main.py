import os
import json
import tarfile
import configparser
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

def add_folder(path, folder_name):
    return os.path.join(path, folder_name)


def remove_last_folder(path):
    return os.path.dirname(path)

class Emulator:
    def __init__(self, username, hostname, tar_path, log_path, start_cript):
        self.username = username
        self.hostname = hostname
        self.current_directory = '/'  # Текущая директория (начинаем с корня '/')

        self.absolute_path = r"c:\Users\USER1\OneDrive\Desktop\КонфигДР1"
        self.start_cript = start_cript
        self.tar_path = tar_path
        self.log_path = log_path
        self.p = 0
        self.file_system = {}  # Словарь для хранения распакованных файлов и папок
        self._load_file_system()  # Распаковываем архив в память
    
    def _get_prompt_directory(self):
        """Метод для получения текущей директории для отображения в prompt."""
        return self.current_directory if self.current_directory != '/' else '/'
    
    def _load_file_system(self):
        """
        Метод для распаковки TAR архива в виртуальную файловую систему.
        """
        if tarfile.is_tarfile(self.tar_path):
            with tarfile.open(self.tar_path, 'r') as tar_ref:
                for file in tar_ref.getnames():
                    p = file.find('/')
                    normalized_path = file[p+1:] # Удаляем начальные / для удобства работы с файлами
                    if normalized_path != "ttt":
                        self.file_system[normalized_path] = "Содержимое"  # Добавляем файлы в словарь
        else:
            print("Error: provided file is not a TAR archive.")

    def ls(self, directory=None):
        """
        Команда 'ls' выводит список файлов и папок в указанной директории (или текущей, если аргумент не передан).
        """
        if directory:
            path = os.path.join(self.current_directory, directory).lstrip('/')
        else:
            path = self.current_directory.lstrip('/')

        output = []
        found_files = False
        for file in self.file_system:
            if file.startswith(path):
                relative_path = file[len(path):].strip('/')
                if '/' not in relative_path:
                    output.append(relative_path)
                    found_files = True

        if not found_files:
            output.append("Directory is empty.")

        response = '\n'.join(output)
        print(response)
        return response

    def cd(self, path):
        """
        Команда 'cd' позволяет перемещаться между директориями.

        :param path: Путь к новой директории
        """
        if path == "..":
            if self.current_directory != '/':
                self.current_directory = os.path.dirname(self.current_directory.rstrip('/')) + '/'
                self.absolute_path = remove_last_folder(self.absolute_path) # Переход на уровень выше
        else:
            new_directory = os.path.join(self.current_directory, path).lstrip('/') # Переход в указанную директорию
            if any(f.startswith(new_directory) for f in self.file_system.keys()):
                self.current_directory = new_directory.rstrip('/') + '/'
                self.absolute_path = add_folder(self.absolute_path, path)
            else:
                response = "Error: directory not found."
                print(response)
                return response
        return ""
    
    def date_lin(self):
        """
        Команда 'date' выводит текущую дату и время в соответствии с настройками локали системы.

        """
        now = datetime.now()
        print(now)
        return now
    
    def find_lin(self, dop):
        """
        Команда 'find' пвыводит список файлов с названием которое было ввидено, без учёта регистра, если было это задано.
        """
        n_path = dop.split(" ")
        if n_path[0] != ".":
            path = os.path.join(self.current_directory, n_path[0]).lstrip('/')
        else:
            path = self.current_directory.lstrip('/')

        output = []
        found_files = False
        for file in self.file_system:
            if file.startswith(path):
                relative_path = file[len(path):].strip('/')
                if '/' not in relative_path:
                    if n_path[1] == "-name":
                        if n_path[2][1:-1] == relative_path:
                            output.append(relative_path)
                            found_files = True

        if not found_files:
            output.append("Directory is empty.")

        response = '\n'.join(output)
        print(response)
        return response




class EmulatorGUI:
    def __init__(self, emulator):
        self.emulator = emulator

        self.window = tk.Tk() # Создание главного окна
        self.window.title("Linux Emulator")
        self.window.configure(bg="black")

        self.window.minsize(900, 500)

        self.output_text = scrolledtext.ScrolledText(self.window, width=80, height=20, bg="black", fg="green",
                                                     state='disabled', font=("Consolas", 12))
        self.output_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # sticky nsew позволяет растягивать элемент

        self.host_display = tk.Label(self.window, text=f"current directory: {emulator.username}@{emulator.hostname}:{emulator._get_prompt_directory()}$",
                                     bg="black", fg="green", font=("Consolas", 12), anchor="w")
        self.host_display.grid(row=2, column=0, sticky='w', padx=10, pady=5) # Область для отображения текущего хоста и директории

        self.command_entry = tk.Entry(self.window, width=80, bg="black", fg="green", font=("Consolas", 12), insertbackground="green") # Поле для ввода команд
        self.command_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.run_command()
        self.command_entry.bind('<Return>', self.run_command) # Привязываем событие нажатия Enter

        self.window.grid_rowconfigure(0, weight=1)  # Растягиваем область вывода по вертикали
        self.window.grid_rowconfigure(1, weight=0)  # Поле для ввода команды не должно сильно изменять размер
        self.window.grid_rowconfigure(2, weight=0)  # Строка хоста фиксирована по высоте
        self.window.grid_columnconfigure(0, weight=1)  # Растягиваем все элементы по горизонтали

        self.window.mainloop() # Запуск основного цикла окна
    

    def run_command(self, event=None):
        """Обработчик ввода команды и её выполнения."""
        if emulator.p == 0:
            f = open(emulator.start_cript)
            commands = f.readlines()
            for command in commands:
                command = command[:-1]
                self.output_text.config(state='normal')
                self.output_text.insert(tk.END, f"{emulator.username}@{emulator.hostname}:{emulator._get_prompt_directory()}$ {command}\n")
                self.output_text.config(state='disabled')
                data = {"username": emulator.username, "hostname": emulator.hostname, "command": command, "rezult": 1}
                self.command_entry.delete(0, tk.END)  # Очищаем поле ввода

                output = self.execute_command(command) # Получаем результат команды из эмулятора
                with open(emulator.log_path, 'a') as log_file:
                    str_outtput = str(output)
                    data = {"username": emulator.username, "hostname": emulator.hostname, "command": command, "rezult": str_outtput}
                    json.dump(data, log_file)

                self.host_display.config(text=f"current directory: {emulator.username}@{emulator.hostname}:{emulator._get_prompt_directory()}$") 
                self.host_display.update() # Обновляем область вывода
                self.output_text.config(state='normal')
                self.output_text.insert(tk.END, f"{output}\n")
                self.output_text.config(state='disabled')
                self.output_text.yview(tk.END)  # Прокрутка вниз
                emulator.p = 1
            f.close()
        else:
            command = self.command_entry.get()
            self.output_text.config(state='normal')
            self.output_text.insert(tk.END, f"{emulator.username}@{emulator.hostname}:{emulator._get_prompt_directory()}$ {command}\n")
            self.output_text.config(state='disabled')
            data = {"username": emulator.username, "hostname": emulator.hostname, "command": command, "rezult": 1}
            self.command_entry.delete(0, tk.END)

            output = self.execute_command(command)
            with open(emulator.log_path, 'a') as log_file:
                    str_outtput = str(output)
                    data = {"username": emulator.username, "hostname": emulator.hostname, "command": command, "rezult": str_outtput}
                    json.dump(data, log_file)

            self.host_display.config(text=f"current directory: {emulator.username}@{emulator.hostname}:{emulator._get_prompt_directory()}$")
            self.host_display.update()
            self.output_text.config(state='normal')
            self.output_text.insert(tk.END, f"{output}\n")
            self.output_text.config(state='disabled')
            self.output_text.yview(tk.END)

    def execute_command(self, command):
        """Метод для выполнения команд через эмулятор."""
        if command.startswith("ls"):
            args = command.split(" ")
            if len(args) == 2:
                return self.emulator.ls(args[1])
            else:
                return self.emulator.ls()
        elif command.startswith("cd "):
            return self.emulator.cd(command.split(" ")[1])
        elif command.startswith("date"):
            return self.emulator.date_lin()
        elif command.startswith("find"):
            args = command.split(" ")
            if len(args) == 4:
                return self.emulator.find_lin(command[5:])
            else:
                return "Unknown command."
        elif command == "exit":
            print(1)
            self.window.destroy()
            return "Exiting emulator..."
        else:
            return "Unknown command."


# Основной код
if __name__ == "__main__":

    CONFIG_PATH = 'conf.ini'
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    username = config['Section1']['name']
    tar_path = config['Section1']['tar_file']
    start_cript = config['Section1']['scr']
    log_path = config['Section1']['log_file']

    hostname = "my_pc"
    absolute_path = r"c:\Users\USER1\OneDrive\Desktop\КонфигДР1"

    emulator = Emulator(username, hostname, tar_path, log_path, start_cript) # Объект имюлятора

    gui = EmulatorGUI(emulator) # Создание и запуск графического интерфейса