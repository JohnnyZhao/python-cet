# -*- coding: utf-8 -*-
import urllib
import urllib2
import re

def get_score_page(name, ticket_num):
    data = {'xm': name.encode('utf8'), 'zkzh': ticket_num.encode('utf8')}
    url = 'http://www.chsi.com.cn/cet/query?' + urllib.urlencode(data)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                              AppleWebKit/537.36 (KHTML, like Gecko) \
                              Chrome/40 Safari/537.36',
               'Host': 'www.chsi.com.cn',
               'Referer': 'http://www.chsi.com.cn/cet/',
               'Upgrade-Insecure-Requests': '1',
               'X-FirePHP-Version': '0.0.6',
               'Connection': 'keep-alive'}
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    return response.read()

def parse_html(html):
    keys = {
            u'姓名': 'name',
            u'学校': 'school',
            u'考试类别': 'exam_type',
            u'准考证号': 'ticket_num',
            u'考试时间': 'exam_time',
            u'总分': 'grade',
            u'听力': 'listening',
            u'阅读': 'reading',
            u'写作与翻译': 'writing',
    }
    table = re.findall(r"<table(.*?)</table", html, re.S)
    td = re.findall(r">(.*?)<", table[1], re.S)
    score_list = []
    for x in td:
        x = x.strip().rstrip('：')
        if x:
            score_list.append(x.decode('utf8'))
    data = {}
    try:
        for x in xrange(0, 17, 2):
            if x%2 == 0:
                data[keys[score_list[x]]] = score_list[x+1]
    except IndexError, e:
        print "Sorry, no data received"
    return data

def get_score(name, ticket_num):
    try:
        html = get_score_page(name, ticket_num)
        score = parse_html(html)
        if len(score) == 9:
            return score
        return "error"
    except:
        return "error"
