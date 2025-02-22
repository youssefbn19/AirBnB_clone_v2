#!/usr/bin/python3
""" This module contains do_deloy function
"""
from fabric.api import put, run, env, local, task
from os import path
from datetime import datetime

env.hosts = ["34.239.255.45", "52.91.182.206"]
env.user = "ubuntu"


def do_pack():
    """
      Generates a .tgz archive from the contents of the web_static
      folder of your AirBnB Clone repo
      Returns:
          the archive path if the archive has been correctly generated.
          Otherwise, it should return None
    """
    d = datetime.now()
    file_name = "web_static_{}{}{}".format(d.year, d.month, d.day)
    file_name += "{}{}{}.tgz".format(d.hour, d.minute, d.second)
    local("mkdir -p versions")
    res = local("tar -cvzf versions/{} web_static".format(file_name))
    if res.succeeded:
        return "versions/{}".format(file_name)
    else:
        return None


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
        res = put(archive_path, "/tmp/")
        file_only = archive_path.split("/")[-1]
        file = file_only.split(".")[0]
        res = run("mkdir -p /data/web_static/releases/{}".format(file))
        res = run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
                  .format(file_only, file))
        res = run("rm /tmp/{}".format(file_only))
        res = run("rm -rf /data/web_static/current")
        res = run("mv -f /data/web_static/releases/{}/web_static/* "
                  "/data/web_static/releases/{}".format(file, file))
        res = run("rm -rf /data/web_static/releases/{}/web_static"
                  .format(file))
        res = run("ln -s /data/web_static/releases/{} /data/web_static/current"
                  .format(file))
        print("New version deployed!")
    except Exception:
        pass
    finally:
        if res.succeeded:
            return True
        else:
            return False
