# -*- coding: utf-8 -*-

import numpy as np
from random import randint
import cvxopt
from cvxopt.modeling import variable, op
import time

start = time.time()

z = cvxopt.modeling._function() # переменная для внесения в нее целевой функции
c = [] # список стоимости перевозки единицы товара от заказчиков к потребителям
supply = [] # список объёмов товаров на складах поставщиков
x = variable(9, 'x') # список объёмов перевозимых товаров, обеспечивающих минимальные затраты
x_non_negative = (x >= 0) # (ограничение)количесвто перевозимого товара не может быть отрицательно

a = 3 # количество поставщиков
b = 3 # количество покупателей
sumA = 0 # объем предложения
sumB = 0 # объем спроса

# функция пользователя (ввод данных)
def userScript():
    global c, supply
    # заполнение пользователем списка стоимости перевозки единицы товара от заказчиков к потребителям
    for element in input('введите матрицу (9 чисел): ').split():
        c.append(int(element))

    # заполнение пользователем списка объёмов товаров на складах поставщиков
    for element in input('введите запасы и потребности производства (6 чисел): ').split():
        supply.append(int(element))
    typeScript()

# функция определяет тип задачи, формирует целевую функцию и присваивает ограниения
def typeScript():
    global  sumA, sumB, z
    # определение типа задачи
    for i in range(a + b):
        if (i < a):
            sumA += supply[i]
        if (i >= b):
            sumB += supply[i]

    # формирование целевой функции
    for i in range(a * b):
        z += c[i] * x[i]

    # вызов функций ограничения
    if (sumA > sumB):
        closedProblem() # для открытой задачи
    else:
        openProblem() # для закрытой задачи

def closedProblem():
    global mass1, mass2, mass3, mass4, mass5, mass6
    # ограничения
    # количество перевозимых товаров с одного склада не может быть больше объема товара на складе
    mass1 = (x[0] + x[1] + x[2] <= supply[0])
    mass2 = (x[3] + x[4] + x[5] <= supply[1])
    mass3 = (x[6] + x[7] + x[8] <= supply[2])
    # количество перевозимых товаров с разных складов должно быть равно количеству спроса
    mass4 = (x[0] + x[3] + x[6] == supply[3])
    mass5 = (x[1] + x[4] + x[7] == supply[4])
    mass6 = (x[2] + x[5] + x[8] == supply[5])

def openProblem():
    global mass1, mass2, mass3, mass4, mass5, mass6
    # ограничения
    mass1 = (x[0] + x[1] + x[2] == supply[0])
    mass2 = (x[3] + x[4] + x[5] == supply[1])
    mass3 = (x[6] + x[7] + x[8] == supply[2])
    mass4 = (x[0] + x[3] + x[6] <= supply[3])
    mass5 = (x[1] + x[4] + x[7] <= supply[4])
    mass6 = (x[2] + x[5] + x[8] <= supply[5])

# основная функция собирает всю информацию и используя библиотеку cvxopt решает задачу
def mainScript():
    userScript() # вызываем необходимую функцию
    list = [mass1, mass2, mass3, mass4, mass5, mass6, x_non_negative]  # вносим в список все ограничения
    problem = op(z, list) # Optimization Problems

    # оптимизация в линейной программе в матричной форме
    # glpk - программный пакет, предназначенный для решения крупномасштабного линейного программирования
    problem.solve(solver='glpk')

    print("Результат Xopt:")
    for i in x.value:
        print(i)

    print("Стоимость доставки:")
    print(problem.objective.value()[0])

mainScript() # вызов главной функции

stop = time.time()
print ("Время :")
print(stop - start)
