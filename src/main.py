# 创建项目，激活虚拟环境
# pip install requests beautifulsoup4 

# 打开你要抓取的网页，F12开发者模式
# 网络：看url，url里面会显示1页数据的条数，找规律；
# 网络：看类型，显示xrh需要抓接口，这是动态网址；显示documents就是静态网址，数据都在html里面

# %%
# 第1步：在F12网络面板看“标头（Headers）”
# 操作：点击那个 top250?start=... 的请求。在右侧找到 请求标头 (Request Headers) 里的 User-Agent，全选复制；再看 常规 (General) 里的 请求 URL，复制下来。
# 对应代码（加上请求头防反爬）：

# %%
import requests

# 1. 把F12里复制的 URL 填进这里（注意：'start=0'代表第一页）
url = 'https://movie.douban.com/top250?start=0'

# 2. 把F12里复制的完整 User-Agent 填进这里（必须原封不动复制那一长串）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' # 👈 你必须在F12里复制你自己的替换这一行
}

# 3. 发送请求，获取源代码（对应F12里的“响应”）
response = requests.get(url, headers=headers)

# 验证是否成功（如果在F12看到的操作是200，这里打印出的也应该是200）
print("状态码:", response.status_code) 


# %%
# 第2步：在F12看“预览和响应（Response）”确认数据在HTML里，去元素里面看，操作界面点击自己需要的数据，看html里面是怎么写的，然后去解析html

# 操作：点击元素和界面去找需要的信息，看信息在html里面的格式,类似这种，去源码里面看格式，发请求，会响应数据在源码
# <div class="item">
#     <span class="title">楚门的世界</span>
#     <span class="rating_num">9.4</span>
# </div>
# 对应代码（引入解析工具，准备解析）：

# %%
from bs4 import BeautifulSoup

# 4. 把刚才下载下来的网页文本（response.text）交给 BeautifulSoup 解析
soup = BeautifulSoup(response.text, 'html.parser')

# 此时，soup就相当于F12里“元素”面板里看到的那棵DOM树
print(soup)

电影卡片信息=soup.find_all()

# %%
