# 写入txt文件
import json
import requests
from requests.exceptions import RequestException
import re
import time

def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    # 学会搭配.*?和其他特殊的字符截取要提取的内容，就算内容含有杂质可以事后字符串处理
    pattern = re.compile('<h1>(.*?)</h1>.*?<P>(.*)</P>.*?</DIV>', re.S)
    items = re.findall(pattern, html)
    print(items)
    for item in items:
        yield {
            'title': item[0],
            'content': item[1].replace('<P>', '').replace('</P>', '').replace('\u3000', '').replace('&nbsp;', ' ').strip()
        }

def write_to_file(item):
    with open('corpus.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(item,ensure_ascii=False)+'\n')

def main(url):
    print(url)
    html = get_one_page(url)
    # print(html)
    if html == None:
        return
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    # 为了简便，只爬取每天的第一版的第一篇
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
            '19', '20', '21', '22', '23', '24', '25', '26', '27', '28']
    for month in months:
        for day in days:
            url = 'http://paper.people.com.cn/rmrb/html/2018-' + month + '/' + day + '/nw.D110000renmrb_2018' + month + day + '_1-01.htm'
            main(url)
            # time.sleep(1)
