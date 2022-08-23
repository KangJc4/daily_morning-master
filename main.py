
import json
import re
import math
from datetime import datetime, date

from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ.get('START_DATE' , '2020-10-08')
city = os.environ.get('CITY', '北京')
birthday2 = os.environ.get('BIRTHDAY' , '10-18')
birthday1 = os.environ.get('BIRTHDAY' , '01-17')

app_id = os.environ.get("APP_ID",'wx722fb8bef9b6c6c7')
app_secret = os.environ.get("APP_SECRET",'90bef06649d2fee4249d58805c7344f6')

user_id = os.environ.get("USER_ID",'oLd7450av29GnW10LqklCxNOccqA')
#模板id
template_id = os.environ.get("TEMPLATE_ID",'BVj3FpyntgUYnlfgJ_xhIJjCY1p5V8rjQxbrXI0CFHE')
meiriyiju = os.environ.get("MEIRIYIJU","每日一句")
# start_date = os.environ['START_DATE']
# city = os.environ['CITY']
# birthday = os.environ['BIRTHDAY']
#
# app_id = os.environ["APP_ID"]
# app_secret = os.environ["APP_SECRET"]
#
# user_id = os.environ["USER_ID"]
# template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

#计算在一起多久了
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

#计算女朋友生日时间
def get_birthday1():
  next = datetime.strptime(str(date.today().year) + "-" + birthday1, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

#计算男朋友生日时间
def get_birthday2():
  next = datetime.strptime(str(date.today().year) + "-" + birthday2, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

#每日一句话
def getDailySentence():
    """
    Get  AiCiBa Daily Sentence
    return: String English + Chinese
    """
    url = 'http://open.iciba.com/dsapi/'
    r = requests.get(url)
    all = json.loads(r.text)
    Englis = all['content']
    Chinese = all['note']
    daily_sentence = '\n@每日壹句:' + '\n' + Englis + '\n' + Chinese + '\n'
    print(daily_sentence)
    return daily_sentence
#获取当前时间
def getDate():

    week_day = {
        1: '星期一',
        2: '星期二',
        3: '星期三',
        4: '星期四',
        5: '星期五',
        6: '星期六',
        7: '星期日',
    }

    # 获取阳历和阴历
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day



    print_date = str(year) + "年" + str(month) + \
        "月" + str(day) + "日"

    var = datetime.isoweekday(datetime.now())

    print_week = "今天是" + week_day[var]

    calendar = '日期：' + print_date + ', ' + print_week + '\n'
    print(calendar)
    return calendar




location = "http://www.weather.com.cn/weather/101220601.shtml"

headers = {
  'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
#天气情况
def getInfo(location):
    """
    Get More Weather Information.
    Arguments:
        location {String} -- location html

    Returns:
        String -- Information
    """
    response = requests.get(location,headers)
    content = response.content.decode("utf-8")
    aim = re.findall(
      r'<input type="hidden" id="hidden_title" value="(.*?)月(.*?)日(.*?)时(.*?) (.*?)  (.*?)  (.*?)"', content)
    airdata = re.findall(
      r'<li class="li16">\n<i></i>\n<span>(.*?)</span>\n<em>(.*?)</em>\n<p>(.*?)</p>\n</li>', content)
    ult_index = re.findall(
      r'<li class="li1">\n<i></i>\n<span>(.*?)</span>\n<em>(.*?)</em>\n<p>(.*?)</p>\n</li>', content)
    cloth_index = re.findall(
      r'<li class="li3 hot" id="chuanyi">\n<a href="javascript:void(0)">\n<div class="pageflip">\n<img src="http://i.tq121.com.cn/i/weather2015/png/page_flip.png">\n<div class="msg_block">/n</div>\n</div>\n<i></i>\n<span>(.*?)</span>\n<em>(.*?)</em>\n<p>(.*?)</p>\n</a>\n</li>', content)
    wash_index = re.findall(r'<li class="li4">\n<i></i>\n<span>(.*?)</span>\n<em>(.*?)</em>\n<p>(.*?)</p>', content)
    lose_index = re.findall(
      r'<span></span>\n<em>(.*?)</em>\n<p>(.*?)</p>\n</a>\n</li>\n<li class="li5">', content)
    # print(lose_index)
    txt1 = '\n' + '@康氏天气预报:' + '\n'
    txt2 = '安庆市天气情况: ' + aim[0][5] + '\n' + '温度情况: ' + aim[0][6] + '\n'
    # txt3 = '穿衣指数: ' + cloth_index[0][0] + ', ' + cloth_index[0][1] + '\n'
    # txt4 = '运动指数：' + lose_index[0][1] + '\n'
    txt5 = '过敏指数: ' + airdata[0][0] + ', ' + airdata[0][2] + '\n'
    txt6 = '紫外线指数: ' + ult_index[0][0] + ', ' + ult_index[0][2] + '\n'

    # txt7 = '洗车指数: '+wash_index[0][0]+', '+wash_index[0][2]+'\n'

    more_information = '\n' + txt1 + txt2 + txt5 + txt6
    print(more_information)
    return more_information


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = { "caihongpi":{"value":get_words()}, "date":{"value":getDate()}, "meiriyiju":{"value":getDailySentence()},"temperature":{"value":temperature},"love_day":{"value":get_count()},"birthday1":{"value":get_birthday1()},"birthday2":{"value":get_birthday2()},"words":{"value":get_words(), "color":get_random_color()},"tianqi":{"value":getInfo(location)}}
res = wm.send_template(user_id, template_id, data)
print(get_random_color())
print(res)





