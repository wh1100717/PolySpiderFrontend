PolySpiderFrontend
==================

This is a website project using web.py as the web framework, which is really easy-use, and bootstrap as fronten framework. Hightcharts, Highstock and Datatables are also included in this project. It focus on showing data in different views and dimensions.

## Requirements
*	[Python] v2.7+
*	[web.py] v0.37+
*	[redis-py] v2.9+
*	[Supervisor] v3.0+
*	Dependencies are listed in [Installation]
*	ak & sk & bucket name of [BaiYun] or [Upyun] for files upload
*	Tested in Windows(both 32&64bit) and CentOS 6.4(64bit)

## Contribution Guides
1.	[Getting Involved]

## Usage
There is a frontend project based on HTML5 in the folder `PolySpiderFrontend/web/` using web.py python web framework. It also integrate BootStrap3 as the frontend framework and some plugins like highcharts, highstock, datatables and so on.

1.  Step into `PolySpiderFrontend/web/` directory
2.  Use `python web-server.py` command to set up a host server.(you can also use `python web-server.py portname`) to specify a particular port.
3.  Just browser this website with `localhost:portname` link address.

[Python]: http://www.python.org/
[web.py]: http://webpy.org/
[redis-py]: https://github.com/andymccurdy/redis-py
[Supervisor]: https://pypi.python.org/pypi/supervisor

[BaiYun]: http://developer.baidu.com
[Upyun]: https://www.upyun.com
[Getting Involved]: http://wh1100717.github.io/PolyTechDocs/docs/invovled/
[Installation]: http://wh1100717.github.io/PolyTechDocs/python/scrapy/installation/
[TODO List]: https://github.com/wh1100717/PolySpider/blob/master/docs/TODO_LIST.md
[Core Functionalities]: https://github.com/wh1100717/PolySpider/blob/master/docs/pipelineinfo.md
[Tips]: https://github.com/wh1100717/PolySpider/blob/master/docs/TIPS.md
[PolySpider]: https://github.com/wh1100717/PolySpider
