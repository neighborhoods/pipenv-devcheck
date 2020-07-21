import pytest

from pipenv_devcheck.pipenv_setup_comp import (
    read_setup, read_pipfile, get_setup_deps, get_pipfile_deps,
    split_ops_and_versions, name_equality_check, version_check,
    extras_equality_check)


def test_read_setup(mocker, setup_text, setup_deps_from_read):
    """
    Tests that setup.py reading functions as expected
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=setup_text))
    read_results = read_setup()
    assert read_results == setup_deps_from_read


def test_read_pipfile(mocker, pipfile_text, pipfile_deps_from_read):
    """
    Tests that Pipfile reading functions as expected
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=pipfile_text))
    read_results = read_pipfile()
    print(read_results)
    assert read_results == pipfile_deps_from_read


def test_get_setup_deps(mocker, setup_deps_from_read, setup_deps_and_extras):
    """
    Tests that dependencies are properly read and parsed from a setup.py file

    Args:
        setup_deps_and_extras (dict<str, list<tuple<str, str>>>),
                               pytest.fixture):
            setup.py dependencies extracted from a string into a dict
    """
    mocker.patch("pipenv_devcheck.pipenv_setup_comp.read_setup",
                 return_value=setup_deps_from_read)
    actual_deps_and_extras = get_setup_deps()
    assert actual_deps_and_extras == setup_deps_and_extras


def test_get_pipfile_deps(mocker, pipfile_deps_from_read,
                          pipfile_deps_and_extras):
    """
    Tests that dependencies are properly read and parsed from a Pipfile

    Args:
        pipfile_deps_and_extras (dict<str, list<tuple<str, str>>>),
                                 pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    mocker.patch("pipenv_devcheck.pipenv_setup_comp.read_pipfile",
                 return_value=pipfile_deps_from_read)
    actual_deps_and_extras = get_pipfile_deps()
    assert actual_deps_and_extras == pipfile_deps_and_extras


def test_split_ops_and_versions(deps_unsplit, pipfile_deps_and_extras):
    """
    Tests that dependency specification strings (operator and version) are
    properly split into a tuple

    Args:
        deps_from_read (dict<str, list<str>>, pytest.fixture):
            Dependencies as they would be returned by
            either read_setup or read_pipfile
        pipfile_deps_and_extras (dict<str, list<tuple<str, str>>>),
                                 pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    pipfile_deps = pipfile_deps_and_extras[0]
    actual_deps = split_ops_and_versions(deps_unsplit)
    assert actual_deps == pipfile_deps


def test_name_equality_check_valid(setup_deps_and_extras,
                                   pipfile_deps_and_extras):
    """
    Tests that no errors are raised when no name discrepancies are present

    Args:
        setup_deps_and_extras (dict<str, list<tuple<str, str>>>),
                               pytest.fixture):
            setup.py dependencies extracted from a string into a dict
        pipfile_deps_and_extras (dict<str, list<tuple<str, str>>>),
                                 pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    setup_deps = setup_deps_and_extras[0]
    pipfile_deps = pipfile_deps_and_extras[0]
    assert name_equality_check(setup_deps, pipfile_deps)


def test_name_equality_check_in_setup_not_pipfile(setup_deps_and_extras,
                                                  pipfile_deps_and_extras):
    """
    Checks that the proper errors are raised when a dependency name is present
    in setup.py but not in the Pipfile

    Args:
        setup_deps_and_extras (dict<str, list<tuple<str, str>>>),
                               pytest.fixture):
            setup.py dependencies extracted from a string into a dict
        pipfile_deps_and_extras (dict<str, list<tuple<str, str>>>),
                                 pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    setup_deps = setup_deps_and_extras[0]
    pipfile_deps = pipfile_deps_and_extras[0]
    del pipfile_deps["pandas"]

    with pytest.raises(ValueError) as excinfo:
        name_equality_check(setup_deps, pipfile_deps)
    assert excinfo.match("Dependencies in setup")
    assert excinfo.match("not in Pipfile")
    assert excinfo.match("pandas")


def test_name_equality_check_in_pipfile_not_setup(setup_deps_and_extras,
                                                  pipfile_deps_and_extras):
    """
    Checks that the proper errors are raised when a dependency name is present
    in the Pipfile but not in setup.py

    Args:
        setup_deps_and_extras (dict<str, list<tuple<str, str>>>),
                               pytest.fixture):
            setup.py dependencies extracted from a string into a dict
        pipfile_deps (dict<str, list<tuple<str, str>>>), pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    setup_deps = setup_deps_and_extras[0]
    pipfile_deps = pipfile_deps_and_extras[0]
    del setup_deps["seaborn"]

    with pytest.raises(ValueError) as excinfo:
        name_equality_check(setup_deps, pipfile_deps)
    assert excinfo.match("Dependencies in Pipfile")
    assert excinfo.match("not in setup")
    assert excinfo.match("seaborn")


def test_name_equality_check_dual_mismatch(setup_deps_and_extras,
                                           pipfile_deps_and_extras):
    """
    Checks that the correct errors are raised when there is a two-sided
    discrepancy in dependency names

    Args:
        setup_deps_and_extras (dict<str, list<tuple<str, str>>>),
                               pytest.fixture):
            setup.py dependencies extracted from a string into a dict
        pipfile_deps_and_extras (dict<str, list<tuple<str, str>>>),
                                 pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    setup_deps = setup_deps_and_extras[0]
    pipfile_deps = pipfile_deps_and_extras[0]
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


def test_version_check_valid(setup_deps_and_extras, pipfile_deps_and_extras):
    """
    Tests that the version_check passes in a valid situation

    Args:
        setup_deps_and_extras (dict<str, list<tuple<str, str>>>),
                               pytest.fixture):
            setup.py dependencies extracted from a string into a dict
        pipfile_deps_and_extras (dict<str, list<tuple<str, str>>>),
                                 pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    setup_deps = setup_deps_and_extras[0]
    pipfile_deps = pipfile_deps_and_extras[0]
    assert version_check(setup_deps, pipfile_deps)


def test_version_check_invalid(setup_deps_and_extras, pipfile_deps_and_extras):
    """
    Tests that the version_check fails in an invalid situation

    Args:
        setup_deps_and_extras (dict<str, list<tuple<str, str>>>),
                               pytest.fixture):
            setup.py dependencies extracted from a string into a dict
        pipfile_deps_and_extras (dict<str, list<tuple<str, str>>>),
                                 pytest.fixture):
            Pipfile dependencies extracted from a string into a dict
    """
    setup_deps = setup_deps_and_extras[0]
    pipfile_deps = pipfile_deps_and_extras[0]
    pipfile_deps["pandas"][0] = ("<", "0.25.1")
    pipfile_deps["seaborn"][0] = ("<", "0.8.0")

    with pytest.raises(ValueError) as excinfo:
        version_check(setup_deps, pipfile_deps)
    excinfo.match("Dependency discrepancies")
    excinfo.match("pandas")
    excinfo.match("seaborn")
    excinfo.match("pandas, seaborn")


def test_extras_equality_check_valid(test_extras):
    """
    Tests that the extras_equality_check passes in a valid situation.

    Args:
        test_extras (dict<str, str>, pytest.fixture):
            A valid dict of package extras as would be passed to
            'extras_equality_check'
    """
    assert extras_equality_check(test_extras, test_extras)


def test_extras_equality_check_invalid_missingdep(test_extras):
    """
    Tests that the extras_equality_check fails when there is a difference
    in which packages have extras specified

    Args:
        test_extras (dict<str, str>, pytest.fixture):
            A valid dict of package extras as would be passed to
            'extras_equality_check'
    """
    setup_extras = test_extras.copy()
    del setup_extras['testpackage']
    pipenv_extras = test_extras.copy()
    with pytest.raises(KeyError,
                       match='discrepancy in what packages have extras'):
        assert extras_equality_check(setup_extras, pipenv_extras)


def test_extras_equality_check_invalid_mismatched_extras(test_extras):
    """
    Tests that the extras_equality_check fails when the packages with extras
    match, but the extras themselves differ

    Args:
        test_extras (dict<str, str>, pytest.fixture):
            A valid dict of package extras as would be passed to
            'extras_equality_check'
    """
    setup_extras = test_extras.copy()
    setup_extras['pyhive'] = ['hive']
    pipenv_extras = test_extras.copy()
    with pytest.raises(ValueError,
                       match='mismatched package extras'):
        assert extras_equality_check(setup_extras, pipenv_extras)
