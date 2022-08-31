from ast import Try
from multiprocessing.util import info
import sys
from geopy.geocoders import Nominatim
import geoip2.database
import requests
import json
import re


def LL_2_Maidenhead(float_Longitude, float_Latitude):  # 将！经纬度转换成！梅登黑德定位代码
    a = float_Longitude/20 + 9
    b = int(a)
    str_maid = chr(b + 65)
    c = float_Latitude/10 + 9
    d = int(c)
    str_maid = str_maid + chr(d + 65)
    a = (a-b) * 10
    b = int(a)
    str_maid = str_maid + chr(b + 48)
    c = (c-d) * 10
    d = int(c)
    str_maid = str_maid + chr(d + 48)
    a = (a-b) * 24
    b = int(a)
    str_maid = str_maid + chr(b + 65)
    c = (c-d) * 24
    d = int(c)
    str_maid = str_maid + chr(d + 65)
    return str_maid


def getLogitudeAndLatitude(ip):
    reader = geoip2.database.Reader('./GeoLite2-City.mmdb')
    response = reader.city(ip)
    try:
        cityName = str(response.city.names["zh-CN"])
    except:
        cityName = str(response.city.name)
    geolocator = Nominatim(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36")  # 放ua
    location = geolocator.geocode(cityName)
    return location.longitude, location.latitude, location.address


def getIp():
    return json.loads(requests.get('https://api.ipify.org/?format=json').text)['ip']


def miniSetup():
    Longitude = input("请输入你所在地的经度")
    Latitube = input("请输入你所在地的纬度")
    print("在你的经纬度输入正确的前提下,你的Maidenhead代码为:" +
          LL_2_Maidenhead(float(Longitude), float(Latitube)))


def main(ip, typei):
    if(typei == 0):
        ip = re.sub("\n", "", getIp())
    Ll2D = getLogitudeAndLatitude(ip)
    return ip, Ll2D


if input("是否要进行轻量化启动？ y/n") != "y":
    Info01 = main(0, 0)
    print("如果你的地址是"+Info01[1][2]+"的话,那么你的Maidenhead代码大概为:" +
          LL_2_Maidenhead(Info01[1][0], Info01[1][1])+"如果不是,请输入1")
    if(input() != str(1)):
        print("程序退出")
        sys.exit()
    else:
        miniSetup()
else:
    miniSetup()

input('任意键退出(指键盘上的任意字母键,说不定电源键也可以？)')
# print(getLogitudeAndLatitude("112.74.207.96"))
# print(LL_2_Maidenhead(117.988929, 36.63561))
