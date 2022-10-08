import os
import json

def antihack(message):
    print(type(message))
    out = True
    test = list(message)
    if "$" == test[0] or "{" == test[0] or "(" == test[0]:
        out = False
    if out == False:
        return out
    else:
        for i in test:
            if "$" == i or "{" == i or "(" == i:
                out = False
                break
        if out == False:
            return out
        if "$(" in message or "${" in message or "(" in message or "{" in message:
            return False
        else:
            return True           

def parsejson(radioid=15016):
    print("Downloading...")
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

def checkyoutubeurl(url):
    print(f"URL: {url}")
    print("Checking url...")
    if url.startswith("https://youtube.com/watch?") or url.startswith("https://youtu.be") or url.startswith("http://youtube.com/watch?") or url.startswith("http://www.youtube.com/watch?") or url.startswith("https://www.youtube.com/watch?") or url.startswith("youtube.com/watch?") or url.startswith("www.youtube.com/watch?"):
        print("This is youtube url!")
        return "ytdl"
    elif url.startswith("https://") or url.startswith("http://"):
        print("This is not youtube url!")
        return "url"
    elif url.startswith("https://youtube.com/playlist?") or url.startswith("http://youtube.com/playlist?") or url.startswith("https://www.youtube.com/playlist?") or url.startswith("http://www.youtube.com/playlist?") or url.startswith("www.youtube.com/playlist?") or url.startswith("youtube.com/playlist?"):
        print("This is a playlist!")
        return "playlist"
    else:
        print("This is not url!")
        return "ytdl"
