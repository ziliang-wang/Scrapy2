## 爬取(反反爬)瓜子二手车全站(requests+selenium+lxml+scrapy+mongodb)
### 项目需求: 爬取瓜子二手车中，所有城市中所有品牌的所有售卖数据，比如上海市的二手特斯拉的数据，获取城市和对应的品牌后，再破解详情页的反爬JS!数据量相当的庞大，此项目爬取时，指定的城市是杭州市！
### 分析结果: 经过分析，所有城市的数据是JS渲染(非异步)的，网页源代码没有城市数据，但有品牌数据，故使用Selenium来抓取城市，lxml来获取品牌，最终再构造一个结合城市和品牌的URL，以供后续的Scrapy爬取！本项目的Selenium驱动的是Chrome Browser，当然也可以用PhantomJS无介面Browser，取决于你自己，若是使用PhantomJS，代码中的chrome.maximize_window()可以省略！

### 关键代码1:前置处理代码块--使用Selenium获取动态渲染的城市数据与lxml获取所有品牌

![img1](https://github.com/ziliang-wang/Scrapy2/blob/master/guazi/images/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20200331200127.png)

### 关键代码2:自定义中间件/破解反爬js
### with语句配合open上下文管理器，文件路径部份使用的是绝对路径，而非相对路径

![img2](https://github.com/ziliang-wang/Scrapy2/blob/master/guazi/images/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20200331202024.png)
