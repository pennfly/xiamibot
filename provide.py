from urllib import parse
from lxml import etree
import requests
import time
import json

print(config)

header = { 
    'Accept': '*/*',
    'Connection': 'keep-alive', 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}

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

#-------------------以上为排行榜-----------以下为歌曲搜索--------------#
def urlSongDec(s):
    start = s.find('%')
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

def searchSong(strSearch):
    url = "https://www.xiami.com/search/song/?spm=a1z1s.3521865.23309985.2.4n06Bl&key=" + strSearch
    xpath = '//*[@id="wrapper"]/div[2]/div[2]/div/div[2]/div[1]/div[1]/table/tbody/tr'
    getHtml = requests.get(url , verify = True , headers = header)
    lists = etree.HTML(getHtml.text).xpath(xpath)[0:6]
    
    data = []
    for x in lists:
        one = {}#获取歌曲id,歌曲详情还有歌手信息
        one["id"] = x.findall('./td[@class="chkbox"]/input')[0].get('value')
        one["name"] = x.findall('./td[@class="song_name"]/a[@target="_blank"]')[0].get('title')
        one["artist"] = x.findall('./td[@class="song_artist"]/a')[0].get('title')
        one["text"] = one["name"] + " - " +one["artist"]
        one["callback_data"] = "/listen " + one["id"]
        data.append(one);

    response = []
    start = 0
    for x in range(0,3):
        ress = data[start:start+2]
        start += 2
        response.append(ress)
    return response

def getByListenId(gid):
    url = "https://www.xiami.com/song/playlist/id/"+ str(gid) +"/object_name/default/object_id/0/cat/json"
    header["referer"] = "https://www.xiami.com/play?ids=/song/playlist/id/"+ str(gid) +"/object_name/default/object_id/0"
    getJson = requests.get(url, verify = True, headers = header)
    songInfo = json.loads(getJson.text)["data"]["trackList"][0]
    res = {}
    res["url"] = "https:" + urlSongDec(songInfo["location"])
    res["text"] = songInfo["songName"] + "-" + songInfo["artist"]
    return res

