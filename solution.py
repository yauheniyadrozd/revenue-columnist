import re

import pandas


def add_virtual_column(df: pandas.DataFrame, role: str, new_column: str) -> pandas.DataFrame:
    label = r"[A-Za-z_]+"

    for column in df.columns:
        if not re.fullmatch(label, str(column)):
            return pandas.DataFrame()

    if not re.fullmatch(label, new_column):
        return pandas.DataFrame()

    tokens = re.split(r"([+\-*])", role.strip())
    operands = tokens[0::2]
    operators = tokens[1::2]

    if len(operands) != len(operators) + 1:
        return pandas.DataFrame()

    expression = ""
    for index, operand in enumerate(operands):
        operand = operand.strip()
        if not re.fullmatch(label, operand) or operand not in df.columns:
            return pandas.DataFrame()
        expression += "`" + operand + "`"
        if index < len(operators):
            expression += operators[index]

    result = df.copy()
    try:
        result[new_column] = result.eval(expression)
    except Exception:
        return pandas.DataFrame()

    return result
