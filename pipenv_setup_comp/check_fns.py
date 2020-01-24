#!/usr/bin/env python
import operator

operators = {
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    "=>": operator.ge,
    "<=": operator.le,
    "<": operator.lt,
    ">": operator.gt
}


def check_equality(setup_dep_op, setup_dep_version,
                   pipfile_dep_op, pipfile_dep_version):
    return operators[pipfile_dep_op](setup_dep_version, pipfile_dep_version)


def check_inequality(setup_dep_op, setup_dep_version,
                     pipfile_dep_op, pipfile_dep_version):
    return not (pipfile_dep_op == "==" and
                setup_dep_version == pipfile_dep_version)


def check_range(setup_dep_op, setup_dep_version,
                pipfile_dep_op, pipfile_dep_version):
    gt_ops = [">", ">=", "=>"]
    lt_ops = ["<", "<="]

    same_op_class = ((setup_dep_op in gt_ops and pipfile_dep_op in gt_ops) or
                     (setup_dep_op in lt_ops and pipfile_dep_op in lt_ops))
    if same_op_class:
        return True
    return (operators[setup_dep_op](pipfile_dep_version, setup_dep_version) and
            operators[pipfile_dep_op](setup_dep_version, pipfile_dep_version))


check_fn_mapping = {
    "==": check_equality,
    "!=": check_inequality,
    ">=": check_range,
    "=>": check_range,
    "<=": check_range,
    "<": check_range,
    ">": check_range
}
