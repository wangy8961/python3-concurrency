# [python3-concurrency](http://www.madmalls.com/blog/category/python3-spider/)

[![Python](https://img.shields.io/badge/python-v3.4%2B-blue.svg)](https://www.python.org/)
[![aiohttp](https://img.shields.io/badge/aiohttp-v3.3.2-brightgreen.svg)](https://aiohttp.readthedocs.io/en/stable/)
[![BeautifulSoup4](https://img.shields.io/badge/BeautifulSoup4-v4.6.3-orange.svg)](https://pypi.org/project/beautifulsoup4/)
[![requests](https://img.shields.io/badge/requests-v2.19.1-yellow.svg)](http://docs.python-requests.org/en/master/)
[![pymongo](https://img.shields.io/badge/pymongo-v3.7.1-red.svg)](https://pypi.org/project/pymongo/)
[![progressbar2](https://img.shields.io/badge/progressbar2-v3.38.0-lightgrey.svg)](https://pypi.org/project/progressbar2/)


![](http://www.madmalls.com/api/medias/uploaded/python3-concurrency-1016d526.png)


# 1. 爬虫系列

- [Python 3 爬虫｜第1章：I/O Models 阻塞/非阻塞 同步/异步](https://madmalls.com/blog/post/io-models/)
- [Python 3 爬虫｜第2章：Python 并发编程](https://madmalls.com/blog/post/concurrent-programming-for-python/)
- [Python 3 爬虫｜第3章：同步阻塞下载](https://madmalls.com/blog/post/sequential-download-for-python/)
- [Python 3 爬虫｜第4章：多进程并发下载](https://madmalls.com/blog/post/multi-process-for-python3/)
- [Python 3 爬虫｜第5章：多线程并发下载](https://madmalls.com/blog/post/multi-thread-for-python/)
- [Python 3 爬虫｜第6章：可迭代对象 / 迭代器 / 生成器](https://madmalls.com/blog/post/iterable-iterator-and-generator-in-python/)
- [Python 3 爬虫｜第7章：协程 Coroutines](https://madmalls.com/blog/post/coroutine-in-python/)
- [Python 3 爬虫｜第8章：使用 asyncio 模块实现并发](https://madmalls.com/blog/post/asyncio-howto-in-python3/)
- [Python 3 爬虫｜第9章：使用 asyncio + aiohttp 并发下载](https://madmalls.com/blog/post/aiohttp-howto-in-python3/)
- [Python 3 爬虫｜第10章：爬取少量妹子图](https://madmalls.com/blog/post/python3-concurrency-pics-01/)
- [Python 3 爬虫｜第11章：爬取海量妹子图](https://madmalls.com/blog/post/python3-concurrency-pics-02/)


# 2. 使用方法

## 2.1 Server

为防止DDoS攻击，本次测试需要在本地搭建一个HTTP测试服务器，具体方法参考 [Python3爬虫系列03 (实验) - 同步阻塞下载](http://www.madmalls.com/blog/post/sequential-download-for-python/)

## 2.2 Client

### (1) 下载代码

```bash
[root@CentOS ~]# git clone https://github.com/wangy8961/python3-concurrency.git
[root@CentOS ~]# cd python3-concurrency/
```

### (2) 准备虚拟环境

如果你的操作系统是`Linux`:

```bash
[root@CentOS python3-concurrency]# python3 -m venv venv3
[root@CentOS python3-concurrency]# source venv3/bin/activate
```

> `Windows`激活虚拟环境的命令是: `venv3\Scripts\activate`

### (3) 安装依赖包

如果你的操作系统是`Linux`:

```bash
(venv3) [root@CentOS python3-concurrency]# pip install -r requirements-linux.txt
```

如果你的操作系统是`Windows`（不会使用`uvloop`）:

```bash
(venv3) C:\Users\wangy> pip install -r requirements-win32.txt
```

### (4) 测试

依序下载：

```python
(venv3) [root@CentOS python3-concurrency]# python sequential.py
```

多进程下载：

```python
(venv3) [root@CentOS python3-concurrency]# python processpool.py
```

多线程下载：

```python
(venv3) [root@CentOS python3-concurrency]# python threadpool.py
```

异步下载：

```python
(venv3) [root@CentOS python3-concurrency]# python asynchronous.py
```