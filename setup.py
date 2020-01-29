from setuptools import setup, find_packages

setup(
        name='pipenv-devcheck',
        version='0.1',
        author='neighborhoods.com',
        maintainer='George Wood (@Geoiv)',
        description='Checks compatibility between developer/user dependencies',
        packages=find_packages(),
        install_requires=[
        ],
        scripts=["bin/pipenv-devcheck"]
     )
