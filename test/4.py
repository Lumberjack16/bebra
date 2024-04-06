import asyncio
import socket
async def start_game():
    obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    await obj.connect(("80.77.36.110",2023))
    with open("file/userdata.json","r") as f:
        text=f.read()
    #text="token ({0})".format(text)
    await obj.sendall(text.encode("utf-8"))
    #date=obj.recv(1024)
    #print(date.decode("utf-8"))
async def funk():
    for i in range(100000):
        print(i)
        await asyncio.sleep(0.01)
async def funk2():
    for i in range(-100000,0):
        print(i)
        await asyncio.sleep(0.01)
async def main():
    t0=asyncio.create_task(start_game())
    t1=asyncio.create_task(funk())
    t2=asyncio.create_task(funk2())
    await asyncio.gather(t0,t1,t2)
if __name__=="__main__":
    asyncio.run(main())