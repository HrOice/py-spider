import urllib.request
import re

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

class BDTB(object):
    def __init__(self, baseUrl, seeLz):
        self.baseUrl = baseUrl
        self.seeLz = '?see_lz='+str(seeLz)
        self.page = ''


    def getPage(self, pageNum):
        try:
            url = self.baseUrl+ self.seeLz + '&pn=' + str(pageNum)
            req = urllib.request.Request(url)
            resp = urllib.request.urlopen(req)
            # print(resp.read())
            content = resp.read().decode('utf-8')
            # print(content)
            self.page = content
            return content
        except urllib.request.URLError as e:
            if hasattr(e, "reason"):
                print(u"连接百度贴吧失败,错误原因", e.reason)
                return None



#<h3 class="core_title_txt pull-left text-overflow  " title="纯原创我心中的NBA2014-2015赛季现役50大" style="width: 396px">纯原创我心中的NBA2014-2015赛季现役50大</h3>
    def getTitle(self):
        page = self.page
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            # print result.group(1)  #测试输出
            return result.group(1).strip()
        else:
            return None

#<li class="l_reply_num" style="margin-left:8px"><span class="red" style="margin-right:3px">141</span>回复贴，共<span class="red">5</span>页</li>
    def getPageCount(self):
        page = self.page
        pattern = re.compile('<li class="l_reply_num.*?<span.*?<span.*?>(.*?)</span>')
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getContent(self, page):
        tool = Tool()
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        floor = 1
        for item in items:
            print(floor, u'楼--------------------------')
            print(tool.replace(item))
            print()
            floor +=1

baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL,1)
bdtb.getPage(1)
print(bdtb.getTitle())
print(bdtb.getPageCount())
bdtb.getContent(bdtb.page)