#!/usr/bin/python3
""" This module contains do_deloy function
"""
from fabric.api import put, run, env, local
from os import path
from datetime import datetime

env.hosts = ["34.239.255.45", "52.91.182.206"]


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


def do_deploy(archive_path):
    """
      Distributes an archive to a server web servers.
      Returns:
          False if the file at the path archive_path doesn’t exist.
    """
    if not path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        file_only = archive_path.split("/")[-1]
        file = file_only.split(".")[0]
        run(f"mkdir -p /data/web_static/releases/{file}")
        run(f"tar -xzf /tmp/{file}.tgz -C /data/web_static/releases/{file}/")
        run(f"rm /tmp/{file}.tgz")
        run(f"rm -rf /data/web_static/current")
        run(f"mv /data/web_static/releases/{file}/web_static/* "
            f"/data/web_static/releases/{file}")
        run(f"rm -rf /data/web_static/releases/{file}/web_static")
        run(f"ln -s /data/web_static/releases/{file} /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False
