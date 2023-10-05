#!/usr/bin/python3
""" This module contains do_pack function
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
      Generates a .tgz archive from the contents of the web_static
      folder of your AirBnB Clone repo
      Returns:
          the archive path if the archive has been correctly generated.
          Otherwise, it should return None
    """
    d = datetime.now()
    file_name = f"web_static_{d.year}{d.month}{d.day}\
                  {d.hour}{d.minute}{d.second}.tgz"
    local("mkdir -p versions")
    res = local(f"tar -cvzf versions/{file_name} web_static", )
    if res.succeeded:
        return f"versions/{file_name}"
    else:
        return None
