import os
import json
import urllib.parse as urlParser
import urllib.request as urlReq

try:
    import requests
except:
    os.system('pip install requests')
    import requests


class AudioList:
    def __init__(self, remixsid, owner_id):
        self.headers = {"accept": "*/*",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Accept-Encoding": "gzip, deflate, br",
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                        "x-requested-with": "XMLHttpRequest",
                        "origin": "https://vk.com",
                        "referer": "https://vk.com",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-origin"}

        self.cookie = dict(remixsid=remixsid)
        self.reqSearchParams = dict(act='section', al='1', claim='0', is_layer='1', owner_id=owner_id,
                                    section='search')
        self.reqReloadParams = dict(act='reload_audio', al='1')

        self.list = []

    def search_audio(self, search):
        self.reqSearchParams['q'] = urlParser.quote(search)
        res = requests.post("https://vk.com/al_audio.php", data=urlParser.urlencode(self.reqSearchParams, safe='%/'),
                            headers=self.headers, cookies=self.cookie)
        res = json.loads(res.text)
        buffList = res['payload'][1][1]['playlist']['list']
        self.list = [Audio(audio[4] + ("" if audio[16] == "" else f" ({audio[16]})"), audio[3], audio[5], audio[2], [audio[1], audio[0], audio[13]]) for audio in
                     buffList]
        self.reload_audio()

    def reload_audio(self, num=-1):
        buffList = self.list.copy()
        if num >= 0:
            buffList = [self.list[num]]

        ids = ""
        i = 0
        resList = []
        restrictList = []
        for audio in buffList:
            buffIds = str(audio.ids[2]).split('/')
            buffIds = [i for i in buffIds if i != '']
            if len(buffIds) != 3:
                self.list.remove(audio)
                restrictList.append(audio)
                continue
            ids += str(audio.ids[0]) + '_' + str(audio.ids[1]) + '_' + buffIds[1] + '_' + buffIds[2]
            ids += ','
            i += 1
            if i % 4 == 0 or i == len(buffList) - len(restrictList):
                self.reqReloadParams['ids'] = ids[:-1]
                res = requests.post("https://vk.com/al_audio.php", data=urlParser.urlencode(self.reqReloadParams),
                                    headers=self.headers, cookies=self.cookie)
                ids = ""
                resList.extend(json.loads(res.text)['payload'][1][0])

        for audio in restrictList:
            buffList.remove(audio)

        for i in range(len(buffList)):
            buffList[i].name = resList[i][4] + ("" if resList[i][16] == "" else f" ({resList[i][16]})")
            buffList[i].group = resList[i][3]
            buffList[i].duration = resList[i][5]
            buffList[i].link = resList[i][2]
            buffList[i].ids[0] = resList[i][1]
            buffList[i].ids[1] = resList[i][0]
            buffList[i].ids[2] = resList[i][13]

        self.decode_link()

    def decode_link(self, num=-1):
        buffList = self.list
        if num >= 0:
            buffList = [self.list[num]]

        links = [audio.link + "\n" for audio in buffList]
        with open("buff", "w") as f:
            f.writelines(links)
        os.system("jsdb.exe getUrl.js")
        with open("buff", "r") as f:
            links = f.readlines()
        os.remove("buff")

        for i in range(len(buffList)):
            if links[i].find('.mp3?extra=') == -1:
                index = links[i].find('/index.m3u8')
                links[i] = links[i][:index] + '.mp3' + links[i][index + 11:-1]
                parts = links[i].split('/')
                for j in range(len(parts)):
                    if parts[j].find('.mp3?extra=') != -1:
                        if parts[j - 1] == 'audios':
                            parts.pop(j - 2)
                        else:
                            parts.pop(j - 1)
                        break
                links[i] = ""
                for part in parts:
                    links[i] += part + '/'

            buffList[i].link = links[i][:-1]

    def save(self, filePath):
        with open(filePath, 'w') as f:
            json.dump(self.list, f, cls=AudioEncoder)


class Audio:
    def __init__(self, name, group, duration, link, ids):
        self.name = name
        self.group = group
        self.duration = duration
        self.link = link
        self.ids = ids

    def save_file(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        baseFilePath = os.path.join(path, self.group + ' - ' + self.name)
        filePath = baseFilePath
        i = 1
        while os.path.isfile(filePath + '.mp3'):
            filePath = baseFilePath + f' ({i})'
            i += 1
        filePath += '.mp3'
        urlReq.urlretrieve(self.link, filePath)


class AudioEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Audio):
            return dict(name=o.name, group=o.group, duration=o.duration, link=o.link, ids=o.ids)
        return json.JSONEncoder.default(self, o)
