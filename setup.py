from setuptools import setup, find_packages

setup(
        name='pipenv-devcheck',
        version='0.1',
        author='neighborhoods.com',
        maintainer='George Wood (@Geoiv)',
        license="MIT",
        description="""
        Checks compatibility between developer dependencies used as used by
        Pipenv and user dependencies as specified in setup.py.
        """,
        packages=find_packages(),
        install_requires=[
        ],
        scripts=["bin/pipenv-devcheck"]
     )
