from packaging.version import parse as parse_version
import re

from pipenv_devcheck.check_fns import check_fn_mapping
from pipenv_devcheck.regexps import ops_exp, setup_exp, pipfile_exp


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
    setup_lines, pipfile_lines = read_dep_files(setup_filename,
                                                pipfile_filename)

    setup_deps_text = extract_deps_text(setup_lines, "setup")
    pipfile_deps_text = extract_deps_text(pipfile_lines, "pipfile")
    setup_deps = deps_text_to_dict(setup_deps_text, "setup")
    pipfile_deps = deps_text_to_dict(pipfile_deps_text, "pipfile")

    run_checks(setup_deps, pipfile_deps)


def read_dep_files(setup_filename, pipfile_filename):
    """
    Reads text as an array of lines from files at specified names
    """
    with open(setup_filename, "r") as f:
        setup_lines = f.readlines()

    with open(pipfile_filename, "r") as f:
        pipfile_lines = f.readlines()

    return setup_lines, pipfile_lines


def extract_deps_text(lines, type):
    """
    Constructs a single string containing only dependencies from the lines of
    a dependency file

    Args:
        lines (list<str>):
            Array of lines from dependency file
        type (str):
            Type of dependency file the lines are sourced from
            (setup.py or Pipfile)
    Returns:
        str:
            A single string containing only the dependency section extracteed
            from a dependency file
    """
    deps_start_line = -1
    deps_end_line = -1
    is_setup = type == "setup"
    if is_setup:
        open_brackets = 0

    for i in range(len(lines)):
        if deps_end_line < 0:
            current_line = lines[i]

            if is_setup:
                start_cond = "install_requires" in current_line
                end_cond = open_brackets == 0
            else:
                start_cond = "[packages]" in current_line
                end_cond = (re.search(r"\[\w*\]", current_line) or
                            i == (len(lines) - 1))

            if deps_start_line > 0 and end_cond:
                deps_end_line = i - 1
            if start_cond:
                deps_start_line = i + 1

            if is_setup:
                open_brackets += current_line.count("[")
                open_brackets -= current_line.count("]")

    deps_joined = "".join(lines[deps_start_line:deps_end_line])
    return deps_joined


def deps_text_to_dict(deps_text, type):
    """
    Converts single string of dependencies to a dictionary from
    dependeny name keys to version specification values

    Args:
        deps_text (str):
            String containing the dependency-specific section
            of a dependency file
        type (str):
            What type of dependency file that deps_text was read from
            (setup.py or Pipfile)
    Returns:
        dict<str, list<tuple<str, str>>>:
                        Dictionary from dependency name keys to a list of
                        tuples as a value, with the tuples containing
                        a comparision operator and a version specification.
    """
    if type == "setup":
        exp = setup_exp
    elif type == "pipfile":
        exp = pipfile_exp
    deps = {}
    for dep in re.findall(exp, deps_text):
        dep_name = dep[0]
        dep_specs = [dep_spec for dep_spec in dep[1:] if dep_spec != ""]
        for dep_spec in dep_specs:
            op_end = re.match(ops_exp, dep_spec).end()
            deps[dep_name] = [(dep_spec[:op_end], dep_spec[op_end:])
                              for dep_spec in dep_specs]
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
