import platform
from collections import OrderedDict
import logging
import docker

os = platform.system


class getplatform:
    """
    收集操作系统数据
    """

    @staticmethod
    def get_os_all_info():
        """
        获取系统性能信息
        :return:
        """
        try:
            if pc := platform:
                # 获取操作系统名称及版本号
                Platform = pc.platform()
                # 获取操作系统版本号
                Version = pc.version()
                # 获取操作系统的位数
                Architecture = pc.architecture()
                # 计算机类型
                Machine = pc.machine()
                # 计算机的网络名称
                Node = pc.node()
                # 计算机操作系统类型
                System = pc.system()
                # 计算机处理器信息
                Processor = pc.processor()
                return OrderedDict({
                    'ID': None,
                    'Platform': Platform,
                    'Version': Version,
                    'Architecture': Architecture,
                    'Machine': Machine,
                    'Node': Node,
                    'System': System,
                    'Processor': Processor
                })
        except Exception as e:
            logging.error(f'获取客户端信息失败,错误信息{e}')
            return False
        finally:
            pass


class getdocker:
    """
    收集docker数据
    """
    CLIENT = docker.from_env()

    def __init__(self):
        # 指定docker socket目录创建client
        # self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        # 使用环境变量初始化client
        pass

    def get_docker_all_info(cls):
        """
        获取docker版本信息
        :return:
        """
        try:
            if docker_info := cls.CLIENT.version():
                docker_engine = docker_info['Platform']['Name']
                # go版本
                go_version = docker_info.get('GoVersion')
                # docker版本
                docker_version = docker_info.get('Version')
                # 运行主机系统类型
                os_type = docker_info.get('Os')
                # 运行主机处理器架构
                arch = docker_info.get('Arch')
                # docker Api版本
                api_version = docker_info.get('ApiVersion')
                # docker安装时间
                build_time = docker_info.get('BuildTime')
                return OrderedDict({
                    'id': None,
                    'docker_version': docker_version,
                    'api_version': api_version,
                    'build_time': build_time,
                    'docker_engine': docker_engine,
                    'os_type': os_type,
                    'arch': arch,
                    'go_version': go_version
                })

        except Exception as e:
            logging.error(f'获取客户端信息失败,错误信息{e}')
            return False
        finally:
            pass

    def get_docker_container_info(cls):
        """
        获取docker容器信息
        :return:
        """
        try:
            # 定义容器列表
            container_list = []
            results_set = cls.CLIENT.containers.list(all=True)
            for item in results_set:
                # 容器ID
                container_id = item.id
                # 容器名称
                container_name = item.name
                # 容器镜像
                container_image = item.image
                container_dict = OrderedDict({
                    'id': None,
                    'container_id': container_id,
                    'container_name': container_name,
                    'container_image': container_image.tags[-1],
                })
                container_list.append(container_dict)
            return container_list
        except Exception as e:
            logging.error(f'获取容器信息失败,错误信息{e}')
            return None
        finally:
            pass
        
    

    def get_docker_container_top(cls):
        try:
            process_list_all = []
            process_dict11 = {}
            results_set = cls.CLIENT.containers.list()
            for item in results_set:
                process_list = []
                container_id = item.id
                container_t = cls.CLIENT.containers.get(container_id)
                process_set = container_t.top()['Processes']
                for item2 in process_set:
                    process_UID = item2[0]
                    process_PID = item2[1]
                    process_PPID = item2[2]
                    process_dict = {
                        'UID': process_UID,
                        'PID': process_PID,
                        'PPID': process_PPID,
                    }
                    process_list.append(process_dict)
                    process_dict11[f"container_{container_id}"] = process_list
            return process_dict11
        except Exception as e:
            logging.error(f'获取容器信息失败,错误信息{e}')
            return None

        finally:
            pass


Docker = getdocker()
print(Docker.get_docker_container_top())




platform1 = getplatform()
print(platform1.get_os_all_info())

Docker = getdocker()
print(Docker.get_docker_all_info())
print(Docker.get_docker_container_info())
print(Docker.get_docker_container_top())
