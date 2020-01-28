from packaging.version import parse as parse_version
import re

from pipenv_devcheck.check_fns import check_fn_mapping
from pipenv_devcheck.regexps import ops_exp, setup_exp, pipfile_exp


def compare_deps(setup_filename="setup.py", pipfile_filename="Pipfile"):
    setup_lines, pipfile_lines = read_dep_files(setup_filename,
                                                pipfile_filename)

    # setup_deps_text = extract_setup_deps_text(setup_lines)
    # pipfile_deps_text = extract_pipfile_deps_text(pipfile_lines)
    setup_deps_text = extract_deps_text(setup_lines, "setup")
    pipfile_deps_text = extract_deps_text(pipfile_lines, "pipfile")
    setup_deps = deps_text_to_dict(setup_deps_text, "setup")
    pipfile_deps = deps_text_to_dict(pipfile_deps_text, "pipfile")

    run_checks(setup_deps, pipfile_deps)
    return setup_deps, pipfile_deps


def read_dep_files(setup_filename, pipfile_filename):
    with open(setup_filename, "r") as f:
        setup_lines = f.readlines()

    with open(pipfile_filename, "r") as f:
        pipfile_lines = f.readlines()

    return setup_lines, pipfile_lines


def extract_deps_text(lines, type):
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
    name_equality_check(setup_deps, pipfile_deps)
    version_check(setup_deps, pipfile_deps)


def name_equality_check(setup_deps, pipfile_deps):
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
