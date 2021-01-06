#!/usr/bin/env python
import os
import subprocess
import sys
from shutil import rmtree

from github import Github
from setuptools import setup, find_packages, Command


here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "pipenv_devcheck", "_version.py"), "r") as f:
    exec(f.read(), about)

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


# Adapted from: https://github.com/navdeep-G/setup.py/blob/master/setup.py
# (Public domain software)
class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(
                  sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        returned_error = os.system('twine upload dist/* ')
        if returned_error:
            raise ValueError('Pushing to PyPi failed.')

        self.status('Pushing git tags…')
        current_commit = str(
            subprocess.check_output(['git', 'rev-parse', 'HEAD']),
            'utf-8').strip()

        g = Github(os.getenv('GITHUB_PAT'))
        repo = g.get_repo('neighborhoods/' + about['__title__'])
        repo.create_git_tag_and_release(
            tag=about['__version__'],
            tag_message='',
            release_name=about['__version__'],
            release_message='',
            object=current_commit,
            type='commit'
        )

        sys.exit()


setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=about["__license__"],
    packages=find_packages(),
    install_requires=[
        'packaging>=20.1',
        'pipfile>=0.0.2'
    ],
    entry_points={
        'console_scripts': [
            'pipenv-devcheck=pipenv_devcheck.__main__:main',
        ],
    },
    cmdclass={
        'upload': UploadCommand,
    }
 )
