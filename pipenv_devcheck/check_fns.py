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


def check_equality(setup_version, pipfile_op, pipfile_version):
    return operators[pipfile_op](setup_version, pipfile_version)


def check_inequality(setup_version, pipfile_op, pipfile_version):
    inclusive_ops = ["==", ">=", "=>", "<="]
    return not (pipfile_op in inclusive_ops and
                setup_version == pipfile_version)


def check_range(setup_op, setup_version, pipfile_op, pipfile_version):
    gt_ops = [">", ">=", "=>"]
    lt_ops = ["<", "<="]

    same_op_class = ((setup_op in gt_ops and pipfile_op in gt_ops) or
                     (setup_op in lt_ops and pipfile_op in lt_ops))
    if same_op_class:
        return True
    return (operators[setup_op](pipfile_version, setup_version) and
            operators[pipfile_op](setup_version, pipfile_version))


check_fn_mapping = {
    "==": check_equality,
    "!=": check_inequality,
    ">=": check_range,
    "=>": check_range,
    "<=": check_range,
    "<": check_range,
    ">": check_range
}
