import time
from queue import Queue
from threading import Thread
from functools import partial
from concurrent import futures
from common import setup_down_path, get_links, download_one, download_one_1
from logger import logger


class ThreadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            down_path, linkno, link = self.queue.get()
            download_one_1(down_path, linkno, link)
            self.queue.task_done()


def download_many():
    '''多线程，按线程数 并发（非并行） 下载所有图片'''
    down_path = setup_down_path()
    links = get_links()

    # 创建队列
    queue = Queue()

    # 创建多个线程
    for i in range(64):
        worker = ThreadWorker(queue)
        worker.daemon = True  # 如果工作线程在等待更多的任务时阻塞了，主线程也可以正常退出
        worker.start()  # 启动线程

    # 往队列中投放任务
    for linkno, link in enumerate(links, 1):  # 链接带序号
        logger.info('Queueing No.{} {}'.format(linkno, link))
        queue.put((down_path, linkno, link))

    logger.info('Waiting for all subthread done...')
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    logger.info('All subthread done.')

    return len(links)


def download_many_1():
    '''多线程，按线程数 并发（非并行） 下载所有图片
    使用concurrent.futures.ThreadPoolExecutor()
    Executor.map()使用Future而不是返回Future，它返回迭代器，
    迭代器的__next__()方法调用各个Future的result()方法，因此我们得到的是各个Future的结果，而非Future本身

    注意Executor.map()限制了download_one()只能接受一个参数，所以images是字典构成的列表
    '''
    down_path = setup_down_path()
    links = get_links()

    images = []
    for linkno, link in enumerate(links, 1):
        image = {
            'path': down_path,
            'linkno': linkno,
            'link': link
        }
        images.append(image)

    workers = min(64, len(links))  # 保证线程池中的线程不会多于总的下载任务数
    # with语句将调用executor.__exit__()方法，而这个方法会调用executor.shutdown(wait=True)方法，它会在所有进程都执行完毕前阻塞主进程
    with futures.ThreadPoolExecutor(workers) as executor:
        # executor.map()效果类似于内置函数map()，但download_one()函数会在多个线程中并发调用
        # 它的返回值res是一个迭代器<itertools.chain object>，我们后续可以迭代获取各个被调用函数的返回值
        res = executor.map(download_one, images)  # 传一个序列

    return len(list(res))  # 如果有进程抛出异常，异常会在这里抛出，类似于迭代器中隐式调用next()的效果


def download_many_2():
    '''多线程，按线程数 并发（非并行） 下载所有图片
    使用concurrent.futures.ThreadPoolExecutor()
    Executor.map()中的调用函数如果要接受多个参数，可以给Executor.map()传多个序列
    参考：https://yuanjiang.space/threadpoolexecutor-map-method-with-multiple-parameters
    '''
    down_path = setup_down_path()
    links = get_links()

    # 固定住保存的路径，不用每次调用下载图片函数时都传同样的down_path参数
    download_one_1_partial = partial(download_one_1, down_path)

    # 创建包含所有linkno的序列
    linknos = [i for i in range(len(links))]

    workers = min(64, len(links))  # 保证线程池中的线程不会多于总的下载任务数
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one_1_partial, linknos, links)  # 给Executor.map()传多个序列

    return len(list(res))


def download_many_3():
    '''多线程，按线程数 并发（非并行） 下载所有图片
    使用concurrent.futures.ThreadPoolExecutor()
    不使用Executor.map()，而使用Executor.submit()和concurrent.futures.as_completed()
    Executor.submit()方法会返回Future，而Executor.map()是使用Future
    '''
    down_path = setup_down_path()
    links = get_links()

    # 固定住保存的路径，不用每次调用下载图片函数时都传同样的down_path参数
    download_one_1_partial = partial(download_one_1, down_path)

    workers = min(64, len(links))  # 保证线程池中的线程不会多于总的下载任务数
    with futures.ThreadPoolExecutor(workers) as executor:
        to_do = []
        # 创建并排定Future
        for linkno, link in enumerate(links, 1):  # 链接带序号
            future = executor.submit(download_one_1_partial, linkno, link)
            to_do.append(future)
            logger.debug('Scheduled for No.{} {}: {}'.format(linkno, link, future))

        results = []
        # 获取Future的结果，futures.as_completed(to_do)的参数是Future列表，返回迭代器，
        # 只有当有Future运行结束后，才产出future
        for future in futures.as_completed(to_do):  # future变量表示已完成的Future对象，所以后续future.result()绝不会阻塞
            res = future.result()
            results.append(res)
            logger.debug('{} result: {!r}'.format(future, res))

    return len(results)


if __name__ == '__main__':
    t0 = time.time()
    count = download_many()
    msg = '{} flags downloaded in {:.2f} seconds.'
    logger.info(msg.format(count, time.time() - t0))
