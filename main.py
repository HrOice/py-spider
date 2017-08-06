import urllib.request
import re
import bs4

page = 1
url = 'http://www.qiushibaike.com/hot/page/%d' % page
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}

pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class' +
                     '="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)


def get_html_doc(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        return (resp.read().decode('utf-8'))
    except urllib.request.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)


def printContent(str_gen):
    print('Content: ')
    for s in str_gen:
        print(s, '\n')


html_doc = get_html_doc(url)

soup = bs4.BeautifulSoup(html_doc, 'html.parser')
items = soup.select('div.article')

# items = re.findall(pattern, html_doc)
for item in items:
    print('-------------------')
    [print('Auth: %s' % author.string) for author in item.select('div.author > a > h2')]
    [printContent(content.stripped_strings) for content in item.select('div.content > span')]
    [print('Good: %s' % good.string) for good in item.select('div.stats > span.stats-vote > i.number')]
