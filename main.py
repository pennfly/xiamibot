from xmbot import Bot
import sys
import json
import time
import logging

logging.basicConfig(format = "%(asctime)s | %(levelname)s | %(message)s")

try:
    with open("./config.json", "r") as f:
        config = json.load(f)
except Exception as e:
    logging.error("Configuration err; message: %s",e)
    sys.exit()

def main():
    bot = Bot(config["path"],config["token"],config["command"])
    while True:
        logging.info(">>>starting: ",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        newMsg = bot.askBot()
        for msg in newMsg:
            print("msg is : %s",msg["text"])
            #根据id获取音乐
            if msg["text"].find("/chart ") == 0:
                songId = int(msg["text"].replace("/chart ", ""))
                bot.sendAudio(msg["chat_id"],songId)
            #排行榜分页
            elif msg["text"].find("/page ") == 0:
                pageId = int(msg["text"].replace("/page ", ""))
                bot.sendChart(chatId = msg["chat_id"],page = pageId)
            #匹配所有
            else:
                bot.sendChart(msg["chat_id"],1)
        logging.info("end<<<<")
        time.sleep(config["appsleep"])

if __name__ == "__main__":
    main()