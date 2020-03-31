import execjs
import requests
import re
from selenium import webdriver
from lxml import etree
from guazi_project.guazi_project.handle_mongo import mongo

url = 'https://www.guazi.com/www/buy'
header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Host":"www.guazi.com",
    "Sec-Fetch-Dest":"document",
    "Sec-Fetch-Mode":"navigate",
    "Sec-Fetch-Site":"none",
    "Sec-Fetch-User":"?1",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
}

r = requests.get(url=url, headers=header)
r.encoding = 'utf-8'

# 如果没带着Cookie去访问
if '正在打开中,请稍后...' in r.text:
    re_res = re.search(r'anti\(\'(.*?)\'\,\'(.*?)\'\)', r.text, re.S).groups()
    string, key = re_res[0], re_res[1]
    with open('kkk.js', 'r') as f:
        f_read = f.read()
    js = execjs.compile(f_read)
    js_return = js.call('anti', string, key)
    cookie_value = 'antipas=' + js_return
    header['Cookie'] = cookie_value
    r2 = requests.get(url=url, headers=header)

    # ------- All cities --------- #
    chrome = webdriver.Chrome()
    chrome.maximize_window()
    chrome.get(url=url)

    left_cities = chrome.find_elements_by_xpath('//div[@id="cityLeft"]/dl/dd/a')
    right_cities = chrome.find_elements_by_xpath('//div[@id="cityRight"]/dl/dd/a')

    all_cities = []
    all_cities_name = []
    for left_city in left_cities:
        all_cities.append(left_city.get_attribute('href').split('/')[-2])
        all_cities_name.append(left_city.get_attribute('title')[:-3])

    for right_city in right_cities:
        all_cities.append(right_city.get_attribute('href').split('/')[-2])
        all_cities_name.append(right_city.get_attribute('title')[:-3])

    chrome.quit()
    #  -------- All Brands ----------#
    html = etree.HTML(r2.text)
    brand_list = html.xpath('//div[@class="dd-all clearfix js-brand '
                            'js-option-hid-info"]/ul/li/p/a/@href')
    brand_name_list = html.xpath('//div[@class="dd-all clearfix '
                                 'js-brand js-option-hid-info"]/ul/li/p/a/text()')

    for city, city_name in zip(all_cities, all_cities_name):
        if city_name == '杭州':
            for brand, brand_name in zip(brand_list, brand_name_list):
                info = {}
                # https: // www.guazi.com / anji / audi / o1i7 /  # bread
                info['task_url'] = 'https://{}/{}/{}/{}'.format('www.guazi.com',
                                                           city, brand.split('/')[2],
                                                           'o1i7',
                                                           )
                info['city_name'] = city_name
                info['brand_name'] = brand_name
                mongo.save_task('guazi_task', info)





