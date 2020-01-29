import pytest

from pipenv_devcheck.pipenv_setup_comp import (extract_deps_text,
                                               deps_text_to_dict,
                                               name_equality_check,
                                               version_check)


def test_extract_deps_text_setup(setup_lines, setup_deps_text):
    """
    Tests that setup.py dependencies are successfully read and extracted into
    a single string

    Args:
        setup_lines (list<str>, pytest.fixture):
            Full setup.py file as a list of strings
        setup_deps_text (str, pytest.fixture):
            Section of setup.py that is specific to dependencies
    """
    expected_deps_text = setup_deps_text

    actual_deps_text = extract_deps_text(setup_lines, "setup")
    assert actual_deps_text == expected_deps_text


def test_extract_deps_text_pipfile(pipfile_lines, pipfile_deps_text):
    """
    Tests that Pipfile dependencies are successfully read and extracted into
    a single string

    Args:
        pipfile_lines (list<str>, pytest.fixture):
            Full Pipfile as a list of strings
        pipfile_deps_text (str, pytest.fixture):
            Section of Pipfile that is specific todependencies
    """
    expected_deps_text = pipfile_deps_text

    actual_deps_text = extract_deps_text(pipfile_lines, "pipfile")
    assert actual_deps_text == expected_deps_text


def test_deps_text_to_dict_setup(setup_deps_text, setup_deps):
    """
    Tests that setup.py dependencies are successfully
    translated to a dictionary

    Args:
        setup_deps_text (str, pytest.fixture):
           Section of setup.py that is specific to dependencies
        setup_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
           setup.py dependencies extracted from a string into a dict
    """
    expected_dep_dict = setup_deps

    dep_dict = deps_text_to_dict(setup_deps_text, "setup")
    assert dep_dict == expected_dep_dict


def test_deps_text_to_dict_pipfile(pipfile_deps_text, pipfile_deps):
    """
    Tests that Pipfile dependencies are successfully translated to a dictionary

    Args:
        pipfile_deps_text (str, pytest.fixture):
            Section of Pipfile that is specific to dependencies
        pipfile_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    expected_dep_dict = pipfile_deps

    dep_dict = deps_text_to_dict(pipfile_deps_text, "pipfile")
    assert dep_dict == expected_dep_dict


def test_name_equality_check_valid(setup_deps, pipfile_deps):
    """
    Tests that no errors are raised when no name discrepancies are present

    Args:
        setup_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            setup.py dependencies extracted from a string into a dict
        pipfile_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    assert name_equality_check(setup_deps, pipfile_deps)


def test_name_equality_check_in_setup_not_pipfile(setup_deps, pipfile_deps):
    """
    Checks that the proper errors are raised when a dependency name is present
    in setup.py but not in the Pipfile

    Args:
        setup_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            setup.py dependencies extracted from a string into a dict
        pipfile_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    del pipfile_deps["pandas"]

    with pytest.raises(ValueError) as excinfo:
        name_equality_check(setup_deps, pipfile_deps)
    assert excinfo.match("Dependencies in setup")
    assert excinfo.match("not in Pipfile")
    assert excinfo.match("pandas")


def test_name_equality_check_in_pipfile_not_setup(setup_deps, pipfile_deps):
    """
    Checks that the proper errors are raised when a dependency name is present
    in the Pipfile but not in setup.py

    Args:
        setup_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            setup.py dependencies extracted from a string into a dict
        pipfile_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    del setup_deps["seaborn"]

    with pytest.raises(ValueError) as excinfo:
        name_equality_check(setup_deps, pipfile_deps)
    assert excinfo.match("Dependencies in Pipfile")
    assert excinfo.match("not in setup")
    assert excinfo.match("seaborn")


def test_name_equality_check_dual_mismatch(setup_deps, pipfile_deps):
    """
    Checks that the correct errors are raised when there is a two-sided
    discrepancy in dependency names

    Args:
        setup_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            setup.py dependencies extracted from a string into a dict
        pipfile_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    del setup_deps["pandas"]
    del pipfile_deps["matplotlib"]

    with pytest.raises(ValueError) as excinfo:
        name_equality_check(setup_deps, pipfile_deps)
    assert excinfo.match("Dependencies in Pipfile")
    assert excinfo.match("not in setup")
    assert excinfo.match(r"not in setup.py:\W*pandas")
    assert excinfo.match("Dependencies in setup")
    assert excinfo.match("not in Pipfile")
    assert excinfo.match(r"not in Pipfile:\W*matplotlib")


def test_version_check_valid(setup_deps, pipfile_deps):
    """
    Tests that the version_check passes in a valid situation

    Args:
        setup_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            setup.py dependencies extracted from a string into a dict
        pipfile_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    assert version_check(setup_deps, pipfile_deps)


def test_version_check_invalid(setup_deps, pipfile_deps):
    """
    Tests that the version_check fails in an invalid situation

    Args:
        setup_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            setup.py dependencies extracted from a string into a dict
        pipfile_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    pipfile_deps["pandas"][0] = ("<", "0.25.1")
    pipfile_deps["seaborn"][0] = ("<", "0.8.0")

    with pytest.raises(ValueError) as excinfo:
        version_check(setup_deps, pipfile_deps)
    excinfo.match("Dependency discrepancies")
    excinfo.match("pandas")
    excinfo.match("seaborn")
    excinfo.match("pandas, seaborn")
