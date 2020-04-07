## 腾讯位置大数据爬虫

[链接](https://heat.qq.com/)

运行环境：Python3.6，需要numpy、pandas以及retry等第三方库。

运行`nohup python run.py &`，后台每五分钟自动执行`python myMap.py`脚本爬取数据，数据保存至data目录。

示例数据见data/2019-10-27 08_27_28.csv，数据有三列经纬度以及在此经纬度的定位请求数。

本项目仅供学习，官网上已经声明“星云图使用效果模拟数据，无法作为他用”。

