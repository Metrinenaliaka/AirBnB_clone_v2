#!/usr/bin/python3
'''fabfile tar packaging'''
from fabric.api import local, run, env, put
from datetime import datetime
import os

env.user = 'ubuntu'
env.hosts = ['100.25.2.92', '54.172.76.0']


def do_pack():
    '''Packes web_static in tgz format'''

    n = datetime.now()
    name = "web_static_{}{}{}{}{}{}.tgz".format(
        n.year, n.month, n.day, n.hour, n.minute, n.second)
    local('mkdir -p versions')
    local("tar -cvzf versions/{} web_static".format(name))
    size = os.stat("versions/{}".format(name)).st_size
    print("web_static packed: versions/{} -> {}".format(name, size))
    path = "versions/{}".format(name)
    return path


def do_deploy(archive_path):
    """
    distributes an archive to your web servers
    """

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
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(name))
        print("New version deployed")
        return True
    except BaseException:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""

    try:
        path = do_pack()
    except BaseException:
        return False
    do_deploy(path)
