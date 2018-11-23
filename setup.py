from urllib.parse import quote
import sys
import json
import time
import logging



try:
    logging.basicConfig(format = "%(asctime)s | %(levelname)s | %(message)s",level=logging.DEBUG)
    with open("./config.json", "r") as f:
        config = json.load(f)
except Exception as e:
    logging.error("初始化错误 message: %s",e)
    sys.exit()

def main():
    logging.info("程序开始 !")
    bot = Bot(config["path"],config["token"],config["command"])
    while True:
        newMsg = bot.askBot()
        for msg in newMsg:
            logging.debug("msg is : %s",msg["text"])
            #根据排行榜id获取音乐
            if msg["text"].find("/chart ") == 0:
                songId = int(msg["text"].replace("/chart ", ""))
                bot.sendAudio(msg["chat_id"],songId)
            #根据音乐搜索歌曲
            elif msg["text"].find("/listen ") == 0:
                songId = int(msg["text"].replace("/listen ", ""))
                bot.sendIdAudio(msg["chat_id"],songId)
            #查找排行榜页
            elif msg["text"].find("/page ") == 0:
                pageId = int(msg["text"].replace("/page ", ""))
                bot.sendChart(chatId = msg["chat_id"],page = pageId)
            #查找 "歌""
            elif parse.quote(msg["text"]).find("%E6%AD%8C") != -1:
                bot.sendChart(msg["chat_id"],1)
            #查找"我要听"
            elif parse.quote(msg["text"]).find("%E6%88%91%E8%A6%81%E5%90%AC") == 0:
                msg["text"].replace("%E6%88%91%E8%A6%81%E5%90%AC", '')
                bot.sendSeacSong(msg["chat_id"],msg["text"])
            else:
                bot.sendChart(msg["chat_id"],1)
        time.sleep(config["appsleep"])

if __name__ == "__main__":
    main()