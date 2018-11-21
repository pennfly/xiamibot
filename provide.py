from urllib import parse
from lxml import etree
import requests
import time
import json

def urlDecrypt(s):
    '''负责解码url'''
    start = s.find('h')
    row = int(s[0:start])
    length = len(s[start:])
    column = length // row
    suck = length % row 
    real_s = list(s[1:])
    output = ''
    sucks = []
    for i in range(1, suck + 1):
        sucks.append(real_s[i * (column)])
        real_s[i * (column)] = 'sucks'
        real_s.remove('sucks')
    for i in range(column):
        output += ''.join(real_s[i:][slice(0, length, column)])
    output += ''.join(sucks)
    return parse.unquote(output).replace('^', '0')

def getFrom():
    '''负责数据的采集和存储'''
    jsonName = './storage/data/' + time.strftime("%Y-%m-%d", time.localtime()) + '.json'
    try:
        with open(jsonName, 'r') as f:
            data = json.load(f)
    except Exception as e:
        url = "https://www.xiami.com/chart/data?c=103&type=0&page=1&limit=100&_=1542620245713"
        header = { 
            'Accept': '*/*',
            'Connection': 'keep-alive', 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
        getHtml = requests.get(url , verify = True , headers = header)
        lists = etree.HTML(getHtml.text).xpath('//tr');
        data = []
        for x in lists:
            ress = {}
            ress["demoid"] = x.attrib['data-demoid']
            ress["index"] = x.attrib['data-index']
            ress["text"]  = x.attrib['data-title']
            try:
                ress["url"]   = urlDecrypt(x.attrib['data-mp3'])
                ress["status"] = 1
            except Exception as e:
                ress["status"] = 0
                ress["url"]   = 'https://www.xiami.com/search?key='+ ress["text"] +'&pos=1'
            data.append(ress)
        # 写入 JSON 数据
        with open(jsonName, 'w') as f:
            json.dump(data, f)
    return data

def getlist(page):
    resFrom =  getFrom();
    response = [];
    start = (page - 1) * 6
    print("start is %d start",start)
    for x in range(0,3):
        ress = resFrom[start:start+2]
        start += 2
        for i in range(len(ress)):
            ress[i].pop('url')
            ress[i]['callback_data'] = '/chart '+ ress[i]['index']
        response.append(ress)
    nexts = {
        "text":"下一页",
        "callback_data":"/page " + str(page + 1)
    }
    now = {
        "text":"当前第" + str(page) + "页",
        "callback_data":"/null "
    }
    lasts = {
        "text":"上一页",
        "callback_data":"/page " + str(page - 1)
    }
    page = [lasts,now,nexts]
    response.append(page)
    return response;

def getById(gid):
    resFrom = getFrom()
    res = resFrom[gid]
    # print(res)
    return res

