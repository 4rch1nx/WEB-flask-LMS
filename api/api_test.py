from requests import get

parametrs = {'apikey': 'R90955l1z65360dnld003z'}
answer = get('http://localhost:8080/api/single', json=parametrs).json()
print(answer)