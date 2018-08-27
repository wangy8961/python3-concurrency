import time
from common import setup_down_path, get_links, download_one
from logger import logger


def download_many():
    '''依序下载所有图片，同步阻塞'''
    down_path = setup_down_path()
    links = get_links()

    for linkno, link in enumerate(links, 1):
        image = {
            'path': down_path,
            'linkno': linkno,  # 图片序号，方便日志输出时，正在下载哪一张
            'link': link
        }
        download_one(image)

    return len(links)


if __name__ == '__main__':
    t0 = time.time()
    count = download_many()
    msg = '{} flags downloaded in {:.2f} seconds.'
    logger.info(msg.format(count, time.time() - t0))
