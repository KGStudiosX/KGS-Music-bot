import os
import json

def antihack(message):
    print(1)
    print(message)
    print(type(message))
    out = True
    test = list(message)
    print(test)
    if "$" == test[0] or "{" == test[0] or "(" == test[0]:
        print("WARN")
        out = False
    if out == False:
        return out
    else:
        print(2)
        for i in test:
            if "$" == i or "{" == i or "(" == i:
                print("WARN")
                out = False
                break
        print(3)
        if out == False:
            return out
        if "$(" in message or "${" in message or "(" in message or "{" in message:
            print("WARN")
            return False
        else:
            return True           

def parsejson():
    print("Downloading...")
    radioid = 15016
    os.system("curl https://www.radiorecord.ru/api/stations/now/ > /tmp/list.json")
    print("Opening file...")
    recordlist = json.load(open("/tmp/list.json"))
    for i in recordlist["result"]:
        if i["id"] == radioid:
            print("Founded record dance radio")
            print("Getting info...")
            recordtrack = i["track"]
            break
        else:
            pass
    recordtrackinfo = {
        "song": recordtrack["song"],
        "artist": recordtrack["artist"]
    }
    print("Parser work done!")
    return recordtrackinfo
