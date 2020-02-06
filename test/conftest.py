import pytest


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
def deps_from_read():
    """Section of pipfile that is specific to dependencies"""
    return {
        "matplotlib": [">=3.1.1", "<=3.1.2"],
        "numpy": ["==1.17.2"],
        "pandas": ["==0.25.1"],
        "seaborn": ["==0.9.0"],
        "simple_salesforce": ["==0.74.3"]
    }
