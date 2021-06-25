# -*- codeing = utf-8 -*-
# @Author :$杨致远
# @Time :2021/2/3 16:39
# @File :finance.py
# @software: PyCharm
# 1.成功爬取所有的html网页，并且对前两个html解析拿到了新闻和公告，后续只需要添加每个网站的getData(i)方法并将函数放入getData列表
# 2.完成getData2-getData(4) getData3公告需要爬取新的网页才能得到
# 3.增加无界面浏览器的形式获取cookie方法get_cookie，增加askURLStrengthen方法：封装cookie模拟浏览器访问 云南财经大学、首都经济贸易大学
# 4.设置excel表格列宽度和超链接
# 5.学习Selenium+PhantomJS爬取动态网页尝试获取完整 首都经济贸易大学 网页源码

# 设置了保存的excel的列宽


import re
import xlwt  # 进行excel操作
import urllib
import datetime  # 获取当前年份，要闻或者公告只提供月日日期，需要加上年份
import pickle  # 保存html文件
from bs4 import BeautifulSoup  # 网页解析，获取数据
from selenium import webdriver
import urllib.request, urllib.error  # 指定url，获取网页数据

finance_url = [
    "http://www.cufe.edu.cn/",  # 中央财经大学
    "http://www.nufe.edu.cn/",  # 南京财经大学（教务处# http://jwc.nufe.edu.cn/）
    "http://www.jxufe.edu.cn/",  # 江西财经大学
    "https://www.sdufe.edu.cn/",  # 山东财经大学
    "http://www.shufe.edu.cn/",  # 上海财经大学------对方服务器有一定几率会炸
    "https://www.zuel.edu.cn/",  # 中南财经政法大学
    "http://www.btbu.edu.cn/",  # 北京工商大学
    "http://www.sxufe.edu.cn/",  # 山西财经大学
    "http://www.dufe.edu.cn/",  # 东北财经大学
    "http://www.tjufe.edu.cn/",  # 天津财经大学
    "https://www.heuet.edu.cn/",  # 河北经贸大学
    "https://www.swufe.edu.cn/",  # 西南财经大学
    "https://www.ctbu.edu.cn/",  # 重庆财经工商大学
    "http://www.uibe.edu.cn/",  # 对外经济贸易大学
    "https://www.hrbcu.edu.cn/",  # 哈尔滨商业大学
    "https://www.tjcu.edu.cn/",  # 天津商业大学
    "https://www.zufe.edu.cn/",  # 浙江财经大学
    "http://news.zjgsu.edu.cn/18/",
    # 浙江工商大学---------首页(http://www.hzic.edu.cn/)有反爬虫机制并且已经失效（status 404)|给成公告页面url：http://news.zjgsu.edu.cn/18/
    "http://www.ynufe.edu.cn/index1024.htm",
    # "http://www.ynufe.edu.cn/",  # 云南财经大学---------使用浏览器也无法访问url 换url--->http://www.ynufe.edu.cn/index1024.htm
    # 要闻：http://www.ynufe.edu.cn/xwzx/index.htm  公告：http://www.ynufe.edu.cn/xwzx/ybdt/index.htm
    "https://www.cueb.edu.cn/"  # 首都经济贸易大学---------有反爬虫机制（status 202 accepted）
]

finance_name = [
    "中央财经大学",
    "南京财经大学",
    "江西财经大学",
    "山东财经大学",
    "上海财经大学",
    "中南财经政法大学",  # 解析得到的要闻链接不安全，不能正常访问(校园网应该可以)---已解决
    "北京工商大学",  # 有时候爬取不到网页源码
    "山西财经大学",
    "东北财经大学",
    "天津财经大学",
    "河北经贸大学",
    "西南财经大学",
    "重庆财经工商大学",  # 解析得到的要闻、公告链接不安全，不能正常访问(校园网应该可以)---已解决
    "对外经济贸易大学",
    "哈尔滨商业大学",
    "天津商业大学",
    "浙江财经大学",
    "浙江工商大学",
    "云南财经大学",
    "首都经济贸易大学"  # 网络状态码202，爬取不到源码---已解决，但是源码爬取不完整，需要学习爬取动态网页知识
]
status = 404
Row = 0
getData = []  # getData函数列表
excel_savepath = "financeNewsAffiche.xls"
remainder = 2
timeout = 2


def main():
    global Row
    datalist = []  # 所有网站的公告、新闻列表[公告(字典)，新闻]
    finance_html = []  # 所有网站的html源码
    # 先进行html网页源码爬取
    # 爬取前18个
    for i in range(0, len(finance_url) - remainder):
        html = askURL(finance_url[i])
        print(i, finance_name[i], status)
        # if 6 == i:
        #     html = bytes(html).decoding("utf-8")
        if 200 != status:
            finance_html.append(" ")
        else:
            finance_html.append(html)

    # 封装cookie获取最后remainder个网页源码(反反爬虫)
    heads = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }
    for i in range(len(finance_url) - remainder, len(finance_url)):
        cookie = get_cookie(finance_url[i])
        heads['Cookie'] = cookie
        # heads['Cookie'] = cookies[i-len(finance_url)+remainder]

        html = askURLStrengthen(finance_url[i], heads)
        print(i, finance_name[i], status)

        if 200 != status:
            finance_html.append(" ")
        else:
            finance_html.append(html)

    # 保存每个网页源码
    # for i in range(0, len(finance_url)):
    # pickle.dump(finance_html[i], open(str(i)+finance_name[i]+".html", 'wb'))

    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # style_compression：压缩的效果
    sheet = book.add_sheet("sheet1", cell_overwrite_ok=True)  # 单元格内容可覆盖
    # 设置excel列宽
    first_col = sheet.col(0)
    first_col.width = 256 * 20  # 设置A列宽度30
    sec_col = sheet.col(1)
    sec_col.width = 256 * 100
    thi_col = sheet.col(2)
    thi_col.width = 256 * 100

    # 内容解析
    for i in range(len(finance_html)):  #
        data = getData[i](finance_html[i])
        datalist.append(data)
        # 保存进excel
        sheet.write(Row, 0, finance_name[i])

        col = ("公告", "要闻")  # 元组添加表头
        for j in range(1, len(col) + 1):  # 写入表头(列名)
            sheet.write(Row + 0, j, col[j - 1])
        Row += 1

        affiche = data[0]  # 公告
        news = data[1]  # 新闻
        for j in range(len(affiche)):
            # sheet.write(Row + j, 1, list(affiche.keys())[j])
            # sheet.write(Row + j, 2, list(affiche.values())[j])
            sheet.write(Row + j, 1,
                        xlwt.Formula('HYPERLINK("{}","{}")'.format(list(affiche.values())[j], list(affiche.keys())[j])))
        for j in range(len(news)):
            # sheet.write(Row + j, 3, list(news.keys())[j])
            # sheet.write(Row + j, 4, list(news.values())[j])
            sheet.write(Row + j, 2,
                        xlwt.Formula('HYPERLINK("{}","{}")'.format(list(news.values())[j], list(news.keys())[j])))
        Row += len(affiche) if len(affiche) > len(news) else len(news)
    a = datetime.datetime.now()  # 得到当前时间
    book.save(a.strftime("%Y-%m-%d-%H-%M-%S_") + excel_savepath)
    # 除了保存为excel考虑使用Flask框架在数据可视化方面更加友好，excel可以作为数据备份


# 得到执行url的网页信息（增加超时机制）
def askURL(url):
    global status
    # 头部信息 其中用户代理用于伪装浏览器访问网页
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36"}
    req = urllib.request.Request(url, headers=head)
    html = ""  # 获取到的网页源码
    try:
        response = urllib.request.urlopen(req, timeout=timeout)
        html = response.read().decode("utf-8")
        status = response.status
    except urllib.error.URLError as e:
        if hasattr(e, "code"):  # has attribute
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 得到执行url的网页信息方法改进版（增加超时机制）
def askURLStrengthen(url, head={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.88 Safari/537.36"}):
    global status
    # 头部信息 其中用户代理用于伪装浏览器访问网页

    req = urllib.request.Request(url, headers=head)
    html = ""  # 获取到的网页源码
    try:
        response = urllib.request.urlopen(req, timeout=timeout)
        html = response.read().decode("utf-8")
        status = response.status
    except urllib.error.URLError as e:
        if hasattr(e, "code"):  # has attribute
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


"""
# 使用CookieJar获取cookie值
def get_cookie(url):
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3427.400 QQBrowser/9.6.12513.400'
    }

    cookie = cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    opener.addheaders = [('User-Agent', 'Mozilla/5.0(Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3427.400 QQBrowser/9.6.12513.400')]
    resp = opener.open(url)

    cookieStr = ''
    for item in cookie:
        cookieStr = cookieStr + item.name + '=' + item.value + ';'
    return cookieStr
"""


# 利用selenium+phantomjs无界面浏览器的形式访问网站，再获取cookie值
def get_cookie(url):
    # 创建浏览器对象
    driver = webdriver.PhantomJS()
    # 打开页面
    driver.get(url)
    # 获取cookie列表
    cookie_list = driver.get_cookies()
    # 格式化打印cookie
    # print(cookie_list)
    cookieStr = ''
    for cookie in cookie_list:
        cookieStr = cookieStr + cookie['name'] + "=" + cookie['value'] + ';'
    return cookieStr


def replaceAll(str):  # 替换所有空格、回车、换行符
    str = str.replace("\r", "")
    str = str.replace("\n", "")
    str = str.replace(" ", "")
    return str


# 中央财经大学
# getData0正则表达式模式对象
ul_xxywList_a_href0 = re.compile('<a href="(.*?)" target="_blank" title=".*?">.*?</a>')  # 最终正则表达式得到的结果就是(.*?)代表的东西
ul_xxywList_a_title0 = re.compile('<a href=".*?" target="_blank" title="(.*?)">.*?</a>')
div_gg_a_href0 = re.compile('<a class="fl" href="(.*?)" title=".*?"><b>.*?</b></a>')
div_gg_a_title0 = re.compile('<a class="fl" href=".*?" title="(.*?)"><b>.*?</b></a>')  # <a.*?title="(.*?)".*?</a>


def getData0(html):  # 解析数据
    soup = BeautifulSoup(html, "html.parser")  # 使用html.parser解析器解析html文档形成树形结构数据
    affiche = {}  # 公告
    news = {}  # 新闻

    # 要闻位于class=xxywList的ul中
    ul_xxywList = soup.select("ul[class='xxywList']")
    ul_xxywList = str(ul_xxywList)
    news_url = re.findall(ul_xxywList_a_href0, ul_xxywList)
    news_title = re.findall(ul_xxywList_a_title0, ul_xxywList)

    for i in range(len(news_url)):
        news[news_title[i]] = news_url[i]
    # print(news)

    # 公告位于class=gg的div中
    # 每个新获取的url需要前缀添加："http://www.cufe.edu.cn/"
    div_gg = soup.select("div[class='gg']")
    div_gg = str(div_gg)
    affiche_url = re.findall(div_gg_a_href0, div_gg)
    affiche_title = re.findall(div_gg_a_title0, div_gg)
    for i in range(len(affiche_url)):
        affiche[affiche_title[i]] = "http://www.cufe.edu.cn/" + affiche_url[i]
    # print(affiche)
    return [affiche, news]


getData.append(getData0)

# 南京财经大学
# getData1正则表达式模式对象
div_frhomegonggao_a_href1 = re.compile('<a class="fl" href="(.*?)">.*?</a>')
div_frhomegonggao_a_title1 = re.compile('<a class="fl" href=".*?">(.*?)</a>')
div_swiper_wrapper_a_href1 = re.compile('<a href="(.*?)">.*?</a>')
div_swiper_wrapper_a_title1 = re.compile('<a href=".*?">(.*?)</a>')


def getData1(html):  # 解析数据
    soup = BeautifulSoup(html, "html.parser")  # 使用html.parser解析器解析html文档形成树形结构数据
    affiche = {}  # 公告
    news = {}  # 新闻

    # 要闻位于class="frhome-gonggao"的div中
    div_frhomegonggao = soup.select("div[class='fr home-gonggao']")
    div_frhomegonggao = str(div_frhomegonggao)
    news_url = re.findall(div_frhomegonggao_a_href1, div_frhomegonggao)
    news_title = re.findall(div_frhomegonggao_a_title1, div_frhomegonggao)

    # 每个新获取的url需要前缀添加："http://www.nufe.edu.cn/"
    for i in range(len(news_url)):
        news[news_title[i]] = "http://www.nufe.edu.cn/" + news_url[i]
    # print(news)

    # 公告位于class="parBd"的div中的第一个class="swiper-wrapper"的div中

    div_swiper_wrapper = soup.body.select("div[class='swiper-wrapper']")
    div_swiper_wrapper = str(div_swiper_wrapper[0])
    affiche_url = re.findall(div_swiper_wrapper_a_href1, div_swiper_wrapper)
    affiche_title = re.findall(div_swiper_wrapper_a_title1, div_swiper_wrapper)
    for i in range(len(affiche_url)):
        affiche[affiche_title[i]] = "http://www.nufe.edu.cn/" + affiche_url[i]
    # print(affiche)
    return [affiche, news]


getData.append(getData1)

# 江西财经大学
# getData2正则表达式模式对象
ul_ul2_a_href2 = re.compile('<a href="(.*?)" target="_blank">.*?</a>', re.S)
ul_ul2_a_title2 = re.compile('<p>(.*?)</p>')
ul_ul2_a_title_time2 = re.compile('<span>(.*?)</span>')
ul_two_leftrl_a_href2 = re.compile('<a href="(.*?)" target="_blank">.*?</a>')
ul_two_leftrl_a_title2 = re.compile('<a href=".*?" target="_blank">(.*?)</a>')
ul_two_leftrl_a_title_time2 = re.compile('<span style="float:right; color:#999999; font-size:12px;">(.*?)</span>')


def getData2(html):  # 解析数据
    soup = BeautifulSoup(html, "html.parser")  # 使用html.parser解析器解析html文档形成树形结构数据
    affiche = {}  # 公告
    news = {}  # 新闻
    # 要闻位于class="ul2"的ul中
    ul_ul2 = soup.select("ul[class='ul2']")
    ul_ul2 = str(ul_ul2)
    news_url = re.findall(ul_ul2_a_href2, ul_ul2)
    news_title = re.findall(ul_ul2_a_title2, ul_ul2)
    news_time = re.findall(ul_ul2_a_title_time2, ul_ul2)
    for i in range(len(news_url)):
        news[news_title[i] + "----" + news_time[i]] = news_url[i]

    # 公告太长通过主页无法爬取，需要通过url:http://news.jxufe.edu.cn/news-list-xinxigonggao.html爬取
    html_affiche = askURL("http://news.jxufe.edu.cn/news-list-xinxigonggao.html")
    soup = BeautifulSoup(html_affiche, "html.parser")
    ul_two_leftrl = soup.select("div[class='two_leftrl']")
    ul_two_leftrl = str(ul_two_leftrl)
    affiche_url = re.findall(ul_two_leftrl_a_href2, ul_two_leftrl)
    affiche_title = re.findall(ul_two_leftrl_a_title2, ul_two_leftrl)
    affiche_time = re.findall(ul_two_leftrl_a_title_time2, ul_two_leftrl)
    for i in range(len(affiche_url)):
        affiche[affiche_title[i] + "----" + affiche_time[i]] = affiche_url[i]
    return [affiche, news]


getData.append(getData2)

# 山东财经大学
# getData3正则表达式模式对象
news_url_a_href3 = re.compile('<a href="(.*?)" target="_blank" title=".*?">.*?</a>')
news_url_a_title3 = re.compile('<a href=".*?" target="_blank" title="(.*?)">.*?</a>')
news_url_a_title_time3 = re.compile('<span class="gray-3 fr">(.*?)</span>')
ul_style_affiche_a_href3 = re.compile('<a href="(.*?)" target="_blank" title=".*?">')
ul_style_affiche_a_title3 = re.compile('<a href=".*?" target="_blank" title="(.*?)">')
ul_style_affiche_a_title_time3 = re.compile('<span class="gray-3 fr">(.*?)</span>')


def getData3(html):  # 解析数据
    soup = BeautifulSoup(html, "html.parser")  # 使用html.parser解析器解析html文档形成树形结构数据
    affiche = {}  # 公告
    news = {}  # 新闻