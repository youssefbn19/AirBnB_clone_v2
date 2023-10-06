#!/usr/bin/python3
""" This module contains do_deloy function
"""
from fabric.api import put, run, env, local, task, runs_once
from os import path
from datetime import datetime


env.hosts = ["34.239.255.45", "52.91.182.206"]


@runs_once
def do_pack():
    """
      Generates a .tgz archive from the contents of the web_static
      folder of your AirBnB Clone repo
      Returns:
          the archive path if the archive has been correctly generated.
          Otherwise, it should return None
    """
    d = datetime.now()
    file_name = f"web_static_{d.year}{d.month}{d.day}"\
                f"{d.hour}{d.minute}{d.second}.tgz"
    local("mkdir -p versions")
    res = local(f"tar -cvzf versions/{file_name} web_static")
    if res.succeeded:
        return f"versions/{file_name}"
    else:
        return None


@task
def do_deploy(archive_path):
    """
      Distributes an archive to a server web servers.
      Returns:
          False if the file at the path archive_path doesnt exist
          or an operation failed, True otherwise.
    """
    if not path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        file_only = archive_path.split("/")[-1]
        file = file_only.split(".")[0]
        run("mkdir -p /data/web_static/releases/{}".format(file))
        run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
            .format(file, file))
        run("rm /tmp/{}.tgz".format(file))
        run("rm -rf /data/web_static/current")
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}".format(file, file))
        run("rm -rf /data/web_static/releases/{}/web_static".format(file))
        run("ln -s /data/web_static/releases/{} /data/web_static/current"
            .format(file))
        print("New version deployed!")
        return True
    except Exception:
        return False


@task
def deploy():
    """
        Creates and distributes an archive to a web servers
        based on do_pack and do_deploy function
        Return:
            False if no archive has been created,
            and maybe True or False depends on do_deploy returns
    """
    path = do_pack()
    if path:
        return do_deploy(path)
    else:
        return False
