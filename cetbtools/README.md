cetbtools
---

## Getting Started

If this is a new project you will need to complete the following steps (assuming you just created this from the cookiecutter template):

1. Add the actual project source in `/source/cetbtools`
2. Edit `/source/recipe/meta.yaml` adding entry points and/or test commands, and dependencies.
3. Create a `environment.yaml` from a conda environment: `conda env export > environment.yaml`
4. Add any runtime commands to `/source/fabfile/run.py`
5. Build a CI machine and test that everything is working.
6. Remove this `Getting Started` section.

## Development Quickstart

This project uses [conda](http://conda.pydata.org/miniconda.html) python. It must be installed to run the tool.

1. Clone the repository
2. `cd cetbtools/source`
3. `conda env create --file environment.yaml`
4. `. activate cetbtools`

## Development/Release Workflow

This project uses [github flow](https://guides.github.com/introduction/flow/). To begin a feature, start a branch and update the version with the `fab version.bump([major|minor|patch])` command. This will allow you to set the version for the expected next release.

### Continuous Integration

On a merge to master the CI jobs will run a do the following:

1. `CI` Clone repository and checkout reference (default: `master`)
2. `CI` Create build a `dev` conda package, that is labeled {version}dev
3. `CI` Deploy the package to anaconda.org (or local_nsidc) on the `dev` channel
4. `CI` Provision an `Integration` VM
5. `CI` Install the `dev` package to the `Integration` VM
6. `CI` Run all tests for the package on `Integration`.

When a package is ready to be tested. Manually run the first `RC` job triggering this chain:

1. `RC` Clone repository and checkout reference (default: `master`)
2. `RC` Create build a conda package, that is labeled {version}
3. `RC` Deploy the package to anaconda.org (or local_nsidc) on the `dev` channel
4. `RC` Provision an `QA` VM
5. `RC` Install the `RC` package to the `QA` VM
6. `RC` Run all tests for the package on `QA`.

### Create A Release

When satisfied with the testing of the RC job, and are ready to create a production release. From Jenkins manually run the first RELEASE job.
The following will run:

1. `RELEASE` Clone repository and Checkout TAG to release
2. `RELEASE` Create build a conda package, labeled {version}
3. `RELEASE` Deploy the package to anaconda.org (or local_nsidc) on the `main` channel
4. `RELEASE` Clean up all `dev` packages of this release on the `dev` channel.


### Ending A Project

An IMPLODE job has been provided and should be used when the package work is completed. The job will attempt to destroy all of the vm's and the notify you to destroy the CI vm.
