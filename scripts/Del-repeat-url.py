from collections import Counter
from urllib.parse import urlparse
import tldextract

"""
Summary:

当从测绘中导出大量url时，可能会存在一个主域名有很多无用子域名的情况，该脚本会对同一个主域名保留前十个子域名，其他的删除

"""

def extract_main_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    extracted_domain = tldextract.extract(domain)
    return f"{extracted_domain.domain}.{extracted_domain.suffix}"

def keep_top_duplicates(input_file, output_file, num_duplicates):
    with open(input_file, 'r') as file:
        urls = file.read().splitlines()

    domain_counts = Counter(extract_main_domain(url) for url in urls)
    filtered_urls = []
    for url in urls:
        domain = extract_main_domain(url)
        if domain_counts[domain] <= num_duplicates:
            filtered_urls.append(url)
            domain_counts[domain] -= 1

    with open(output_file, 'w') as file:
        file.write('\n'.join(filtered_urls))

# 替换为你的url.txt文件路径和new-url.txt的输出路径
keep_top_duplicates('url.txt', 'new-url.txt', 10)

