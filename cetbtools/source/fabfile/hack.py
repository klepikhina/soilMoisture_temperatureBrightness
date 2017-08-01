import re
import os

# Need some routines in both version and deploy.
# These will go away when continuum fixes their packages.
# fix_package_name will be deleted and conda_version_filename and
# current_version will go back into version

# This is a static file written after a build to store the full name and path
# of the last build.

CONDA_ARTIFACT_FILENAME = '__conda_artifact_name__.txt'


def correct_artifact_name(artifact_filename):
    with open(artifact_filename, 'r') as fn:
        pkg_location = fn.read().strip()
        pkg_location = fix_package_name(pkg_location)

    with open(artifact_filename, 'w') as fn:
        fn.write(pkg_location)


def tag():
    return "v{}".format(current_version())


def conda_version_filename(directory=None):
    ''' filename where the conda version file would normally go.
    '''
    if directory is None:
        directory = os.getcwd()
    conda_filename = os.path.join(directory, '__conda_version__.txt')
    return conda_filename


def fix_package_name(conda_build_location):
    '''currently conda build recipe --output doesn't consider if the default
      version of the package was over ridden by the use of a
      __conda_version__.txt file which is how we control our dev packages.
      Until this issue is fixed,
      https://github.com/Anaconda-Server/anaconda-build/issues/82, we will
      have to build/guess at the correct package to upload to anaconda.org.
    '''
    try:
        with open(conda_version_filename(), 'r') as cvf:
            build_version = cvf.read().strip()
            base = os.path.basename(conda_build_location)
            directory = os.path.dirname(conda_build_location)
            base = base.replace(current_version(), build_version)
            conda_build_location = os.path.join(directory, base)
    except IOError:
        # don't worry if you couldn't open the file because it didn't
        # exist, you don't need to relocate the package name.
        pass

    return conda_build_location


def current_version(version_fn='.bumpversion.cfg'):
    ''' read current version from .bumpversion.cfg with bumpversion '''
    matcher = re.compile('current_version *= *(\d+\.\d+\.\d+)')
    with open(version_fn, 'r') as vf:
        for line in vf.readlines():
            match = matcher.match(line)
            if match is not None:
                return match.groups()[0]

    raise Exception('The current version was not found in version file {0}'.format(version_fn))


def write_conda_version_file(extension, directory=None):
    with open(conda_version_filename(directory), 'w') as fp:
        fp.write(current_version() + extension)
