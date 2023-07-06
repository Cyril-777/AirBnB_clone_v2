#!/usr/bin/python3
"""write a Fabric script that generates a .tgz archive
from the contents of the web_static folder"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    generates a .tgz archive from the contents of the web_static folder.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.succeeded:
        return archive_path
    else:
        return None
