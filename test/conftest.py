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
                'pyhive[hive, presto]>=0.6.0',
                'pandas[fake_extra]>=0.25.1',
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
        'pyhive[hive, presto]>=0.6.0',
        'pandas[fake_extra]>=0.25.1',
        'seaborn>=0.9.0',
        'simple_salesforce>=0.74.3'
    ]


@pytest.fixture()
def setup_deps_and_extras():
    """setup.py dependencies extracted from a string into a dict"""
    return (
        {
            "matplotlib": [(">=", "3.1.1")],
            "pyhive": [(">=", "0.6.0")],
            "pandas": [(">=", "0.25.1")],
            "seaborn": [(">=", "0.9.0")],
            "simple_salesforce": [(">=", "0.74.3")]
        },
        {
            "pyhive": ["hive", "presto"],
            "pandas": ["fake_extra"]
        }
    )


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
pyhive = {extras = ["hive", "presto"], version = "==0.6.1"}
pandas = {extras = ["fake_extra"], version = "==0.25.1"}
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
            "pyhive": {"extras": ["hive", "presto"], "version": "==0.6.1"},
            "pandas": {"extras": ["fake_extra"], "version": "==0.25.1"},
            "seaborn": "==0.9.0",
            "simple_salesforce": "==0.74.3"
    }


@pytest.fixture
def pipfile_deps_and_extras():
    """Pipfile dependencies extracted from a string into a dict"""
    return (
        {
            "matplotlib": [(">=", "3.1.1"), ("<=", "3.1.2")],
            "pyhive": [("==", "0.6.1")],
            "pandas": [("==", "0.25.1")],
            "seaborn": [("==", "0.9.0")],
            "simple_salesforce": [("==", "0.74.3")]
        },
        {
            "pyhive": ["hive", "presto"],
            "pandas": ["fake_extra"]
        }
    )


@pytest.fixture
def deps_unsplit():
    """Section of pipfile that is specific to dependencies"""
    return {
        "matplotlib": [">=3.1.1", "<=3.1.2"],
        "pyhive": ["==0.6.1"],
        "pandas": ["==0.25.1"],
        "seaborn": ["==0.9.0"],
        "simple_salesforce": ["==0.74.3"]
    }


@pytest.fixture
def test_extras():
    """
    A valid dict of extras as would be returned by 'get_setup_deps'
    or 'get_pipfile_deps'
    """
    return {
        'pyhive': ['hive', 'presto'],
        'testpackage': ['extra0', 'extra1']
    }
