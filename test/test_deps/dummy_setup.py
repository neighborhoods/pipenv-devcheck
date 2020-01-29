from setuptools import setup, find_packages

setup(
        name='demo_setup',
        version='0.0',
        author='neighborhoods.com',
        maintainer='George Wood',
        description='Demo setup file',
        packages=find_packages(),
        install_requires=[
                'matplotlib>=3.1.1',
                'numpy>=1.17.2',
                'pandas>=0.25.1',
                'seaborn>=0.9.0',
                'simple_salesforce>=0.74.3'
        ]
     )
