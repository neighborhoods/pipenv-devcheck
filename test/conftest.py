import pytest


@pytest.fixture
def setup_lines():
    """Full setup.py file as a list of strings"""
    return [
         "from setuptools import setup, find_packages\n",
         "\n",
         "setup(\n",
         "        name='demo_setup',\n",
         "        version='0.0',\n",
         "        author='neighborhoods.com',\n",
         "        maintainer='George Wood',\n",
         "        description='Demo setup file',\n",
         '        packages=find_packages(),\n',
         '        install_requires=[\n',
         "                'matplotlib>=3.1.1',\n",
         "                'numpy>=1.17.2',\n",
         "                'pandas>=0.25.1',\n",
         "                'seaborn>=0.9.0',\n",
         "                'simple_salesforce>=0.74.3'\n",
         '        ]\n',
         '     )\n'
    ]


@pytest.fixture
def setup_deps_text():
    """Section of setup.py that is specific to dependencies"""
    return (
        "                'matplotlib>=3.1.1',\n"
        "                'numpy>=1.17.2',\n"
        "                'pandas>=0.25.1',\n"
        "                'seaborn>=0.9.0',\n"
        "                'simple_salesforce>=0.74.3'\n"
    )


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
def pipfile_lines():
    """Full Pipfile file as a list of strings"""
    return [
            '[[source]]\n',
            'name = "pypi"\n',
            'url = "https://pypi.org/simple"\n',
            'verify_ssl = true\n',
            '\n',
            '[packages]\n',
            'matplotlib = "=>3.1.1, <=3.1.2"\n',
            'numpy = "==1.17.2"\n',
            'pandas = "==0.25.1"\n',
            'seaborn = "==0.9.0"\n',
            'simple_salesforce = "==0.74.3"\n',
            '\n',
            '[requires]\n',
            'python_version = "3.7"\n'
    ]


@pytest.fixture
def pipfile_deps_text():
    """Section of pipfile that is specific to dependencies"""
    return (
        'matplotlib = "=>3.1.1, <=3.1.2"\n'
        'numpy = "==1.17.2"\n'
        'pandas = "==0.25.1"\n'
        'seaborn = "==0.9.0"\n'
        'simple_salesforce = "==0.74.3"\n'
    )


@pytest.fixture
def pipfile_deps():
    """Pipfile dependencies extracted from a string into a dict"""
    return {
            "matplotlib": [("=>", "3.1.1"), ("<=", "3.1.2")],
            "numpy": [("==", "1.17.2")],
            "pandas": [("==", "0.25.1")],
            "seaborn": [("==", "0.9.0")],
            "simple_salesforce": [("==", "0.74.3")]
        }
