import time
import pywifi
from pywifi import const

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

def find_ESP():
    iface.scan()
    time.sleep(2)
    networks = iface.scan_results()
    available_esp_nets = []
    for net in networks:
        if "ESP8266_CAR" in net.ssid:
            available_esp_nets.append(net)
    if len(available_esp_nets) > 0:
        return available_esp_nets
    else:
        return None


def connect_to_wifi(ssid):
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = 12345678

    # Удаляем возможные дубликаты профилей
    for i in iface.scan_results():
        if i.ssid == ssid:
            iface.remove_network_profile(i)

    # Добавляем профиль и подключаемся
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    time.sleep(3)  # Даём время на подключение

    # Проверяем статус подключения
    if iface.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False


