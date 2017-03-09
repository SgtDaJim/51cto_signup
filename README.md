51cto_signup
====================
自动登录[51CTO](www.51cto.com)，进行签到领取无忧币、领取下载豆等动作。释放碎片时间。
## 依赖
    BeautifulSoup
    lxml
## 安装依赖
    pip install BeautifulSoup4
    pip install lxml
    
windows用户在安装lxml可能会因为缺少C语言库报错<br>
可以选择到[Unofficial Windows Binaries for Python Extension Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/)下载whl文件
例如：<br>
使用python3.5版本<br>
则下载lxml-3.6.4-cp35-cp35m-win_amd64.whl<br>
然后<br>

    pip install wheel
    pip install f:\lxml-3.6.4-cp35-cp35m-win_amd64.whl (你lxml的whl文件的存放目录)
## 用法
    1. 安装依赖。
    2. notepad打开user.ini。
    3. 在LoginInfo项中，
            user=51CTO注册账号
            password=密码
    4. 在EmailInfo项中，
            from=充当发送者的邮箱
            to=充当收件者的邮箱
            authorization=发送者邮箱的smtp授权码
            smtp_server=发送者邮箱的smtp服务器
            smtp_port=smtp服务器端口
    5. 使用python3.x运行51cto_signup.py。
    6. Enjoy.
    
