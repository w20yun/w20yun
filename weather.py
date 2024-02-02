# _*_ coding: utf-8 _*_
"""
Time:     2024/1/13 14:49
Author:   11111
Version:  V 0.1
File:     weather.py
Describe: 
"""
import requests
import json
import re
from lxml import etree
import datetime

city_dic = {}
text_mw = input('请输入查询的城市：')
text_id = str(text_mw.encode('utf-8')).upper().replace('\\X', '%')[2:-1]  # 将中文转置为字符
# print('text_id',text_id)
id_url = 'https://j.i8tq.com/weather2020/search/city.js'
url = 'http://toy1.weather.com.cn/search?cityname=' + text_id
headers = {'Referer': 'http://www.weather.com.cn/',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/120.0.0.0 Safari/537.36',
           'Cookie': 'f_city=%E6%B7%B1%E5%9C%B3%7C101280601%7C; Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1705048649,'
                     '1705652961,1705724650,1706691853; Hm_lpvt_080dabacb001ad3dc8b9b9049b36d43b=1706692058'
           }
# 获取当前时间
current_time = datetime.datetime.now()


def get_area_id():
    areas = requests.get(url=id_url, headers=headers)
    if areas.status_code == 200:
        areas.encoding = 'utf-8'
        # print(areas.text)
        # 使用正则表达式,匹配地区名称和地区ID
        matches = re.findall(r'"AREAID":\s*"(\d+)"\s*,\s*"NAMECN":\s*"([\u4e00-\u9fa5]+)"', areas.text)
        # 将匹配结果转换为字典
        result = {match[1]: match[0] for match in matches}
        # 保存匹配结果到json文件
        with open("D:\Programs\python_file/area_id.json", 'W', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        return "请到 data/area_id.json 文件里查看地区id"
    else:
        return "地区id信息爬取失败..."


def weather_7day():
    resp = requests.get(url=url, headers=headers)
    # print(resp.status_code)  #请求状态码
    # print(resp.text)
    data = resp.text[1:-1]
    json_data = json.loads(data)[0]['ref'][0:9]
    city_url7 = 'http://www.weather.com.cn/weather/' + json_data + '.shtml'
    # print(city_url7)
    city_resp = requests.get(url=city_url7, headers=headers)
    city_resp.encoding = city_resp.apparent_encoding
    html = etree.HTML(city_resp.text)
    node_all7 = html.xpath('//ul[@class="t clearfix"]/li')
    # print('节点名称',[i.tag for i in node_all])
    for node in node_all7:
        day_text = node.xpath('.//h1/text()')
        wea_text = node.xpath('.//p[@class="wea"]/text()')
        tem_text = node.xpath('.//p[@class="tem"]//text()')
        for tem in tem_text:
            if tem in ('/', '\n'):
                tem_text.remove(tem)
        win_text = node.xpath('.//p[@class="win"]//text()')
        for win in win_text:
            if win in ('/', '\n'):
                win_text.remove(win)
        return text_mw, json_data, day_text, wea_text, type(tem_text), tem_text, win_text


def weather_day():
    resp = requests.get(url=url, headers=headers)
    # print(resp.status_code)  #请求状态码
    data = resp.text[1:-1]
    # json_data1 = json.loads(data)[1]
    json_data = json.loads(data)[0]['ref'][0:9]
    # print(json_data)   #获取城市对应编码
    ull_day = 'http://d1.weather.com.cn/dingzhi/' + json_data + '.html?_=1706703751807'
    resp2 = requests.get(url=ull_day, headers=headers)
    resp2.encoding = 'utf-8'
    json_resp2 = resp2.text[21:-31]
    # dict_date = json.loads(json_resp2)
    print(json_resp2)
    # dict_date1 = dict_date['weatherinfo']
    # return dict_date1


def weather_1day():
    # low_temp =Weather_day()['temp']
    # High_temp = Weather_day()['tempn']
    resp = requests.get(url=url, headers=headers)
    # print(resp.status_code)  #请求状态码
    data = resp.text[1:-1]
    # json_data1 = json.loads(data)[1]
    json_data = json.loads(data)[0]['ref'][0:9]
    # print(json_data)   #获取城市对应编码
    weather1_url = 'http://d1.weather.com.cn/sk_2d/' + json_data + '.html?_=1706693282176'  #
    resp2 = requests.get(url=weather1_url, headers=headers)
    resp2.encoding = 'utf-8'
    json_resp2 = resp2.text[11:]
    dict_date = json.loads(json_resp2)
    print(
        '当前时间:', current_time.now().strftime("%Y-%m-%d %H:%M:%S"), '\n'  # 获取当前年月日时分秒
        # "更新时间:", dict_date["date"], dict_date['time'], '\n'
        '当前城市:', dict_date["cityname"], '\n'
        # "城市编码:", dict_date["city"], '\n'
        # '今天温度:', low_temp+' ~ '+High_temp, '\n'
        "当前温度:", dict_date["temp"] + ' ℃', '\n'
        "风向等级:", dict_date["WD"], dict_date["WS"], "\n"
        "湿度:", dict_date["SD"], "\n"
        "天气:", dict_date["weather"], '\n'
        'PM2.5:', dict_date['aqi_pm25'], "\n"
    )


if __name__ == '__main__':
    weather_1day()
