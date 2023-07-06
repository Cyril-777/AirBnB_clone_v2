#!/usr/bin/python3
"""full deployment"""
from fabric.api import env, run
from fabric.operations import put
from fabric.contrib.files import exists
from datetime import datetime


# Web server IPs
env.hosts = ['54.173.134.61', '54.89.133.85']


def do_pack():
    """A script that generates an archive of
    the contents of the web_static folder"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    local("sudo mkdir -p versions")
    local("sudo tar -czvf {} web_static".format(archive_path))

    return (archive_path)


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress archive to the folder /data/web_static/releases/<archive
        # filename without extension> on the web server
        filename = archive_path.split('/')[-1]
        folder = '/data/web_static/releases/' + filename.split('.')[0]
        run('sudo mkdir -p {}'.format(folder))
        run('sudo tar -xzf /tmp/{} -C {}'.format(filename, folder))

        # Delete the archive from the web server
        run('sudo rm /tmp/{}'.format(filename))

        # Move the contents of the uncompressed folder to the proper location
        run('sudo mv {}/web_static/* {}/'.format(folder, folder))
        run('sudo rm -rf {}/web_static'.format(folder))

        # Delete the symbolic link /data/web_static/current from web server
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current on web server
        run('sudo ln -s {} /data/web_static/current'.format(folder))

        return True

    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()

    if not archive_path:
        return (False)

    return do_deploy(archive_path)

