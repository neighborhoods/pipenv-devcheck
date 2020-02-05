import importlib
from packaging.version import parse as parse_version
import re
import pipfile
from unittest import mock

from pipenv_devcheck.check_fns import check_fn_mapping
from pipenv_devcheck.regexps import setup_exp, spec_exp, split_exp


def compare_deps(setup_filename="setup.py", pipfile_filename="Pipfile"):
    """

    Args:
        setup_filename (str, default "setup.py"):
            Location/name of file to be used as setup.py
        pipfile_filename (str, default "Pipfile"):
            Location/name of file to be used as Pipfile
    Returns:
        tuple<str, str>:
            Dictionaries of the dependencies found in setup.py and the Pipfile
    """
    setup_deps, pipfile_deps = new()
    print(setup_deps)
    print(pipfile_deps)
    run_checks(setup_deps, pipfile_deps)
    return setup_deps, pipfile_deps


def new():
    with mock.patch("setuptools.setup") as mock_setup:
        exec(compile(open("setup.py", "rb").read(), "setup.py", 'exec'))
    print(mock_setup.call_args)
    args, kwargs = mock_setup.call_args
    setup_deps_str = kwargs["install_requires"]
    print(setup_deps_str)
    setup_deps = {}
    for dep in setup_deps_str:
        parsed_dep = re.findall(setup_exp, dep)[0]
        setup_deps.update({parsed_dep[0]: [spec for spec in parsed_dep[1:]
                                           if spec != ""]})

    pipfile_data = pipfile.load("Pipfile").data
    pipfile_deps = pipfile_data["default"]
    for dep in pipfile_deps.keys():
        dep_spec = pipfile_deps[dep]
        pipfile_deps[dep] = re.findall(spec_exp, dep_spec)

    setup_deps = split_ops_and_versions(setup_deps)
    pipfile_deps = split_ops_and_versions(pipfile_deps)

    return setup_deps, pipfile_deps


def split_ops_and_versions(deps):
    for dep in deps.keys():
        specs = deps[dep]
        deps[dep] = [re.findall(split_exp, spec)[0] for spec in specs]
    return deps


def run_checks(setup_deps, pipfile_deps):
    """
    Runs all currently implemented checks
    """
    name_equality_check(setup_deps, pipfile_deps)
    version_check(setup_deps, pipfile_deps)


def name_equality_check(setup_deps, pipfile_deps):
    """
    Checks that all names present in either dependency file are present
    in both dependency files

    Args:
        setup_deps (dict<str, list<tuple<str, str>>>):
            Dictionary from setup.py dependency name keys to a list of
            tuples as a value, with the tuples containing
            a comparision operator and a version specification.
        pipfile_deps (dict<str, list<tuple<str, str>>>):
            Dictionary from Pipfile dependency name keys to a list of
            tuples as a value, with the tuples containing
            a comparision operator and a version specification.
    Returns:
        bool:
            Whether the check passes - will always be true, otherwise the
            function will not reach this line.
    Raises:
        ValueError:
            If there are discrepancies between version names
    """
    in_setup_not_pipfile = set(setup_deps.keys()).difference(
        set(pipfile_deps.keys()))
    in_pipfile_not_setup = set(pipfile_deps.keys()).difference(
        set(setup_deps.keys()))
    if len(in_setup_not_pipfile) or len(in_pipfile_not_setup):
        err_msg = "Dependency name mismatch!\n"
        if len(in_setup_not_pipfile):
            err_msg += ("Dependencies in setup.py but not in Pipfile: " +
                        str(in_setup_not_pipfile) + "\n")
        if len(in_pipfile_not_setup):
            err_msg += ("Dependencies in Pipfile but not in setup.py: " +
                        str(in_pipfile_not_setup) + "\n")
        raise ValueError(err_msg)
    return True


def version_check(setup_deps, pipfile_deps):
    """
    Checks that the dependency specifications in either dependency file are
    fully compatibile with those in the other

    Args:
        setup_deps (dict<str, list<tuple<str, str>>>):
            Dictionary from setup.py dependency name keys to a list of
            tuples as a value, with the tuples containing
            a comparision operator and a version specification.
        pipfile_deps (dict<str, list<tuple<str, str>>>):
            Dictionary from Pipfile dependency name keys to a list of
            tuples as a value, with the tuples containing
            a comparision operator and a version specification.
    Returns:
        bool:
            Whether the check passes - will always be true, otherwise the
            function will not reach this line.
    Raises:
        ValueError:
            If there are discrepancies between version specifications
    """
    problem_deps = []
    for dep_name, setup_dep_specs in setup_deps.items():
        pipfile_dep_specs = pipfile_deps[dep_name]

        for setup_dep_spec in setup_dep_specs:
            setup_op = setup_dep_spec[0]
            setup_version = parse_version(setup_dep_spec[1])

            check_fn = check_fn_mapping[setup_op]
            check_args = {}
            if setup_op not in ["==", "!="]:
                check_args["setup_op"] = setup_op
            check_args["setup_version"] = setup_version

            for pipfile_dep_spec in pipfile_dep_specs:
                pipfile_op = pipfile_dep_spec[0]
                pipfile_version = parse_version(pipfile_dep_spec[1])
                check_args["pipfile_op"] = pipfile_op
                check_args["pipfile_version"] = pipfile_version

                if not check_fn(**check_args):
                    problem_deps.append(dep_name)

    if len(problem_deps):
        raise ValueError(
            "Dependency discrepancies between Pipfile and setup.py "
            "are present in the following packages: " +
            ", ".join(problem_deps))
    return True
