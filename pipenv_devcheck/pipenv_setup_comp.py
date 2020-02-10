import ast
from packaging.version import parse as parse_version
import pipfile
import re

from pipenv_devcheck.check_fns import check_fn_mapping
from pipenv_devcheck.regexps import setup_exp, spec_exp, split_exp


def compare_deps():
    """
    Main wrapper around reading dependencies and running all checks

    Returns:
        tuple<dict<str, list<tuple<str, str>>>:
            Dictionaries of the dependencies found in setup.py and the Pipfile
    """
    setup_deps = get_setup_deps()
    pipfile_deps = get_pipfile_deps()
    run_checks(setup_deps, pipfile_deps)
    return setup_deps, pipfile_deps


def get_setup_deps():
    """
    Parses dependencies from setup.py and
    returns them as a dictionary

    Returns:
        tuple<dict<str, list<tuple<str, str>>>:
            Dictionaries of the dependencies found in setup.py
    """
    setup_deps_str = read_setup()

    setup_deps = {}
    for dep in setup_deps_str:
        parsed_dep = re.findall(setup_exp, dep)
        if len(parsed_dep):
            parsed_dep = parsed_dep[0]
            setup_deps.update({parsed_dep[0]: [spec for spec in parsed_dep[1:]
                                               if spec != ""]})
        else:
            setup_deps.update({dep: ["*"]})

    setup_deps = split_ops_and_versions(setup_deps)
    return setup_deps


def read_setup():
    """
    Reads dependencies from setup.py and does preprocessing

    Returns:
        list<str>: A list of the dependency lines from setup.py
    """
    filename = "setup.py"
    with open(filename, "r") as f:
        setup_tree = ast.parse(f.read(), filename)
    for node in ast.walk(setup_tree):
        is_setup_node = (hasattr(node, "func") and
                         hasattr(node.func, "id") and
                         node.func.id == "setup")
        if is_setup_node:
            setup_node = node

    for kw in setup_node.keywords:
        if kw.arg == "install_requires":
            setup_deps_str = ast.literal_eval(kw.value)
            return setup_deps_str


def get_pipfile_deps():
    """
    Parses dependencies from  Pipfile and
    returns them as a dictionary

    Returns:
        tuple<dict<str, list<tuple<str, str>>>:
            Dictionaries of the dependencies found in the Pipfile
    """
    pipfile_deps = read_pipfile()
    for dep in pipfile_deps.keys():
        dep_spec = pipfile_deps[dep]
        pipfile_deps[dep] = re.findall(spec_exp, dep_spec)

    pipfile_deps = split_ops_and_versions(pipfile_deps)

    return pipfile_deps


def read_pipfile():
    """
    Reads dependencies from Pipfile and does preprocessing

    Returns:
        dict<str, str>: A dict of the dependencies in Pipfile, from
        package name keys to version specification values
    """
    filename = "Pipfile"
    pipfile_data = pipfile.load(filename).data
    pipfile_deps = pipfile_data["default"]
    return pipfile_deps


def split_ops_and_versions(deps):
    """
    Splits string values in dependency dictionary into tuples containing
    separate strings for the operator and the version

    Args:
        deps (dict<str, list<str>>):
            Dependency dictionary with strings containing both operators
            and versions as values
    Returns:
        tuple<dict<str, list<tuple<str, str>>>:
            Dependency dictionary with operator/version string values split
            into tuples
    """
    for dep in deps.keys():
        specs = deps[dep]
        if not (len(specs) == 1 and specs[0] == "*"):
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
            if not setup_op == "*":
                setup_version = parse_version(setup_dep_spec[1])

                check_fn = check_fn_mapping[setup_op]
                check_args = {}
                if setup_op not in ["==", "!="]:
                    check_args["setup_op"] = setup_op
                check_args["setup_version"] = setup_version

                for pipfile_dep_spec in pipfile_dep_specs:
                    pipfile_op = pipfile_dep_spec[0]
                    if not pipfile_op == "*":
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
