import os
import time
import requests
from logger import logger


basepath = os.path.abspath(os.path.dirname(__file__))  # 当前模块文件的根目录


def setup_down_path():
    '''设置图片下载后的保存位置，所有图片放在同一个目录下'''
    down_path = os.path.join(basepath, 'downloads')
    if not os.path.isdir(down_path):
        os.mkdir(down_path)
        logger.info('Create download path {}'.format(down_path))
    return down_path


def get_links():
    '''获取所有图片的下载链接'''
    with open(os.path.join(basepath, 'flags.txt')) as f:  # 图片名都保存在这个文件中，每行一个图片名
        return ['http://192.168.40.121/flags/' + flag.strip() for flag in f.readlines()]


def download_one(image):  # 为什么设计成接收一个字典参数，而不是三个位置参数? 方便后续多线程时concurrent.futures.ThreadPoolExecutor.map()
    '''下载一张图片
    :param image: 字典，包括图片的保存目录、图片的序号、图片的URL
    '''
    logger.info('Downloading No.{} [{}]'.format(image['linkno'], image['link']))
    t0 = time.time()

    resp = requests.get(image['link'])
    filename = os.path.split(image['link'])[1]
    with open(os.path.join(image['path'], filename), 'wb') as f:
        f.write(resp.content)  # resp.content是bytes类型，而resp.text是str类型

    t1 = time.time()
    logger.info('Task No.{} [{}] runs {:.2f} seconds.'.format(image['linkno'], image['link'], t1 - t0))


def download_one_1(path, linkno, link):
    '''下载一张图片
    :param path: 图片的保存目录
    :param linkno: 图片的序号
    :param link: 图片的URL
    '''
    logger.info('Downloading No.{} [{}]'.format(linkno, link))
    t0 = time.time()

    resp = requests.get(link)
    filename = os.path.split(link)[1]
    with open(os.path.join(path, filename), 'wb') as f:
        f.write(resp.content)

    t1 = time.time()
    logger.info('Task No.{} [{}] runs {:.2f} seconds.'.format(linkno, link, t1 - t0))
