import provide

import requests
import logging
import json
import logging
class Bot:
    '''
    r是基于requests实例化
    u是telegram网址记录
    i标记每次消息递增id
    l请求头长度
    '''
    r = requests.Session()
    u = ''
    i = 0
    l = 0

    def __init__(self, path, token, command):
        """初始化数据"""
        self.u = path.replace('<TOKEN>',token)
        self.r.verify = True
        self.r.timeout = 3
        self.r.headers = {"Content-Type":"application/json"}
        ##处理url的实例化
        Bot.askBotUrl = self.u.replace('<COMMAND>',command["askBot"])
        Bot.sendAudioUrl = self.u.replace('<COMMAND>',command["sendAudio"])
        Bot.sendMsgUrl = self.u.replace('<COMMAND>',command["sendMsg"])

    def askBot(self):
        result = []
        res = self.r.get(Bot.askBotUrl)
        #判断是否收到新消息
        if res.headers['Content-Length'] == Bot.l:
            return result
        Bot.l = res.headers['Content-Length']
        results = json.loads(res.content)
        if results["ok"] == False:
            logging.error(results)
            return result
        metadata = results["result"]
        for x in reversed(metadata):
            if x["update_id"] > Bot.i:
                one = {}
                if "callback_query" in x:
                    one["chat_id"] = x["callback_query"]["message"]["chat"]["id"]
                    one["text"] = x["callback_query"]["data"]
                elif ("message" in x) and ("text" in x["message"]):
                    one["chat_id"] = x["message"]["chat"]["id"]
                    one["text"] = x["message"]["text"]
                else:
                    logging.error("ask err",x)
                    continue
                result.append(one)
            else:
                break
        Bot.i = metadata[-1]['update_id']
        return result

    def sendAudio(self,chatId,songId):
        res = provide.getById(songId)
        result = {
            "chat_id":chatId,
            "audio":res["url"],
            "caption":'`'+ res["text"] +'`',
            "parse_mode" : "Markdown"
        }
        self.r.post(Bot.sendAudioUrl, json = result)

    def sendChart(self, chatId, page):
        text = '''
        * - 今日虾米音乐排行榜 - * 
        联系我 @pennfly
        `嘿嘿嘿！现在程序还非常脆弱，不停完善中..`
        '''
        result = {
            "chat_id" : chatId,
            "text" : text,
            "reply_markup" : { "inline_keyboard" :  provide.getlist(page) },
            "parse_mode" : "Markdown"
        }
        self.r.get(Bot.sendMsgUrl , json = result)
