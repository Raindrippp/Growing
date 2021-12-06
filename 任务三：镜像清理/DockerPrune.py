import os
from logging.handlers import TimedRotatingFileHandler

import docker
import logging

path = '/root'
if not os.path.exists('log'):
    os.makedirs('log')
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOG_HANDLER = TimedRotatingFileHandler(filename='/root/log/myProgramLog.txt', when='midnight',
                                       interval=1, backupCount=7)
FORMAT = '%(asctime)s %(levelname)s %(message)s'
DATA_FORMAT = '%Y-%m-%d %H:%M:%S'
FOR_MATTER = logging.Formatter(FORMAT, DATA_FORMAT)
LOG_HANDLER.setFormatter(FOR_MATTER)
LOGGER.addHandler(LOG_HANDLER)


def info(msg):
    LOGGER.info(msg)
    return


def warning(msg):
    LOGGER.warning(msg)
    return


def error(msg):
    LOGGER.error(msg)
    return


class Docker_Prune:
    client = docker.from_env()

    def __init__(self):
        pass

    def prune_unused_images(self):
        try:
            list0 = self.client.images.prune(filters={'dangling': False})
        except Exception as e:
            error(f'清理无用镜像失败,错误信息{e}')
            return None
        else:
            info(f"成功清理镜像:{list0['ImagesDeleted']}")
        finally:
            pass


Docker = Docker_Prune()
Docker.prune_unused_images()
