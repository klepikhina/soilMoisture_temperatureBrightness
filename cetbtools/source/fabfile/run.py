from fabric.api import local, task


@task(default=True)
def run():
    """
    runs a command
    """
    local("echo 'running a command!'")
