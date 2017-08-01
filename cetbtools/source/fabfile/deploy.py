import os

from fabric.api import local, task

import hack

NSIDC_LOCAL = '/share/sw/packages/python/conda'


def get_package_info():
    """
    read the package information from the conda build artifact
    """

    with open(hack.CONDA_ARTIFACT_FILENAME, 'r') as fn:
        pkg_location = fn.read().strip()
        pkg_name = os.path.basename(pkg_location)

    return pkg_location, pkg_name


@task(default=True)
def anaconda(channel, token):
    """
    deploy package to anaconda.org
    """

    pkg_location, pkg_name = get_package_info()
    pkg_dir, _ = os.path.split(pkg_location)
    pkg_root = pkg_dir.replace('linux-64', '')

    osx_location = pkg_location.replace('linux-64', 'osx-64')

    cmd = 'anaconda -t {token} upload -u nsidc {location} -c {channel} --force && '
    cmd += 'conda convert {location} -p osx-64 -o {root} &&'
    cmd += 'anaconda -t {token} upload -u nsidc {osx_location} -c {channel} --force'
    local(cmd.format(location=pkg_location,
                     name=pkg_name,
                     channel=channel,
                     root=pkg_root,
                     token=token,
                     osx_location=osx_location))
