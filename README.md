# Работа номер 3
# Цель работы
Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее.
# Постановка задач
Вариант №2

Задание №3

Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.

Входной текст на учебном конфигурационном языке принимается из
файла, путь к которому задан ключом командной строки. Выходной текст на
языке json попадает в стандартный вывод.

Однострочные комментарии:

REM Это однострочный комментарий

Многострочные комментарии:

--[[

Это многострочный

комментарий

]]

Словари:

table(

 имя => значение,
 
 имя => значение,
 
 имя => значение,
 
 ...
 
)

Имена:

[_a-zA-Z]+

Значения:

• Числа.

• Строки.

• Словари.

Строки:

@"Это строка"

Объявление константы на этапе трансляции:

set имя = значение

Вычисление константы на этапе трансляции:

${имя}

Результатом вычисления константного выражения является значение.

Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 3
примера описания конфигураций из разных предметных областей.

# Функции созданные в коде

all_read() - создаёт словарь в виде джейсона со всеми записями.

readd() - выдаёт результат обработки строки, показывая чем она является.

main() - основной код программы, где осуществляется работа с командной строкой.

Испульзуемые библиотеки

import json

import sys, os

# Сборка проекта

Сборка проекта осуществляется через командную строку, так как написан на питоне

py prac.py file.txt
# Результат работы
![image](https://github.com/user-attachments/assets/25d231c5-45e3-4c8d-bcbf-175f0a31c021)



# Тестирование и работа программы

Тесты были написаны вручную в файле test_prac.py
Результат прогона тестов показл, что функции работают корректно
![image](https://github.com/user-attachments/assets/4b1acc54-a9f8-4cfb-8901-73f22f411b16)
