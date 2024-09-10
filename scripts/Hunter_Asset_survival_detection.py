import requests
import openpyxl
import base64
import time
from tqdm import tqdm  # 导入tqdm模块

"""
Summary:
通过Hunter快速确认大批量公司是否有资产存活
domain.txt中应为完整的搜索语法，如：icp.name="xxxx公司"，每行一个
为了节约积分，每行语法只获取一条数据，可自行修改page&page_size,但是不建议大量获取，默认会返回存货资产的页面信息
可以自行修改start_time和end_time来进行时间范围的筛选
"""

# API密钥，你需要将其替换为实际的API密钥
api_key = '你的API'

# 读取domain.txt文件中的原始域名
with open('domain.txt', 'r', encoding='utf-8') as file:
    domains = [line.strip() for line in file]

# 设置每秒最大请求数
requests_per_second = 1

# 创建一个新的Excel工作簿
wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Search Results'
# 设置表头
ws.append(['Search', 'Response'])

# 使用tqdm创建进度条
for domain in tqdm(domains, desc="Processing"):
    # 对域名进行URL安全的base64编码
    encoded_domain = base64.urlsafe_b64encode(domain.encode('utf-8')).decode('utf-8')
    url = f"https://hunter.qianxin.com/openApi/search?api-key={api_key}&search={encoded_domain}&page=1&page_size=1&is_web=1&start_time=2024-01-01&end_time=2024-09-01"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果响应状态码不是200，将抛出HTTPError异常
        # 将原始域名和响应内容写入Excel
        ws.append([domain, response.text])
    except requests.exceptions.RequestException as e:
        # 如果请求失败，将错误信息写入Excel
        ws.append([domain, f"Error: {e}"])
    time.sleep(1 / requests_per_second)

# 保存Excel文件
wb.save('search_results.xlsx')
print("请求完成，结果已保存到'search_results.xlsx'")
