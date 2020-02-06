import operator


def check_equality(setup_version, pipfile_op, pipfile_version):
    """
    Checks for version compatibility when at least one specifies
    an exact version

    Args:
        setup_version (packaging.version.Version):
            The version specified in setup.py
        pipfile_op (str):
            The comparison operation specified in the Pipfile
        pipfile_version (packaging.version.Version):
            The version specified in the Pipfile
    Returns:
        bool: Whether or not the check passed
    """
    return operators[pipfile_op](setup_version, pipfile_version)


def check_inequality(setup_version, pipfile_op, pipfile_version):
    """
    Checks for version compatibility when at least one specifies
    an explicitly disallowed version

    Args:
        setup_version (packaging.version.Version):
            The version specified in setup.py
        pipfile_op (str):
            The comparison operation specified in the Pipfile
        pipfile_version (packaging.version.Version):
            The version specified in the Pipfile
    Returns:
        bool: Whether or not the check passed
    """
    inclusive_ops = ["==", ">=", "=>", "<="]
    return not (pipfile_op in inclusive_ops and
                setup_version == pipfile_version)


def check_range(setup_op, setup_version, pipfile_op, pipfile_version):
    """
    Checks for version compatibility when at least one specifies
    an exact version

    Args:
        setup_op (str):
            The comparison operation specified in setup.py
        setup_version (packaging.version.Version):
            The version specified in setup.py
        pipfile_op (str):
            The comparison operation specified in the Pipfile
        pipfile_version (packaging.version.Version):
            The version specified in the Pipfile
    Returns:
        bool: Whether or not the check passed
    """
    gt_ops = [">", ">=", "=>"]
    lt_ops = ["<", "<="]

    same_op_class = ((setup_op in gt_ops and pipfile_op in gt_ops) or
                     (setup_op in lt_ops and pipfile_op in lt_ops))
    if same_op_class:
        return True
    return (operators[setup_op](pipfile_version, setup_version) and
            operators[pipfile_op](setup_version, pipfile_version))


# Mapping from operator strings to comparison functions
operators = {
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    "<=": operator.le,
    "<": operator.lt,
    ">": operator.gt
}

# Mapping from operator strings to relevant comparison functions
check_fn_mapping = {
    "==": check_equality,
    "!=": check_inequality,
    ">=": check_range,
    "<=": check_range,
    "<": check_range,
    ">": check_range
}
