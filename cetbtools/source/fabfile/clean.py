import subprocess

from fabric.api import local, task

import hack


def remove_anaconda_dev(project, token):
    ''' cleans development packages from anaconda.org
    '''
    dev_pkg_version = "{0}{1}".format(hack.current_version(), 'dev')
    cmd = 'anaconda -t {token} remove nsidc/{project}/{version} --force'.format(
        token=token, project=project, version=dev_pkg_version)
    subprocess.call(cmd, shell=True)


@task(default=True)
def clean():
    """
    clean the project directories
    """
    local('find . -name "*.pyc" -exec rm -rf {} \;')


@task()
def remove_dev_packages(project, token):
    '''Remove from repository any dev packages that exist for the release (as
    defined by the .bumpversion.cfg)
    '''
    remove_anaconda_dev(project, token)
