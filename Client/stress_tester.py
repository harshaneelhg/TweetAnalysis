import requests
import random
import time
import thread

def thread_function(tNum):
    base_url = 'http://192.168.56.101:8080/api/'
    data = {'username':'abc','password':'abc'}
    while True:
        response = requests.post(base_url+'login', data=data)


current_milli_time = lambda: int(round(time.time() * 1000))
response = requests.post("http://192.168.56.101:8080/api/startStressTest")
print response.json()
n_thread = 100
while n_thread>0:
    #rand_part_num = random.randint(1,5)
    thread.start_new_thread(thread_function, (n_thread,))
    n_thread -= 1

t1 = current_milli_time()

while True:
    if current_milli_time() - t1 > 20000:
        break

response = requests.post("http://192.168.56.101:8080/api/endStressTest")
print response.json()
