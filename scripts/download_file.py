import requests


"""
Summary:

一个下载文件的小脚本，三行代码
可以下载网站js文件，再配合diff，轻松实现js文件变化监控。
"""

url = 'https://download.sysinternals.com/files/PSTools.zip'
r = requests.get(url, allow_redirects=True)
open('PSTools.zip', 'wb').write(r.content)
