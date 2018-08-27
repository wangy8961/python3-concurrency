import asyncio
import logging
import os
import sys
import time
import aiohttp
import aiofiles
import progressbar


# 当前模块文件的根目录
basepath = os.path.abspath(os.path.dirname(__file__))

# 记录日志
logger = logging.getLogger('spider')  # 创建logger实例
logger.setLevel(logging.CRITICAL)  # 保持控制台清爽，只输出总信息和进度条
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')  # 控制台日志和日志文件使用同一个Formatter
log_path = os.path.join(basepath, 'logs')  # 日志文件所在目录
if not os.path.isdir(log_path):
    os.mkdir(log_path)
filename = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) + '.log'  # 日志文件名，以当前时间命名
file_handler = logging.FileHandler(os.path.join(log_path, filename), encoding='utf-8')  # 创建日志文件handler
file_handler.setFormatter(formatter)  # 设置Formatter
file_handler.setLevel(logging.DEBUG)  # 单独设置日志文件的日志级别，注释掉则使用总日志级别
stream_handler = logging.StreamHandler()  # 控制台日志StreamHandler
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)  # 将handler添加到logger中
logger.addHandler(stream_handler)


def setup_down_path():
    '''设置图片下载后的保存位置，所有图片放在同一个目录下'''
    down_path = os.path.join(basepath, 'downloads')
    if not os.path.isdir(down_path):
        os.mkdir(down_path)
        logger.critical('Create download path {}'.format(down_path))
    return down_path


async def get_links():
    '''获取所有图片的下载链接'''
    async with aiofiles.open(os.path.join(basepath, 'flags.txt')) as f:  # 图片名都保存在这个文件中，每行一个图片名
        flags = await f.readlines()
        return ['http://192.168.40.121/flags/' + flag.strip() for flag in flags]


async def download_one(semaphore, session, image):
    logger.debug('Downloading No.{} [{}]'.format(image['linkno'], image['link']))
    t0 = time.time()

    try:
        async with semaphore:
            async with session.get(image['link']) as response:
                if response.status == 200:
                    image_content = await response.read()  # Binary Response Content: access the response body as bytes, for non-text requests
                else:
                    logger.error('received invalid response code: {}, message: {}'.format(response.status, response.reason))
                    raise aiohttp.ClientError()
    except Exception as e:
        logger.error('Exception {} raised on No.{} [{}]'.format(e.__class__, image['linkno'], image['link']))
        return False  # 用于告知 download_one() 的调用方，请求此图片URL时失败了

    filename = os.path.split(image['link'])[1]
    async with aiofiles.open(os.path.join(image['path'], filename), 'wb') as f:
        await f.write(image_content)

    t1 = time.time()
    logger.debug('Task No.{} [{}] runs {:.2f} seconds.'.format(image['linkno'], image['link'], t1 - t0))

    return True  # 用于告知 download_one() 的调用方，成功请求此图片URL


async def download_many():
    down_path = setup_down_path()
    links = await get_links()
    # 用于限制并发请求数量
    sem = asyncio.Semaphore(min(1000, len(links)))

    async with aiohttp.ClientSession() as session:  # aiohttp建议整个应用只创建一个session，不能为每个请求创建一个seesion
        successful_images = 0  # 请求成功的图片数
        failed_images = 0  # 请求失败的图片数

        if len(sys.argv) > 1 and sys.argv[1] == '-v':  # 输出详细信息
            logger.setLevel(logging.DEBUG)

            tasks = []  # 保存所有任务的列表
            for linkno, link in enumerate(links, 1):
                image = {
                    'path': down_path,
                    'linkno': linkno,  # 图片序号，方便日志输出时，正在下载哪一张
                    'link': link
                }
                task = asyncio.create_task(download_one(sem, session, image))  # asyncio.create_task()是Python 3.7新加的，否则使用asyncio.ensure_future()
                tasks.append(task)
            results = await asyncio.gather(*tasks)

            for result in results:
                if result:
                    successful_images += 1
                else:
                    failed_images += 1
        else:  # 输出进度条
            to_do = []
            for linkno, link in enumerate(links, 1):
                image = {
                    'path': down_path,
                    'linkno': linkno,  # 图片序号，方便日志输出时，正在下载哪一张
                    'link': link
                }
                to_do.append(download_one(sem, session, image))

            to_do_iter = asyncio.as_completed(to_do)

            with progressbar.ProgressBar(max_value=len(to_do)) as bar:
                for i, future in enumerate(to_do_iter):
                    result = await future
                    if result:
                        successful_images += 1
                    else:
                        failed_images += 1
                    bar.update(i)

        logger.critical('Successful [{}] images, failed [{}] images'.format(successful_images, failed_images))


if __name__ == '__main__':
    t0 = time.time()
    if sys.platform != 'win32':
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_many())
    loop.close()
    logger.critical('Total Cost {:.2f} seconds'.format(time.time() - t0))
