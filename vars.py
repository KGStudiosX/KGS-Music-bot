import json

TOKEN = "YOUR TOKEN HERE"
errorjson = json.dumps(
    {
    "result": "false"
    })
compjson = json.dumps(
    {
    "result": "true"
    })
radioldb = {
    "main": "http://radiorecord.hostingradio.ru/rr_main96.aacp",
    "phonk": "https://radiorecord.hostingradio.ru/phonk96.aacp"
}
radiodb = {
    "main": 15016,
    "phonk": 43174
}
pausestate = False
userstate = "none"
botdebug=False
currentradio = "main"
queuelist = [
    
]
blockedusers =[
    
]
apistatusjson = {
    "playing": "false",
    "type": "idle",
    "url": "none",
    "name": "none",
    "author": "none"
}