import json
s={"риба":5,"щось":"%$#%$%","так":True}
with open("file.txt","w") as f:
    f.write(json.dumps(s))
with open("file.txt","r") as f:
    info=json.loads(f.read())
print(info)