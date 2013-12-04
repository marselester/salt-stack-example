# coding: utf-8
"""
fabfile
~~~~~~~

It is responsible for initialization of deployment.

The following example shows how to deploy ``development`` Salt environment
to Virtual Machine from scratch::

    $ fab setup_masterless_minion
    $ fab salt_env:development deploy

``setup_masterless_minion`` is only needed the first time.

"""
from fabric.api import env, task, run, runs_once, sudo, put, cd, abort
from fabric.contrib.project import upload_project
from fabric.contrib.files import exists


# Where to deploy?
env.hosts = ['vagrant@salt-hello-world']
# Use Vagrant's ssh key.
env.key_filename = '~/.vagrant.d/insecure_private_key'
# Here we will store Salt environment's name which is given by user.
env.salt_env_name = None


@task
@runs_once
def salt_env(name):
    """Which Salt environment to deploy?

    There are following Salt environments:

    - ``development`` -- contains well known credentials and libraries
      which facilitate development.
    - ``production`` -- contains production credentials.

    """
    if name in ('development', 'production'):
        env.salt_env_name = name
    else:
        abort('Unknown Salt environment.')


@task
@runs_once
def bootstrap_salt():
    """Bootstraps Salt installation."""
    with cd('/tmp/'):
        run('wget -O - http://bootstrap.saltstack.org | sudo sh')


@task
@runs_once
def update_minion_config():
    """Updates minion's config and restarts ``salt-minion`` service."""
    put('salt/minion.conf', '/etc/salt/minion', use_sudo=True, mode=0600)

    sudo('chown root:root /etc/salt/minion')

    sudo('service salt-minion restart')


@task
@runs_once
def update_state_and_pillar_files():
    """Updates state and pillar files by uploading them to ``/srv/salt_roots``.

    First it checks whether folder is present. If folder present it will
    be deleted.

    After all ``salt_roots`` folder is uploaded to ``/srv`` and
    owner is changed to root.

    """
    if exists('/srv/salt_roots'):
        sudo('rm -rf /srv/salt_roots')

    upload_project('salt/salt_roots', '/srv', use_sudo=True)

    sudo('chown root:root -R /srv/salt_roots')
    sudo('chmod 600 -R /srv/salt_roots')


@task
@runs_once
def setup_masterless_minion():
    """Prepares server to be able to run Salt commands."""
    bootstrap_salt()
    update_state_and_pillar_files()
    update_minion_config()


@task
@runs_once
def deploy():
    """Deploys infrastructure based on given environment."""
    if env.salt_env_name is None:
        abort('Salt environment has to be specified.')

    update_state_and_pillar_files()

    sudo("salt-call state.highstate env={salt_env_name}".format(
        salt_env_name=env.salt_env_name))
