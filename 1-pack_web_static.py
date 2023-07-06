#!/usr/bin/python3
"""write a Fabric script that generates a .tgz archive
from the contents of the web_static folder"""
from fabric.api import local
from time import strftime


def do_pack():
    """
    generates a .tgz archive from the contents of the web_static folder.
    """
    filename = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(filename))

        return "versions/web_static_{}.tgz".format(filename)

    except Exception as e:
        return None
