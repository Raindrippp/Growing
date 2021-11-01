#! /usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# NAME: process                                                         #
# FUNCTION: import process information to elasticsearch                 #
# ENV: Python3.6                                                        #
# Author: DingHang                                                      #
# CreateTime: 2021/10/28                                                #
#########################################################################






import platform
import logging
import docker
import socket
from elasticsearch import Elasticsearch, helpers
from collections import OrderedDict

es = Elasticsearch()
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
            logging.error(f'获取操作系统信息失败,错误信息{e}')
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
            logging.error(f'获取docker版本信息失败,错误信息{e}')
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
            process_dict11 = {}
            results_set = cls.CLIENT.containers.list()
            for item in results_set:
                process_list = []
                container_id = item.id
                #获取容器ID
                container_name = item.name
                #获取容器名
                container_t = cls.CLIENT.containers.get(container_id)
                process_set = container_t.top()['Processes
                #获取容器下进程信息
                for item2 in process_set:
                    process_UID = item2[0]
                    #获取进程UID
                    process_PID = item2[1]
                    #获取进程PID                            
                    process_PPID = item2[2]
                    #获取进程PPID
                    process_STIME = item2[4]
                    #获取进程STIME
                    process_TIME = item2[6]
                    #获取进程TIME
                    process_dict = OrderedDict({
                        'USER': process_UID,
                        'ID': process_PID,
                        'PPID': process_PPID,
                        'STIME': process_STIME,
                        'TIME': process_TIME,
                    })
                    process_list.append(process_dict)
                    process_dict11[f"{container_name}"] = process_list
            return process_dict11
        except Exception as e:
            logging.error(f'获取容器进程信息失败,错误信息{e}')
            return None
        finally:
            pass
        
       
    def docker_top_to_table(cls):
        try:
            docker_top = cls.get_docker_container_top()
            if docker_top and docker_top is not False:
                date = docker_top
                hostname = socket.gethostname()
                for key, the_value in date.items():
                    top_date = [{
                        "_index": "process",
                        "_hostname": hostname,
                        "_name": key,
                        "_USER": t['USER'],
                        '_ID': t['ID'],
                        '_PPID': t['PPID'],
                        '_STIME': t['STIME'],
                        '_TIME': t['TIME']
                    } for t in the_value]
                    helpers.bulk(es, top_date)
        except Exception as e:
            logging.error(f'docker进程信息写入失败,错误信息{e}')
        finally:
            pass

        

platform1 = getplatform()
Docker = getdocker()
print(platform1.get_os_all_info())
Docker.docker_top_to_table()
