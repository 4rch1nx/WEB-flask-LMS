import datetime

available_actions = ["вперёд", "назад", "направо", "налево"]


def read_code(code):
    list_of_functions = code.split(',')
    functions = []
    for function in list_of_functions:
        if function != "":
            error = find_error_in_function(function)
            if error is None:
                action = function[:function.find("(")]
                time = function[function.find("(") + 1:-1]
                functions.append([action, time])
            else:
                return error
    return functions


def find_error_in_function(func):
    function = delete_comments(func)
    function = function.replace(" ", "")
    function = function.replace("\n", "")
    if function == "":
        return None
    if (function.startswith("вперёд(") or function.startswith("назад(") or
        function.startswith("налево(") or function.startswith("направо(")) and function.endswith(")"):
        time = function[function.find("(") + 1:-1]
        if not time.isdigit():
            return f"Ошибка! Недопустимый аргумент функции: '{func}'. В качестве аргумента можно передать только целое число!"
        else:
            return None
    else:
        if (function.startswith("вперёд(") or function.startswith("назад(") or
            function.startswith("налево(") or function.startswith("направо(")) and ")" not in function:
            return f"Ошибка! В команде '{func}' отсутствует закрывающаяся скобка ')'"

        elif (function.startswith("вперёд(") or function.startswith("назад(") or
              function.startswith("налево(") or function.startswith("направо(")) and not function.endswith(")"):
            return f"Ошибка в строке '{func}'! В каждой строке должна быть только функция и её аргумент!"

        elif (not function.startswith("вперёд(") and not function.startswith("назад(") and
              not function.startswith("налево(") and not function.startswith("направо(")):
            return f"Ошибка! Недопустимая команда: '{func}'"

        else:
            return f"Ошибка! Недопустимая команда: '{func}'"


def find_errors_in_code(code):
    list_of_functions = code.split(',')
    for function in list_of_functions:
        if function != "":
            error = find_error_in_function(function)
            if error is not None:
                return error


def delete_comments(string):
    if "//" in string:
        string = string[:string.find("//")]
    return string


def make_algorithm_name():
    time = datetime.datetime.now().strftime("%d_%b_%H:%M:%S")
    name = "Sketch_" + time
    return name
