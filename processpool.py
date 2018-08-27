import time
from functools import partial
from multiprocessing import Pool
from concurrent import futures
from common import setup_down_path, get_links, download_one, download_one_1
from logger import logger


def download_many():
    '''多进程，按进程数 并行 下载所有图片
    使用multiprocessing.Pool.apply_async()
    '''
    down_path = setup_down_path()
    links = get_links()

    p = Pool(4)  # 指定进程池中的进程数
    for linkno, link in enumerate(links, 1):
        image = {
            'path': down_path,
            'linkno': linkno,
            'link': link
        }
        p.apply_async(download_one, args=(image,))

    logger.info('Waiting for all subprocesses done...')
    p.close()  # 关闭进程池
    p.join()  # 主进程等待进程池中的所有子进程结束
    logger.info('All subprocesses done.')

    return len(links)


def download_many_1():
    '''多进程，按进程数 并行 下载所有图片
    使用multiprocessing.Pool.map(download_one, images)
    注意Pool.map()限制了download_one()只能接受一个参数，所以images是字典构成的列表
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

    with Pool(4) as p:
        p.map(download_one, images)  # 将images序列依次映射给download_one()函数

    logger.info('Waiting for all subprocesses done...')
    # p.close()  # 使用with语句和Pool.map()后，会自动调用Pool.close()和Pool.join()
    # p.join()
    logger.info('All subprocesses done.')

    return len(links)


def download_many_2():
    '''多进程，按进程数 并行 下载所有图片
    使用multiprocessing.Pool.starmap(download_one_1, images)，它是Python-3.3添加的
    可以给download_one_1()函数传元组组成的序列，会自动解包元组给函数的多个参数
    '''
    down_path = setup_down_path()
    links = get_links()

    images = []
    for linkno, link in enumerate(links, 1):
        images.append((down_path, linkno, link))

    with Pool(4) as p:
        p.starmap(download_one_1, images)  # 链接带序号

    logger.info('Waiting for all subprocesses done...')
    # p.close()
    # p.join()
    logger.info('All subprocesses done.')

    return len(links)


def download_many_3():
    '''多进程，按进程数 并行 下载所有图片
    使用multiprocessing.Pool.starmap(download_one_1, images)，它是Python-3.3添加的
    可以给download_one_1()函数传元组组成的序列，会自动解包元组给函数的多个参数
    由于下载每张图片时的保存目录都相同，可以使用functools.partial()固定住这个参数
    '''
    down_path = setup_down_path()
    links = get_links()

    # 固定住保存的路径，不用每次调用下载图片函数时都传同样的down_path参数
    download_one_1_partial = partial(download_one_1, down_path)

    images = []
    for linkno, link in enumerate(links, 1):
        images.append((linkno, link))  # 每个元组将不包含保存的目录

    with Pool(4) as p:
        p.starmap(download_one_1_partial, images)  # 链接带序号

    logger.info('Waiting for all subprocesses done...')
    # p.close()
    # p.join()
    logger.info('All subprocesses done.')

    return len(links)


def download_many_4():
    '''多进程，按进程数 并行 下载所有图片
    使用concurrent.futures.ProcessPoolExecutor()
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

    # with语句将调用executor.__exit__()方法，而这个方法会调用executor.shutdown(wait=True)方法，它会在所有进程都执行完毕前阻塞主进程
    with futures.ProcessPoolExecutor(max_workers=16) as executor:  # 不指定max_workers时，进程池中进程个数默认为os.cpu_count()
        # executor.map()效果类似于内置函数map()，但download_one()函数会在多个进程中并行调用
        # 它的返回值res是一个迭代器<itertools.chain object>，我们后续可以迭代获取各个被调用函数的返回值
        res = executor.map(download_one, images)  # 传一个序列

    return len(list(res))  # 如果有进程抛出异常，异常会在这里抛出，类似于迭代器中隐式调用next()的效果


def download_many_5():
    '''多进程，按进程数 并行 下载所有图片
    使用concurrent.futures.ProcessPoolExecutor()
    Executor.map()中的调用函数如果要接受多个参数，可以给Executor.map()传多个序列
    参考：https://yuanjiang.space/threadpoolexecutor-map-method-with-multiple-parameters
    '''
    down_path = setup_down_path()
    links = get_links()

    # 固定住保存的路径，不用每次调用下载图片函数时都传同样的down_path参数
    download_one_1_partial = partial(download_one_1, down_path)

    # 创建包含所有linkno的序列
    linknos = [i for i in range(len(links))]

    with futures.ProcessPoolExecutor(max_workers=16) as executor:
        res = executor.map(download_one_1_partial, linknos, links)  # 给Executor.map()传多个序列

    return len(list(res))


def download_many_6():
    '''多进程，按进程数 并行 下载所有图片
    使用concurrent.futures.ProcessPoolExecutor()
    不使用Executor.map()，而使用Executor.submit()和concurrent.futures.as_completed()
    Executor.submit()方法会返回Future，而Executor.map()是使用Future
    '''
    down_path = setup_down_path()
    links = get_links()

    # 固定住保存的路径，不用每次调用下载图片函数时都传同样的down_path参数
    download_one_1_partial = partial(download_one_1, down_path)

    with futures.ProcessPoolExecutor(max_workers=16) as executor:
        to_do = []
        # 创建并且排定Future
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
    count = download_many_4()
    msg = '{} flags downloaded in {:.2f} seconds.'
    logger.info(msg.format(count, time.time() - t0))
