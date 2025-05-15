from requests import post, get, put

parametrs = {'api_key': 'y57blu0890557r9mVzW0PgJ5Q4r3y5',
             'device_id': 1}
answer = get('http://localhost:8080/api/saved_devices/single', json=parametrs).json()
print(answer)