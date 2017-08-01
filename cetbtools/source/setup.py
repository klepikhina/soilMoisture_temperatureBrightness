from setuptools import setup, find_packages

setup(name='cetbtools',
      version='0.0.12',
      description='Python tools from the NSIDC Passive Microwave ESDR project',
      url='git@bitbucket.org:nsidc/cetbtools.git',
      author='NSIDC PMESDR Team',
      author_email='brodzik@nsidc.org',
      license='GPLv3',
      packages=find_packages(exclude=('fabfile',)))
