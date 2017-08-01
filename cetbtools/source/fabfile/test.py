from fabric.api import local, task, execute


@task(default=True)
def all():
    """
    run all of the tests
    """

    execute(flake8)
    execute(unittest)


@task
def flake8():
    """
    run flake8 syntax checking
    """

    local("flake8 --config .flake8rc $(find . -name '*.py') --verbose")


@task
def unittest():
    """
    run unittests using nose
    """

    local("nosetests --verbose --exclude-dir=recipe")
