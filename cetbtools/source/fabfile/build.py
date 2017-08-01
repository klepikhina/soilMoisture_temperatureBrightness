from fabric.api import local, task

import hack


@task(default=True)
def build(recipe, decorator=None):
    """
    build the conda package

    recipe = location of the conda recipe

    decorator = suffix that is applied to the build package. This should be
    None to name the package as is. or 'dev' to add a dev extension
    """
    if decorator is not None:
        hack.write_conda_version_file(decorator)

    # generate the build
    cmd = 'conda build {recipe}'.format(recipe=recipe)
    local(cmd)

    # generate the build artifact
    artifact = '--output > {0}'.format(hack.CONDA_ARTIFACT_FILENAME)
    cmd += ' {artifact}'.format(artifact=artifact)
    local(cmd)

    hack.correct_artifact_name(hack.CONDA_ARTIFACT_FILENAME)
