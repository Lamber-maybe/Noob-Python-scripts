# Noob-Python-scripts
A collection of clever Python scripts for daily use

# 使用说明
请将脚本放到 `scripts` 目录

脚本里面一定要携带如下格式的注释信息

```
"""
Summary:

"""
```

该注释信息里面用于描述脚本的功能和用法。并且README会自动提取该摘要信息。

# 现有脚本清单如下
## [download_file.py](/scripts/download_file.py)
```
一个下载文件的小脚本，三行代码
可以下载网站js文件，再配合diff，轻松实现js文件变化监控。
```
## [calc_current_dir_size.py](/scripts/calc_current_dir_size.py)
```
计算该脚本所在目录，所占用的存储空间大小
使用方法:
python3 calc_current_dir_size.py
```
## [Del-repeat-url.py](/scripts/Del-repeat-url.py)
```
当从测绘中导出大量url时，可能会存在一个主域名有很多无用子域名的情况，该脚本会对同一个主域名保留前十个子域名，其他的删除
```
