# 1. 理论

- [Python3爬虫系列01 (理论) - I/O Models 阻塞 非阻塞 同步 异步](http://www.madmalls.com/blog/post/io-models/)
- [Python3爬虫系列02 (理论) - Python并发编程](http://www.madmalls.com/blog/post/concurrent-programming-for-python/)
- [Python3爬虫系列06 (理论) - 可迭代对象、迭代器、生成器](http://www.madmalls.com/blog/post/iterable-iterator-and-generator-in-python/)
- [Python3爬虫系列07 (理论) - 协程](http://www.madmalls.com/blog/post/coroutine-in-python/)
- [Python3爬虫系列08 (理论) - 使用asyncio模块实现并发](http://www.madmalls.com/blog/post/asyncio-howto-in-python3/)


# 2. 实验

- [Python3爬虫系列03 (实验) - 同步阻塞下载](http://www.madmalls.com/blog/post/sequential-download-for-python/)
- [Python3爬虫系列04 (实验) - 多进程并发下载](http://www.madmalls.com/blog/post/multi-process-for-python3/)
- [Python3爬虫系列05 (实验) - 多线程并发下载](http://www.madmalls.com/blog/post/multi-thread-for-python/)
- [Python3爬虫系列09 (实验) - 使用asyncio+aiohttp并发下载](http://www.madmalls.com/blog/post/aiohttp-howto-in-python3/)


# 3. 使用方法

## 3.1 下载代码

```bash
# git clone git@github.com:wangy8961/python3-concurrency.git
```

## 3.2 准备环境

### (1) Server

为防止DDoS攻击，本次测试需要在本地搭建一个HTTP测试服务器，具体方法参考 [Python3爬虫系列03 (实验) - 同步阻塞下载](http://www.madmalls.com/blog/post/sequential-download-for-python/)

### (2) Client

爬虫客户端所在的操作系统如果是`Linux`:

```bash
# pip install -r requirements-linux.txt
```

爬虫客户端所在的操作系统如果是`Windows`:

```bash
# pip install -r requirements-win32.txt
```

## 3.3 测试

### (1) 依序下载

```python
# python sequential.py
```

### (2) 多进程下载

```python
# python processpool.py
```

### (3) 多线程下载

```python
# python threadpool.py
```

### (4) 异步下载

```python
# python asynchronous.py
```