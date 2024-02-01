import os
import re

def extract_summary_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        match = re.findall(r'"""\nSummary.*?\n(.*?)\n"""', content, re.DOTALL)
        if match:
            return match[0]
        else:
            return None

def check_duplicate(filename):
    with open('README.md', 'r') as file:
        contents = file.read()
        if filename in contents:
            return False
        else:
            return True

def main():
    readme_path = 'README.md'
    summary_content = ""

    for root, dirs, files in os.walk('./scripts', topdown=True):
        for file in files:
            file_path = os.path.join(root, file)
            summary = extract_summary_from_file(file_path)
            if summary and check_duplicate(f"## [{file}](/scripts/{file})"):
                print("写入摘要成功: " + file)
                summary_content += f"## [{file}](/scripts/{file})\n```\n{summary.strip()}\n```\n"
            elif summary:
                print("写入摘要失败，有重复内容: " + file)
            else:
                print("摘要为空: " + file)


    # Append extracted summaries to README
    with open(readme_path, 'a', encoding='utf-8') as readme_file:
        readme_file.write(summary_content)

if __name__ == "__main__":
    main()

