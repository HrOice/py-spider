from urllib import request
import re
from ParserTool import Tool
import os

img_path = os.path.join(os.path.abspath(os.path.curdir), 'images')

class MM(object):
    def __init__(self, name, age, area, profession, link):
        self.name = name
        self.age = age
        self.area = area
        self.profession = profession
        self.link = link
        self.images = []
        self.detailPage = ''

    def printBaseInfo(self):
        print('name: ', self.name)
        print('age: ', self.age)
        print('profession: ', self.profession)
        print('area: ', self.area)
        print()


    def addImage(self, link):
        self.images.append(link)

    def getImages(self):
        return self.images

    def setDetailPage(self, page):
        self.detailPage = page


    def saveImages(self):
        if len(self.images) > 0:
            pass






class TBMM(object):
    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = Tool()


    def getPage(self, pageNum):
        try:
            url = self.siteURL + '?page=' + str(pageNum)
            req = request.Request(url)
            resp = request.urlopen(req)
            return resp.read().decode('gbk')
        except request.URLError as e:
            if e.reason:
                print('loading page failed: %s' % e.reason)


    def getBaseInfo(self, page):
#pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<p class="top.*?<a class="lady-name.*?href="(.*?)".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>.*?<p>.*?<em>(.*?)</em>', re.S)
        result = re.findall(pattern, page)
        contents = []
        for item in result:
            contents.append(MM(item[2], item[3], item[4], item[5],item[0]))
        return contents


    def getDetailPage(self, url):
        resp = request.urlopen('http:' + url)
        return resp.read().decode('gbk')


#<img style="float: none;margin: 10.0px;" src="//img.alicdn.com/imgextra/i3/687471686/TB1dU0WKXXXXXcBXpXXXXXXXXXX_!!0-tstar.jpg">
    def collectImages(self, mm):
        page = mm.detailPage
        pattern = re.compile('<img.*?src="(.*?)".*?>', re.S)
        result = re.findall(pattern, page)
        for item in result:
            mm.addImage('http:' + item.strip())


    def saveImage(self, uri, path, index):
        try:
            u = request.urlopen(uri)
            fileName = os.path.join(path, index + '.jpg')
            data = u.read()
            f = open(fileName, 'wb')
            f.write(data)
            f.close()
        except request.URLError as e:
            print('get img %s failed, cause: %s', uri, e.reason)

    def saveImages(self, mm, path):
        index = 1
        for imgUrl in mm.getImages():
            self.saveImage(imgUrl, path, 'mm' + str(index))
            index += 1



    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print(u'create dir: ', path)
            os.makedirs(path)
            return True
        else:
            return False


    def start(self, start, end):
        for pageNum in range(start, end + 1):
            page = self.getPage(pageNum)
            mms = self.getBaseInfo(page)
            for mm in mms:
                mm.printBaseInfo()
                detailPage = self.getDetailPage(mm.link)
                mm.setDetailPage(detailPage)
                self.collectImages(mm)
                dirPath = os.path.join(img_path, mm.name)
                self.mkdir(dirPath)
                self.saveImages(mm, dirPath)







tbmm = TBMM()
tbmm.start(1,1)
# page = tbmm.getPage(1)


# mms = tbmm.getBaseInfo(page)
# for item in mms:
#     item.printBaseInfo()