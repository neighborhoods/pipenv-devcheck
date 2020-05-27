from pipenv_devcheck.check_fns import (check_equality, check_inequality,
                                       check_range)


def test_same_range_op_class_compatibility():
    """
    Tests for same range operator class compatibility.
    Operators in the same class (e.g. both '<'/'<=', or
    both '>'/'>='/'=>' tha never directly conflict.
    """
    assert check_range(">", "0.24.1", "=>", "0.25.1")
    assert check_range("=>", "0.24.1", ">=", "0.25.1")
    assert check_range("<", "0.24.1", "<=", "0.25.1")


def test_valid_range():
    """
    Tests that compatible version ranges pass checks
    """
    assert check_range(">", "1.2.3", "<=", "4.5.6")
    assert check_range("<=", "4.5.6", ">", "1.2.3")


def test_invalid_range():
    """
    Tests that incompatible version ranges fail checks
    """
    assert not check_range(">=", "4.5.6", "<", "1.2.3")
    assert not check_range("<=", "1.2.3", ">", "4.5.6")


def test_valid_equality():
    """
    Tests that compatible version equalities pass checks -
    includes a case where 'left_op' if provided
    """
    assert check_equality(left_op='==', left_version="1.2.3",
                          right_op="<", right_version="3.2.1")
    assert check_equality("1.2.3", "==", "1.2.3")


def test_invalid_equality():
    """
    Tests that incompatible version equalities fail checks
    """
    assert not check_equality("1.2.3", "<", "1.2.3")
    assert not check_equality("1.2.3", "!=", "1.2.3")


def test_valid_inequality():
    """
    Tests that compatible version inequalities pass checks -
    includes a case where 'left_op' if provided
    """
    assert check_inequality(left_op="!=", left_version="1.2.3",
                            right_op=">", right_version="1.2.3")
    assert check_inequality("1.2.3", "==", "4.5.6")


def test_invalid_inequality():
    """
    Tests that incompatible version inequalities fail checks
    """
    assert not check_inequality("1.2.3", "=>", "1.2.3")
    assert not check_inequality("1.2.3", "==", "1.2.3")
