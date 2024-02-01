#!/usr/bin/python3
'''packaging and deployement'''
from fabric.api import local, run, env, put
from datetime import datetime
import os

env.user = 'ubuntu'
env.hosts = ['100.25.2.92', '54.172.76.0']


def do_pack():
    '''Packes web_static in tgz format'''
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(date)
    if os.path.isdir("versions") is False:
        local(" mkdir versions")
    local('tar -cvzf ' + file_path + ' web_static')
    if os.path.exists(file_path):
        return file_path
    return None


def do_deploy(archive_path):
    """deploying achive files"""
    if not archive_path:
        return False
    name = archive_path.split('/')[1]
    try:
        put(archive_path, '/tmp/')
        run("mkdir -p /data/web_static/releases/{}".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
            .format(name, name))
        run("rm /tmp/{}".format(name))
        run("mv /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}".format(name, name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(name))
        print("New version deployed")
        return True
    except BaseException:
        return False
