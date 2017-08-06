# coding: utf-8
import urllib.request

import bs4


class QSBK(object):
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self, page):
        print('loading page[%d]' % page)
        try:
            url = 'http://www.qiushibaike.com/hot/page/%d' % page
            req = urllib.request.Request(url, headers=self.headers)
            resp = urllib.request.urlopen(req)
            return (resp.read().decode('utf-8'))
        except urllib.request.URLError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)


    def getPageItems(self, page):
        pageContent = bs4.BeautifulSoup(self.getPage(page), 'html.parser')
        pageStories = []

        if not pageContent:
            print("页面加载失败....")
            return None
        items = pageContent.select('div.article')
        for item in items:
            pageStories.append({'Author': self.getAuthor(item),
                                'Content': self.getContent(item),
                                'Vote': self.getVote(item)
                                })
        return pageStories


    def getAuthor(self, item):
        for author in item.select('div.author > a > h2'):
            if author:
                return author.string.replace("\n", "")


    def getContent(self, item):
        contentStr = ''
        for content in item.select('div.content > span'):
            for str_line in content.stripped_strings:
                contentStr = contentStr + '\n' + str_line
        return contentStr


    def getVote(self, item):
        for good in item.select('div.stats > span.stats-vote > i.number'):
            if good:
                return good.string


    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1


    def getOneStory(self, pageStories, page):
        for story in pageStories:
            keyInput = input()
            self.loadPage()
            if keyInput == 'Q':
                self.enable = False
                return
            print('Author: %s' % story['Author'])
            print('Content: %s' % story['Content'])
            print('Vote: %s' % story['Vote'])
            print('--------------------------------')
            print()


    def start(self):
        print(u"正在读取糗事百科,按回车查看新段子，Q退出")
        # 使变量为True，程序可以正常运行
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)


spider = QSBK()
spider.start()

