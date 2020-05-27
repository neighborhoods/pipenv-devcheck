import operator


def check_equality(left_version, right_op, right_version, **_):
    """
    Checks for version compatibility when the dependency for
    'left_version' has specified an exact version

    Args:
        left_version (packaging.version.Version):
            The version on the left side of the comparison
        right_op (str):
            The comparison operator to be used, associated with 'right_version'
        right_version (packaging.version.Version):
            The version on the right side of the comparison
        **_ (dict):
            Unused **kwargs. Present to allow this function to accept
            'left_op' arguments
    Returns:
        bool: Whether or not the check passed
    """
    return operators[right_op](left_version, right_version)


def check_inequality(left_version, right_op, right_version, **_):
    """
    Checks for version compatibility when the dependency for
    'left_version' has specified an explicitly disallowed version

    Args:
        left_version (packaging.version.Version):
            The version on the left side of the comparison
        right_op (str):
            The comparison operator to be used, associated with 'right_version'
        right_version (packaging.version.Version):
            The version on the right side of the comparison
        **_ (dict):
            Unused **kwargs. Present to allow this function to accept
            'left_op' arguments
    Returns:
        bool: Whether or not the check passed
    """
    inclusive_ops = ["==", ">=", "=>", "<="]
    return not (right_op in inclusive_ops and
                left_version == right_version)


def check_range(left_op, left_version, right_op, right_version):
    """
    Checks for version compatibility when the dependency for 'left_version'
    has specified a version range

    Args:
        left_op (str):
            A comparison operator, associated with 'left_version'
        left_version (packaging.version.Version):
            The version on the left side of the comparison
        right_op (str):
            A comparison operator, associated with 'right_version'
        right_version (packaging.version.Version):
            The version on the right side of the comparison
    Returns:
        bool: Whether or not the check passed
    """
    gt_ops = [">", ">=", "=>"]
    lt_ops = ["<", "<="]

    same_op_class = ((left_op in gt_ops and right_op in gt_ops) or
                     (left_op in lt_ops and right_op in lt_ops))
    if same_op_class:
        return True
    elif right_op == "==":
        return check_equality(right_version, left_op, left_version)
    elif right_op == "!=":
        return check_inequality(right_version, left_op, left_version)
    else:
        return (operators[left_op](right_version, left_version) and
                operators[right_op](left_version, right_version))


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
