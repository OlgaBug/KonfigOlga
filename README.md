# Работа номер 1
# Цель работы
Изучить зависимостей для коммитов.
# Постановка задач
Вариант №2

Задание №1

Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
tar. Эмулятор должен работать в режиме GUI.

Конфигурационный файл имеет формат ini и содержит:

• Имя пользователя для показа в приглашении к вводу.

• Путь к архиву виртуальной файловой системы.

• Путь к лог-файлу.

• Путь к стартовому скрипту.

Лог-файл имеет формат json и содержит все действия во время последнего
сеанса работы с эмулятором. Для каждого действия указан пользователь.
Стартовый скрипт служит для начального выполнения заданного списка
команд из файла.

Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:

1. date.

2. find.

Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 2 теста.

# Функции созданные в коде

add_folder() - соединяет компоненты пути файловой системы

remove_last_folder() - возвращает имя котолога

class Emulator

get_prompt_directory() - функия для получения текущей директории используется для отображения в prompt

load_file_system() - функция для распаковки TAR архива в виртуальную файловую систему

ls() - выводит и возвращяет список файлов и папок в указанной директории (или текущей, если аргумент не передан)

cd() - перемещает на директорию, которая была указана

date_lin() - выводит и возвращает текущую дату и время в соответствии с настройками локали системы

find_lin() - выводит и возвращает список файлов с названием, которое было ввидено

class EmulatorGUI

run_command() - Обработчик ввода команды и её выполнения

execute_command() - выполнение команд через эмулятор

Испульзуемые библиотеки

import os

import json

import tarfile

import configparser

import tkinter as tk

from tkinter import scrolledtext

from datetime import datetime

# Сборка проекта

Сборка проекта осуществляется через командную строку, так как написан на питоне

python emul.py --tar_path ttt.tar --log_path emulator.txt - команда для командной строки

# Тестирование и работа программы

Тэсты были проведены в ручную

Проверка работы команд ls и cd

первая команда cd должна была изменить текущую дерикторию на заданную, что успешно было сделано, это можно проверить вызвав команду ls, которая выводит файлы в ней, они были правильно выведины "vtoroy.txt"

первая команда cd должна была изменить текущую дерикторию на главную, что успешно было сделано, это можно проверить вызвав команду ls, которая выводит файлы в ней, они были правильно выведины "papkapervay" и "pervy.txt"

![image](https://github.com/user-attachments/assets/1b0f58a8-2cef-4b79-9db1-2842c2a84693)

Проверка работы команды date, на скриншоте показано врем и дата соответсвующее Московскому времяни, секунды не точные, так как скриншёт был сделан не мгновенно, после выполнения команд

![image](https://github.com/user-attachments/assets/b1bc2c31-e4d3-439d-ab5e-6ca0d3543ffe)

Проверка работы команды find, если ввести "pervy.txt" то программа должна вывести pervy.txt, что успешно выводит, если ввести файл без ковычек, то выдаст пустую деректорию

![image](https://github.com/user-attachments/assets/fb89f6e5-a9cd-4fc3-8cfa-0187318146f3)
