#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['54.173.134.61', '54.89.133.85']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
        """Distributes an archive to the web servers.
        """
        try:
                if not (path.exists(archive_path)):
                        return False

                # uploads the archive to /tmp/ directory of the web server
                put(archive_path, '/tmp/')

                # create target dir
                file_name = archive_path[-18:-4]
                run('sudo mkdir -p /data/web_static/\
releases/web_static_{}/'.format(file_name))

                # uncompress the archive to the folder on the web server
                run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}/'
                    .format(file_name, file_name))

                # deletes the archive from the web server
                run('sudo rm /tmp/web_static_{}.tgz'.format(file_name))

                # moves the content of the uncompressed folder
                run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(file_name, file_name))

                # remove extraneous web_static dir
                run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'
                    .format(file_name))

                # delets the sym link /data/web_static/current from webserver
                run('sudo rm -rf /data/web_static/current')

                # creates a new symbolic link /data/web_static/current on webserver
                run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(file_name))
        except:
                return False
        return True
