import docker
import logging


class Docker_Prune:
    client = docker.from_env()

    def __init__(self):
        pass

    def prune_unused_images(self):
        try:
            list0 = self.client.images.prune(filters={'dangling': False})
        except Exception as e:
            logging.error(f'清理无用镜像失败,错误信息{e}')
            return None
        else:
            logging.info(f"成功清理镜像:{list0['ImagesDeleted']}")
        finally:
            pass


Docker = Docker_Prune()
Docker.prune_unused_images()
