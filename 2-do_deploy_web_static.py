#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import put, run, env
from os import path

env.hosts = ['54.173.134.61', '54.89.133.85']
env.user = 'ubuntu'

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    """
    if not path.exists(archive_path):
        return False

    try:
        # uploads the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # uncompress the archive to the folder releases/<archive
        # filename without extension> on the web server
        file = archive_path.split('/')[-1]
        folder = '/data/web_static/releases/' + file.split('.')[0]
        run('mkdir -p {}'.format(folder))
        run('tar -xzf /tmp/{} -C {}'.format(file, folder))

        # deletes the archive from the web server
        run('rm /tmp/{}'.format(file))

        # moves the content of the uncompressed folder to the proper location
        run('mv {}/web_static/* {}/'.format(folder, folder))
        run('rm -rf {}/web_static'.format(folder))

        # delets the symbolic link /data/web_static/current from webserver
        run('rm -rf /data/web_static/current')

        # creates a new symbolic link /data/web_static/current on webserver
        run('ln -s {} /data/web_static/current'.format(folder))
        return True

    except Exception as e:
        return False
