import time
from requests import get

from Other.code_reader import read_code

ESP_server = "http://192.168.4.1/servo_"
speed_argument = "?speed="
motors_speeds_for_actions = {"вперед": [180, 0],
                             "назад": [0, 180],
                             "налево": [0, 0],
                             "направо": [180, 180],
                             "стоп": [90, 90]}


def send_algorithm(algorithm):
    list_of_functions = read_code(algorithm)
    if isinstance(list_of_functions, str):
        return list_of_functions
    for function in list_of_functions:
        action, delay = function
        motors_speeds = motors_speeds_for_actions[action]
        error = send_message_to_ESP(motors_speeds)
        if error is not None:
            return error
        time.sleep(int(delay))
        error = send_message_to_ESP(motors_speeds_for_actions["стоп"])
        if error is not None:
            return error


def send_message_to_ESP(motors_speeds):
    try:
        get(ESP_server + "l" + speed_argument + str(motors_speeds[0]))
        get(ESP_server + "r" + speed_argument + str(motors_speeds[1]))
    except:
        return "Ошибка подключения к машинке! Проверьте, подключен ли ваш компьютер к WiFi сети машинки!"