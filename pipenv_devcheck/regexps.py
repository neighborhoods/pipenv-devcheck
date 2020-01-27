from pipenv_devcheck.check_fns import operators

ops_exp = "(?:"
for i in range(len(list(operators.keys()))):
    ops_exp += list(operators.keys())[i]
    if i != len(list(operators.keys())) - 1:
        ops_exp += "|"
ops_exp += ")"

version_exp = r"[\d.]+"

spec_exp = "(" + ops_exp + version_exp + ")"
addtl_spec_exp = r"(?:(?:,\s*)" + spec_exp + ")?"

setup_exp = (
    r"'([\w|\-]*)" +
    spec_exp +
    addtl_spec_exp +
    addtl_spec_exp +
    "'"
)

pipfile_exp = (
    r"([\w|\-]*)" +
    r"(?:\s*=\s*\")" +
    spec_exp +
    addtl_spec_exp +
    addtl_spec_exp +
    "\""
)
