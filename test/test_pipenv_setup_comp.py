import pytest

from pipenv_devcheck.pipenv_setup_comp import (extract_deps_text,
                                               deps_text_to_dict,
                                               name_equality_check,
                                               version_check)


def test_extract_deps_text_setup():
    """
    Tests that setup.py dependencies are successfully read and extracted into
    a single string
    """
    setup_lines = [
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
    expected_deps_text = (
        "                'matplotlib>=3.1.1',\n"
        "                'numpy>=1.17.2',\n"
        "                'pandas>=0.25.1',\n"
        "                'seaborn>=0.9.0',\n"
        "                'simple_salesforce>=0.74.3'\n"
    )

    setup_deps_text = extract_deps_text(setup_lines, "setup")
    assert setup_deps_text == expected_deps_text


def test_extract_deps_text_pipfile():
    """
    Tests that Pipfile dependencies are successfully read and extracted into
    a single string
    """
    pipfile_lines = [
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
    expected_deps_text = (
        'matplotlib = "=>3.1.1, <=3.1.2"\n'
        'numpy = "==1.17.2"\n'
        'pandas = "==0.25.1"\n'
        'seaborn = "==0.9.0"\n'
        'simple_salesforce = "==0.74.3"\n'
    )

    pipfile_deps_text = extract_deps_text(pipfile_lines, "pipfile")
    assert pipfile_deps_text == expected_deps_text


def test_deps_text_to_dict_setup():
    """
    Tests that setup.py dependencies are successfully
    translated to a dictionary
    """
    deps_text = (
        "                'matplotlib>=3.1.1',\n"
        "                'numpy>=1.17.2',\n"
        "                'pandas>=0.25.1',\n"
        "                'seaborn>=0.9.0',\n"
        "                'simple_salesforce>=0.74.3'\n"
    )

    expected_dep_dict = {
        "matplotlib": [(">=", "3.1.1")],
        "numpy": [(">=", "1.17.2")],
        "pandas": [(">=", "0.25.1")],
        "seaborn": [(">=", "0.9.0")],
        "simple_salesforce": [(">=", "0.74.3")]
    }

    dep_dict = deps_text_to_dict(deps_text, "setup")
    assert dep_dict == expected_dep_dict


def test_deps_text_to_dict_pipfile():
    """
    Tests that Pipfile dependencies are successfully translated to a dictionary
    """
    deps_text = (
        'matplotlib = "=>3.1.1, <=3.1.2"\n'
        'numpy = "==1.17.2"\n'
        'pandas = "==0.25.1"\n'
        'seaborn = "==0.9.0"\n'
        'simple_salesforce = "==0.74.3"\n'
    )
    expected_dep_dict = {
        "matplotlib": [("=>", "3.1.1"), ("<=", "3.1.2")],
        "numpy": [("==", "1.17.2")],
        "pandas": [("==", "0.25.1")],
        "seaborn": [("==", "0.9.0")],
        "simple_salesforce": [("==", "0.74.3")]
    }

    dep_dict = deps_text_to_dict(deps_text, "pipfile")
    assert dep_dict == expected_dep_dict


def test_name_equality_check_valid():
    """
    Tests that no errors are raised when no name discrepancies are present
    """
    setup_deps = {
        "matplotlib": [(">=", "3.1.1")],
        "numpy": [(">=", "1.17.2")],
        "pandas": [(">=", "0.25.1")],
        "seaborn": [(">=", "0.9.0")],
        "simple_salesforce": [(">=", "0.74.3")]
    }
    pipfile_deps = {
        "matplotlib": [("=>", "3.1.1"), ("<=", "3.1.2")],
        "numpy": [("==", "1.17.2")],
        "pandas": [("==", "0.25.1")],
        "seaborn": [("==", "0.9.0")],
        "simple_salesforce": [("==", "0.74.3")]
    }

    assert name_equality_check(setup_deps, pipfile_deps)


def test_name_equality_check_in_setup_not_pipfile():
    """
    Checks that the proper errors are raised when a dependency name is present
    in setup.py but not in the Pipfile
    """
    setup_deps = {
        "matplotlib": [(">=", "3.1.1")],
        "numpy": [(">=", "1.17.2")],
        "pandas": [(">=", "0.25.1")],
        "seaborn": [(">=", "0.9.0")],
        "simple_salesforce": [(">=", "0.74.3")]
    }
    pipfile_deps = {
        "matplotlib": [("=>", "3.1.1"), ("<=", "3.1.2")],
        "numpy": [("==", "1.17.2")],
        "seaborn": [("==", "0.9.0")],
        "simple_salesforce": [("==", "0.74.3")]
    }

    with pytest.raises(ValueError) as excinfo:
        name_equality_check(setup_deps, pipfile_deps)
    assert excinfo.match("Dependencies in setup")
    assert excinfo.match("not in Pipfile")
    assert excinfo.match("pandas")


def test_name_equality_check_in_pipfile_not_setup():
    """
    Checks that the proper errors are raised when a dependency name is present
    in the Pipfile but not in setup.py
    """
    setup_deps = {
        "matplotlib": [(">=", "3.1.1")],
        "numpy": [(">=", "1.17.2")],
        "seaborn": [(">=", "0.9.0")],
        "simple_salesforce": [(">=", "0.74.3")]
    }
    pipfile_deps = {
        "matplotlib": [("=>", "3.1.1"), ("<=", "3.1.2")],
        "numpy": [("==", "1.17.2")],
        "pandas": [("==", "0.25.1")],
        "seaborn": [("==", "0.9.0")],
        "simple_salesforce": [("==", "0.74.3")]
    }

    with pytest.raises(ValueError) as excinfo:
        name_equality_check(setup_deps, pipfile_deps)
    assert excinfo.match("Dependencies in Pipfile")
    assert excinfo.match("not in setup")
    assert excinfo.match("pandas")


def test_name_equality_check_dual_mismatch():
    """
    Checks that the correct errors are raised when there is a two-sided
    discrepancy in dependency names
    """
    setup_deps = {
        "matplotlib": [(">=", "3.1.1")],
        "numpy": [(">=", "1.17.2")],
        "seaborn": [(">=", "0.9.0")],
        "simple_salesforce": [(">=", "0.74.3")]
    }
    pipfile_deps = {
        "numpy": [("==", "1.17.2")],
        "pandas": [("==", "0.25.1")],
        "seaborn": [("==", "0.9.0")],
        "simple_salesforce": [("==", "0.74.3")]
    }

    with pytest.raises(ValueError) as excinfo:
        name_equality_check(setup_deps, pipfile_deps)
    assert excinfo.match("Dependencies in Pipfile")
    assert excinfo.match("not in setup")
    assert excinfo.match(r"not in setup.py:\W*pandas")
    assert excinfo.match("Dependencies in setup")
    assert excinfo.match("not in Pipfile")
    assert excinfo.match(r"not in Pipfile:\W*matplotlib")


def test_version_check_valid():
    """
    Tests that the version_check passes in a valid situation
    """
    setup_deps = {
        "matplotlib": [(">=", "3.1.1")],
        "numpy": [(">=", "1.17.2")],
        "pandas": [(">=", "0.25.1")],
        "seaborn": [(">=", "0.9.0")],
        "simple_salesforce": [(">=", "0.74.3")]
    }
    pipfile_deps = {
        "matplotlib": [("=>", "3.1.1"), ("<=", "3.1.2")],
        "numpy": [("==", "1.17.2")],
        "pandas": [("==", "0.25.1")],
        "seaborn": [("==", "0.9.0")],
        "simple_salesforce": [("==", "0.74.3")]
    }

    assert version_check(setup_deps, pipfile_deps)


def test_version_check_invalid():
    """
    Tests that the version_check fails in an invalid situation
    """
    setup_deps = {
        "matplotlib": [(">=", "3.1.1")],
        "numpy": [(">=", "1.17.2")],
        "pandas": [(">=", "0.25.1")],
        "seaborn": [(">=", "0.9.0")],
        "simple_salesforce": [(">=", "0.74.3")]
    }
    pipfile_deps = {
        "matplotlib": [("=>", "3.1.1"), ("<=", "3.1.2")],
        "numpy": [("==", "1.17.2")],
        "pandas": [("<", "0.25.1")],
        "seaborn": [("<", "0.8.0")],
        "simple_salesforce": [("==", "0.74.3")]
    }

    with pytest.raises(ValueError) as excinfo:
        version_check(setup_deps, pipfile_deps)
    excinfo.match("Dependency discrepancies")
    excinfo.match("pandas")
    excinfo.match("seaborn")
    excinfo.match("pandas, seaborn")
