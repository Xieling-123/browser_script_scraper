"""
项目入口模块。

这是整个项目的启动文件，当你执行 `python src/main.py` 时，Python 会从这里开始运行代码。

你可以在这个文件中编写主逻辑，或者导入其他模块。
例如，你可以新建一个 src/utils.py 文件，然后在这里导入它：from utils import my_function
"""
# source venv/Scripts/activate   # 先激活（注意 Git Bash 用 source）这里面要检查自己的虚拟环境叫做什么名字
# pip install 包名               # 激活后，这里的 pip 自动指向虚拟环境也就是激活这个然后才直接使用pip

# ./venv/Scripts/python -m pip install 包名 requests beautifulsoup4
# 虚拟环境安装对应的包

import requests  # 用来发请求（对应浏览器里的Network）
from bs4 import BeautifulSoup  # 用来解析网页（对应浏览器里的Elements）
import csv
import time
import os

# 1. 伪装请求头（对应浏览器网络面板里的 Request Headers）
# 如果不加 User-Agent，豆瓣会直接把你拦截掉
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# 2. 核心爬虫逻辑


def scrape_douban():
    # 创建存放数据的文件夹
    if not os.path.exists('D:/mytool/01_doc/doc-python/browser_script_scraper/output'):
        os.makedirs('D:/mytool/01_doc/doc-python/browser_script_scraper/output')

    # 打开CSV文件准备写入（utf-8-sig 防止Excel打开乱码）
    with open('D:/mytool/01_doc/doc-python/browser_script_scraper/output/douban_movies.csv', mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['排名', '电影名称', '评分', '经典台词/短评'])

        # 豆瓣每页25条，爬取前5页
        for page in range(0, 125, 25):
            url = f"https://movie.douban.com/top250?start={page}&filter="
            print(f"正在抓取页面: {url}")

            try:
                # 发送 GET 请求（对应浏览器里的 Fetch/XHR）
                response = requests.get(url, headers=headers)

                # 检查状态码（对应浏览器里的 Status 200）
                if response.status_code == 200:
                    # 用 BeautifulSoup 解析网页里的 HTML 结构
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # 找到所有电影的列表项
                    items = soup.find_all('div', class_='item')

                    for index, item in enumerate(items):
                        # 提取排名
                        rank = item.find('em').text
                        # 提取电影名（取第一个）
                        title = item.find('span', class_='title').text
                        # 提取评分
                        rating = item.find('span', class_='rating_num').text
                        # 提取短评（有的电影没有，加个判断）
                        quote_tag = item.find('span', class_='inq')
                        quote = quote_tag.text if quote_tag else "无短评"

                        # 打印出来看看
                        print(f"抓取成功: {rank} - {title} - {rating}分")

                        # 写入 CSV
                        writer.writerow([rank, title, rating, quote])
                else:
                    print(f"请求失败，状态码: {response.status_code}")

            except Exception as e:
                print(f"抓取出错: {e}")

            # 重要！每次抓完一页停顿2秒，防止请求太快被封IP
            time.sleep(2)

    print("\n全部抓取完成！数据已保存output/douban_movies.csv 中。")


if __name__ == '__main__':
    scrape_douban()
