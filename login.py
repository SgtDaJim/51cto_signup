#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @File       : login.py
# @Time       : 2017/3/7 19:50
# @Author     : Jim
# @GitHub     : https://github.com/SgtDaJim

import urllib.request
import urllib.parse
import http.cookiejar
import json
from bs4 import BeautifulSoup
import configparser
from email_constructor import Email


def build_opener():
    cookie = http.cookiejar.CookieJar()
    cookie_processor = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookie_processor)
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0")]
    urllib.request.install_opener(opener)

def login():

    url = "http://home.51cto.com/index"

    login_data = configparser.ConfigParser()
    login_data.read("user.ini")

    username = login_data.get("LoginInfo", "user")
    password = login_data.get("LoginInfo", "password")

    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "lxml")

    # 获取防伪造参数
    csrf_param = soup.find("meta", attrs={"name": "csrf-param"})["content"]

    # 获取防伪造token
    csrf_token = soup.find("meta", attrs={"name":"csrf-token"})["content"]

    # 构造登录参数
    params = {
        csrf_param : csrf_token,
        "LoginForm[username]": username,
        "LoginForm[password]": password,
        "LoginForm[rememberMe]": "0",
        "login - button": "登录"
    }

    # 参数urlencode
    params = urllib.parse.urlencode(params).encode("utf-8")

    # 模拟登录过程
    request = urllib.request.Request(url, params, method="POST")
    response = urllib.request.urlopen(request)

    # 成功登录后会refresh到home.51cto.com/home，所以此处response无内容。输出下info确认登录情况
    print(response.info())


def get_download_bean():

    url = "http://down.51cto.com/download.php?do=getfreecredits"

    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8")

    data = data.split(",")

    # 邮件信息
    msg = ""

    if data[0] == "0":
        print("下载豆领取失败！！！")
        msg += "下载豆领取失败！！！"
    elif data[0] == "1":
        print("今天已领取！！！已领取" + data[1] + "个下载豆！！！")
        msg += "今天已领取！！！已领取" + data[1] + "个下载豆！！！"
    else:
        print("成功领取" + data[1] +"个下载豆，目前拥有" + data[0] + "个下载豆！")
        msg += "成功领取" + data[1] +"个下载豆，目前拥有" + data[0] + "个下载豆！"

    return msg

def get_wuyou_coins():

    url = "http://home.51cto.com/home"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "lxml")

    # 获取防伪造参数
    csrf_param = soup.find("meta", attrs={"name": "csrf-param"})["content"]

    # 获取防伪造token
    csrf_token = soup.find("meta", attrs={"name":"csrf-token"})["content"]

    # 构造领取无忧币参数
    params = {
        csrf_param: csrf_token,
    }

    # 参数urlencode
    params = urllib.parse.urlencode(params).encode("utf-8")

    # 模拟领取过程
    request = urllib.request.Request(url + "/ajax-to-sign", params, method="POST")
    request.add_header("Connection", "keep-alive")
    request.add_header("Accept", "application/json, text/javascript, */*; q=0.01")
    request.add_header("Origin", "http://home.51cto.com")
    request.add_header("X-CSRF-Token", csrf_token)
    request.add_header("X-Requested-With", "XMLHttpRequest")
    request.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    request.add_header("Referer", "http://home.51cto.com/home")
    response = urllib.request.urlopen(request)

    data = response.read().decode("utf-8")
    data = json.loads(data)

    # 邮件信息
    msg = ""

    # 判断领取状态
    if data["isSignSuccess"] == True:
        print("签到成功，并领取了"+ str(data["signCentToday"]) +"个无忧币！"+"已成功签到"
              + str(data["lastedTimes"]) + "天！现在共拥有" + str(data["wuyoucent"]) +"个无忧币！")
        msg += "签到成功，并领取了"+ str(data["signCentToday"]) +"个无忧币！"+"已成功签到" \
               + str(data["lastedTimes"]) + "天！现在共拥有" + str(data["wuyoucent"]) +"个无忧币！"

    elif data["isSignSuccess"] == False:
        print("签到失败或今天已经签到！")
        msg += "签到失败或今天已经签到！"

    return msg



if __name__ == "__main__":
    build_opener()
    login()

    msg = ""
    msg += get_download_bean()
    msg += "\n"
    msg += get_wuyou_coins()

    # 发送邮件
    email = Email(msg)
    email.send()

    print("运行结束。")
