from fabric.api import local, task

import hack


@task
def tag():
    cmd = 'git tag {tag} --force && git push --tags --force'.format(tag=hack.tag())
    local(cmd)


@task
def bump(part='patch'):
    cmd = ("bumpversion {0}".format(part))
    local(cmd)
