#!/usr/bin/python3
""" This module contains do_deloy function
"""
from fabric.api import put, run, env
env.hosts = ["34.239.255.45", "52.91.182.206"]


def do_deploy(archive_path):
    """
      Distributes an archive to a server web servers.
      Returns:
          False if the file at the path archive_path doesnt exist
          or an operation failed, True otherwise.
    """
    try:
        put(archive_path, "/tmp/")
        file_only = archive_path.split("/")[-1]
        file = file_only.split(".")[0]
        run(f"mkdir -p /data/web_static/releases/{file}/")
        run(f"tar -xzf /tmp/{file}.tgz -C /data/web_static/releases/{file}/")
        run(f"rm /tmp/{file}.tgz")
        run(f"mv /data/web_static/releases/{file}/web_static/* "
            f"/data/web_static/releases/{file}/")
        run(f"rm -rf /data/web_static/releases/{file}/web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s /data/web_static/releases/{file}/ "
            f"/data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False
