import pytest


@pytest.fixture()
def setup_text():
    """setup.py text as would be returned by f.open().read()"""
    return """
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
    """


@pytest.fixture()
def setup_deps_from_read():
    """setup.py dependencies extracted from a string into a dict"""
    return [
        'matplotlib>=3.1.1',
        'numpy>=1.17.2',
        'pandas>=0.25.1',
        'seaborn>=0.9.0',
        'simple_salesforce>=0.74.3'
    ]


@pytest.fixture()
def setup_deps():
    """setup.py dependencies extracted from a string into a dict"""
    return {
            "matplotlib": [(">=", "3.1.1")],
            "numpy": [(">=", "1.17.2")],
            "pandas": [(">=", "0.25.1")],
            "seaborn": [(">=", "0.9.0")],
            "simple_salesforce": [(">=", "0.74.3")]
    }


@pytest.fixture
def pipfile_text():
    """Pipfile as would be returned by f.open().read()"""
    return """
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[packages]
matplotlib = ">=3.1.1, <=3.1.2"
numpy = "==1.17.2"
pandas = "==0.25.1"
seaborn = "==0.9.0"
simple_salesforce = "==0.74.3"

[requires]
python_version = "3.7"
    """


@pytest.fixture
def pipfile_deps_from_read():
    """Pipfile dependencies extracted from a string into a dict"""
    return {
            "matplotlib": ">=3.1.1, <=3.1.2",
            "numpy": "==1.17.2",
            "pandas": "==0.25.1",
            "seaborn": "==0.9.0",
            "simple_salesforce": "==0.74.3"
    }


@pytest.fixture
def pipfile_deps():
    """Pipfile dependencies extracted from a string into a dict"""
    return {
            "matplotlib": [(">=", "3.1.1"), ("<=", "3.1.2")],
            "numpy": [("==", "1.17.2")],
            "pandas": [("==", "0.25.1")],
            "seaborn": [("==", "0.9.0")],
            "simple_salesforce": [("==", "0.74.3")]
    }


@pytest.fixture
def deps_unsplit():
    """Section of pipfile that is specific to dependencies"""
    return {
        "matplotlib": [">=3.1.1", "<=3.1.2"],
        "numpy": ["==1.17.2"],
        "pandas": ["==0.25.1"],
        "seaborn": ["==0.9.0"],
        "simple_salesforce": ["==0.74.3"]
    }
