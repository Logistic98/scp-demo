# -*- coding: utf-8 -*-

import os
from configparser import RawConfigParser
import paramiko
import logging

'''
对于远程服务器的指定路径，可以根据筛选规则上传文件
'''

# 生成日志文件
logging.basicConfig(filename='push_file.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def read_config():
    cfg = RawConfigParser()
    cfg.read('./config.ini', encoding='utf-8')
    host_ip = cfg.get('push', 'host_ip')
    host_port = cfg.get('push', 'host_port')
    host_username = cfg.get('push', 'host_username')
    host_password = cfg.get('push', 'host_password')
    remote_path = cfg.get('push', 'remote_path')
    local_path = cfg.get('push', 'local_path')
    push_file_key = cfg.get('push', 'push_file_key')
    push_file_suffix = cfg.get('push', 'push_file_suffix')
    scp_config = {}
    scp_config['host_ip'] = host_ip
    scp_config['host_port'] = host_port
    scp_config['host_username'] = host_username
    scp_config['host_password'] = host_password
    scp_config['remote_path'] = remote_path
    scp_config['local_path'] = local_path
    scp_config['push_file_key'] = push_file_key
    scp_config['push_file_suffix'] = push_file_suffix
    return scp_config


def push(host_ip, host_port, host_username, host_password, remote_path, local_path, push_file_key, push_file_suffix):
    scp = paramiko.Transport((host_ip, host_port))
    scp.connect(username=host_username, password=host_password)
    sftp = paramiko.SFTPClient.from_transport(scp)
    files = os.listdir(local_path)
    key = push_file_key
    suffix_name = push_file_suffix
    suffix_len = len(suffix_name)
    try:
        for file in files:
            if file.find(key) != -1:
                # 判断文件后缀
                if file[-int(suffix_len):] == suffix_name:
                    local_file = local_path + file
                    remote_file = remote_path + file
                    try:
                        sftp.put(local_file, remote_file)
                        logger.info(file + 'file push successfully')
                    except Exception as e:
                        logger.error(e)
    except IOError:
        logger.error("remote_path or local_path is not exist")
    scp.close()


if __name__ == '__main__':
    # 读取配置文件
    scp_config = read_config()
    host_ip = str(scp_config['host_ip'])
    host_port = int(scp_config['host_port'])
    host_username = str(scp_config['host_username'])
    host_password = str(scp_config['host_password'])
    remote_path = str(scp_config['remote_path'])
    local_path = str(scp_config['local_path'])
    push_file_key = str(scp_config['push_file_key'])
    push_file_suffix = str(scp_config['push_file_suffix'])
    # 调用方法上传文件
    push(host_ip, host_port, host_username, host_password, remote_path, local_path, push_file_key, push_file_suffix)

