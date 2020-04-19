## 爬取(反反爬)瓜子二手车全站(requests+selenium+lxml+scrapy+mongodb)
### 项目需求: 
##### 爬取瓜子二手车中，所有城市中所有品牌的所有售卖数据，比如上海市的二手特斯拉的数据，获取城市和对应的品牌后，再破解详情页的反爬JS!全站爬取的数据量相当的庞大，可依据城市缩小范围，指定的城市是杭州市！
### 分析结果:
##### 1，经过分析，所有城市的数据是JS渲染(非异步)的，网页源代码没有城市数据，但有品牌数据，故使用Selenium来抓取城市，lxml来获取品牌，最终再构造一个# 结合城市和品牌的URL，以供后续的Scrapy爬取！本项目的Selenium驱动的是Chrome Browser，当然也可以用PhantomJS无介面Browser，取决于你自己，若是使用PhantomJS，代码中的chrome.maximize_window()可以省略！
##### 2，若全站爬取"全国所有的二手车"，2020/4/15当天为例，共约14万笔

#### 关键代码1:前置处理代码块--使用Selenium获取动态渲染的城市数据与lxml获取所有品牌
##### Note:使用text获取文本值若为空，表示该文本被隐藏，此时，可以获取title属性，或是innerHTML，比如get_attribute('innerHTML')，就可以获取到文本值!
![img1](https://github.com/ziliang-wang/Scrapy2/blob/master/guazi/images/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20200331200127.png)
##### 或是--for PhantomJS，All cities部份
![img4](https://github.com/ziliang-wang/Scrapy2/blob/master/guazi/images/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20200416005026.png)
### 破解反爬策略
#### 1，瓜子二手车的反爬策略: cookis反爬虫，未带cookies下返回的是经过混肴的js，如下图:
![img3](https://github.com/ziliang-wang/Scrapy2/blob/master/guazi/images/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20200415165830.png)
#### 2，关键代码2:
#### 自定义中间件/导入execjs模块，运行js函数anti()，得出cookie值，破解反爬js
#### with语句配合open上下文管理器，文件路径部份使用的是绝对路径，而非相对路径

![img2](https://github.com/ziliang-wang/Scrapy2/blob/master/guazi/images/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20200331202024.png)
### 补充说明：关spider的部份，此部份代码较简单，唯一要注意的是：
##### 1，刚开始从mongo取出来并发出去的请求，其返回的response会先经过downloader middleware中的js反反爬逻辑，再丢给调度器排序，然后再下载，属于同一个请求，所以要加上参数dont_filter = True，即不过滤同一个请求，请见下图：

##### 2 同理，下一页，即每一次的翻页请求，也需要经过下载器中间件的处理，也一样需要设置dont_filter = True，请见下图：
