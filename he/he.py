import heapq
#s=[4,54,6,4,1,1]
"""s.sort()
s.append(5)
s.sort()
print(*s)"""

"""heapq.heapify(s)
print(*s)
k=len(s)
for i in range(k):
    print(heapq.heappop(s),end=" ") 
print("s:",s)"""
import time
import random
import threading
lock=threading.Lock()
all_commands=[]
def fun1():
    while True:
        time.sleep(1)
        with lock:
            heapq.heappush(all_commands,(random.randint(1,3),time.time(),"command"))
t1=threading.Thread(target=fun1)
t1.start()
def fun2():
    while True:
        time.sleep(2)
        if all_commands:
            with lock:
                print(heapq.heappop(all_commands)," all",all_commands)
t2=threading.Thread(target=fun2)
t2.start()