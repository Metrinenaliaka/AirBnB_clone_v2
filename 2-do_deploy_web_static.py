#!/usr/bin/python3
"""
    script that distributes an archive to your web servers
"""
import os.path
from datetime import datetime
from fabric.api import *

env.hosts = ['100.25.2.92', '54.172.76.0']
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_pack():
    """generationg a tgz file"""
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(date)
    if os.path.isdir("versions") is False:
        local(" mkdir versions")
    local('tar -cvzf ' + file_path + ' web_static')
    if os.path.exists(file_path):
        return file_path
    return None


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if os.path.exists(archive_path) is False:
        return False
    archive_name = archive_path.split('/')[1]
    arch_mod = archive_name.split(".")[0]
    remote_path = "/data/web_static/releases/" + arch_mod
    upload_path = '/tmp/' + archive_name
    put(archive_path, '/tmp/')
    # put(archive_path, upload_path)
    sudo('mkdir -p ' + remote_path)
    sudo('tar -xzf /tmp/{} -C {}/'.format(archive_name, remote_path))
    sudo('rm {}'.format(upload_path))
    mv = 'mv ' + remote_path + '/web_static/* ' + remote_path + '/'
    sudo(mv)
    sudo('rm -rf ' + remote_path + '/web_static')
    sudo('rm -rf /data/web_static/current')
    sudo('ln -s ' + remote_path + ' /data/web_static/current')
    return True
