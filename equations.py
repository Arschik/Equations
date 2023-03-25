from itertools import permutations
from copy import deepcopy
from numpy import array
from fractions import Fraction
s = {"0":"₀","1":"₁","2":"₂","3":"₃","4":"₄","5":"₅","6":"₆","7":"₇","8":"₈","9":"₉"}
def trans(frac:Fraction) -> str:
    """Преобразует переменную класса Fraction в привычный вид

    Args:
        frac (Fraction): объект класса Fraction

    Returns:
        str: trans(Fraction(1,3)) -> "1/3", 
             trans(Fraction(0,1)) -> "0"
    """
    frac = frac.as_integer_ratio()
    if str(frac[1]) == "1":
        return str(frac[0])
    return str(frac[0]) + "/" + str(frac[1])
    
def check_inversion(lst:tuple) -> int:
    """Проверяет чётность перестановки
    Например, check_inversion([1,2,3,4,5]) -> 2,
    check_inversion([2,1,3,4,5]) -> 1

    Args:
        lst (tuple): перестановка

    Returns:
        int: если перестановка нечетна, возвращает 1, иначе 2
    """
    sum_ = 0
    for i in lst:
        for j in lst[lst.index(i) + 1:]:
            if i > j:
                sum_ += 1
    if sum_ % 2 == 0:
        return 2
    return 1
def check_det(m:list) -> int:
    """ Считает значение определителя

    Args:
        m (list): матрица, определитель которой будет высчитан

    Returns:
        int: check_det([1,2],[4,3]) -> -5
    """
    det = 0
    perms = permutations(range(len(m)))
    for perm in perms:
        mult = 1
        i = 0
        for j in perm:
            mult *= m[i][j]
            i += 1
        det += mult * (-1)**(check_inversion(perm))
    return det
def rang(matrix:list) -> tuple:
    """ Возвращает ранг матрицы, список индексов линейно независимых строк и столбцов

    Args:
        matrix (list): матрица, ранг которой будет подсчитан

    Returns:
        возвращает кортеж с тремя индексами
        0 - ранг матрицы
        1 - список индексов линейно независимых строк
        2 - список индексов линейно независимых столбцов
    """
    if matrix == [[0]*len(matrix[0]) for _ in range(len(matrix))]:
        return (0,[0],[0])
    if [0]*len(matrix[0]) in matrix: # удаляет нулевую стркоу при наличии
        matrix.remove([0]*len(matrix[0]))
    r = 1
    minor = [[matrix[0][0]]] #тут будет наибольший отличный от нуля минор
    strings = [0]
    columns = [0]
    for cur_string in range(len(matrix)):
        if cur_string not in strings: #ищем строку
            new_minor = deepcopy(minor) + [[]]
            for column in columns:
                new_minor[-1].append(matrix[cur_string][column]) #окаймление строкой
                minor_before_column = deepcopy(new_minor)
            for cur_column in range(len(matrix[0])):
                if cur_column not in columns: #ищем столбец
                    i = 0
                    for string in strings:
                        new_minor[i].append(matrix[string][cur_column]) #окаймление столбцом
                        i += 1
                    new_minor[i].append(matrix[cur_string][cur_column])
                    if check_det(new_minor) != 0:
                        minor = new_minor.copy()
                        strings += [cur_string]
                        columns += [cur_column]
                        strings.sort()
                        columns.sort()
                        r += 1
                        break
                    else:
                        new_minor = deepcopy(minor_before_column)
    return r,strings,columns
if __name__ == "__main__":
    wide_a = [[1,2,3,4],[5,3,4,5],[8,8,6,1]]
    eq = int(input("Введите количество уравнений: "))
    if eq <= 0:
        raise ValueError 
    var = int(input("Введите количество переменных: "))
    if var <= 0:
        raise ValueError
    for i in range(eq):
        temp = []
        for j in range(var):
            index = ""
            for l in str(j):
                index += l
            temp.append(int(input(f"x{s[str(int(index) + 1)]} = ")))
        index = ""
        for l in str(i):
            index += l
            temp.append(int(input(f"b{s[str(int(index) + 1)]} = ")))
        wide_a.append(temp)

    a = [i.copy()[:-1] for i in wide_a]
    r,strings,columns = rang(wide_a)
    if r != rang(a)[0]:
        print("Решений нет")
    elif r == 0:
        print("x₁ ∈ ℝ")
    else:
        free = sorted({i + 1 for i in range(len(wide_a[0]))} - {i + 1 for i in columns})[:-1] #новые свободные члены
        det_content = [[] for _ in range(r)] #будущая матрица из коэффицентов в миноре наивысшего порядка, не равного нулю
        prev_a = deepcopy(a) # нужен т.к, удаляя из a элементы, мы нарушим порядок индексков
        for i in strings: # заполняем определитель
            for j in columns:
                det_content[i].append(prev_a[i][j])
                a[i].remove(prev_a[i][j])
        for i in strings: # переносим свободные члены в правую часть
            a[i] = array([wide_a[i][-1]] + [-i for i in a[i]])
        det = Fraction(check_det(det_content)) #значение минора наивысшего порядка
        for column in range(len(det_content)): #подставляем столбец свободных членов в минор, согласно правилу Крамера
            new_det = deepcopy(det_content)
            for string in range(len(det_content)):
                new_det[string][column] = a[string].copy()
            ans = check_det(new_det)/det #список коэффицентов при свободных переменных и начального свободного члена 
            ans = list(map(trans,ans))
            for i in range(1, len(ans)): #добавляем свободные переменные к свободным членам
                index = ""
                for j in str(free[i - 1]):
                    index += s[j]
                ans[i] = ans[i] + "x" + index

            index = ""
            for j in str(columns[column]): #добавляем индексы к зависимым пременным
                index += s[str(int(j) + 1)]
            for i in range(1,len(ans)): #приводим ответ в более приятный для глаза вид
                if ans[i][0] != "-":
                    ans[i] = "+ " + ans[i]
                else:
                    ans[i] = "- " + ans[i][1:]
                if ans[i][0] == "1":
                    ans[i] = ans[i][1:]
                
            ans = " ".join(ans)
            print(f"x{index} = {ans}")
