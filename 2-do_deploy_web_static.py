#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['54.173.134.61', '54.89.133.85']

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    """
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split('/')[-1]
        no_ext_name = file_name.split('.')[0]
        remote_path = "/data/web_static/releases/{}".format(no_ext_name)

        # uploads the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(file_name))

        # uncompress the archive to the folder on the web server
        run("mkdir -p {}".format(remote_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, remote_path))

        # deletes the archive from the web server
        run("rm /tmp/{}".format(file_name))

        # moves the content of the uncompressed folder to the proper location
        run("mv {}/web_static/* {}/".format(remote_path, remote_path))
        run("rm -rf {}/web_static".format(remote_path))

        # delets the symbolic link /data/web_static/current from webserver
        run("rm -rf /data/web_static/current")

        # creates a new symbolic link /data/web_static/current on webserver
        run("ln -s {} /data/web_static/current".format(remote_path))

        return True
    except Exception as e:
        return False
