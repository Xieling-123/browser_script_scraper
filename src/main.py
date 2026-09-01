import requests
from bs4 import BeautifulSoup
import csv
import time
import os

# -------- 常量配置（便于修改） --------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
BASE_URL = "https://movie.douban.com/top250?start={}&filter="

# -------- 动态路径（无需硬编码） --------
SCRIPT_DIR = os.path.dirname(__file__)          # 当前脚本所在目录
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "douban_movies.csv")

def scrape_douban():
    # 创建输出目录（exist_ok=True 避免重复判断）
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_FILE, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['排名', '电影名称', '评分', '经典台词/短评'])

        for page in range(0, 125, 25):
            url = BASE_URL.format(page)
            print(f"正在抓取页面: {url}")

            try:
                resp = requests.get(url, headers=HEADERS, timeout=10)
                resp.raise_for_status()  # 状态码非200时抛出异常，自动中断本次循环

                soup = BeautifulSoup(resp.text, 'html.parser')
                # 直接遍历所有电影项，无需 enumerate（排名从页面提取）
                for item in soup.find_all('div', class_='item'):
                    rank = item.find('em').text
                    title = item.find('span', class_='title').text
                    rating = item.find('span', class_='rating_num').text
                    quote_tag = item.find('span', class_='inq')
                    quote = quote_tag.text if quote_tag else "无短评"

                    print(f"抓取成功: {rank} - {title} - {rating}分")
                    writer.writerow([rank, title, rating, quote])

            except Exception as e:
                print(f"页面 {url} 抓取出错: {e}")

            # 每次请求后暂停 2 秒，避免封 IP
            time.sleep(2)

    print(f"\n全部抓取完成！数据已保存至 {OUTPUT_FILE}")

if __name__ == '__main__':
    scrape_douban()