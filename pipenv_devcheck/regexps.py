from pipenv_devcheck.check_fns import operators

# Matches one of any of the operators specified in the operators map
ops_exp = "(?:"
for i in range(len(list(operators.keys()))):
    ops_exp += list(operators.keys())[i]
    if i != len(list(operators.keys())) - 1:
        ops_exp += "|"
ops_exp += ")"

# Matches version numbers
# TODO - Add support for letters, like in beta releases?
version_exp = r"[\d.]+"

# Captures a full specification - an operator and a version.
spec_exp = r"(\s*" + ops_exp + r"\s*" + version_exp + "|\\*)"
# Captures a full specification, capturing the operator and version separately
split_exp = "(" + ops_exp + r")\s*(" + version_exp + ")"
# Captures any additional specifications beyond the first one
addtl_spec_exp = r"(?:," + spec_exp + ")?"

# Full expression for matching dependencies in setup.py
setup_exp = (
    r"([\w|\-]*)" +
    spec_exp +
    addtl_spec_exp +
    addtl_spec_exp
)
