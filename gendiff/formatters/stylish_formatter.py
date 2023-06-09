INDENT = 4


def make_value(data, depth: int):
    """
    Returns a string representation of a nested dictionary
    """
    if isinstance(data, bool):
        return str(data).lower()

    if data is None:
        return 'null'

    if not isinstance(data, dict):
        return data

    res = '{'
    for key, value in data.items():
        res += f'\n{" " * (depth + 1) * INDENT}{key}:' \
               f' {make_value(value, depth + 1)}'
    res += f'\n{" " * depth * INDENT}}}'

    return res


def make_stylish_string(_dict: dict, depth: int) -> str:
    """
    Iterates over a dictionary recursively
    and returns a formatted string representation
    """
    result = ''

    for key, val in _dict.items():
        status = val.get('status')

        if status == 'updated':
            result += f'{" " * depth * INDENT}' \
                      f'{" " * (INDENT - 2) + "- "}{key}:' \
                      f' {make_value(val["old_value"], depth + 1)}\n'
            result += f'{" " * depth * INDENT}' \
                      f'{" " * (INDENT - 2) + "+ "}{key}:' \
                      f' {make_value(val["new_value"], depth + 1)}\n'

        elif status == 'nested':
            result += f'{" " * (depth + 1) * INDENT}{key}: {{\n' \
                      f'{make_stylish_string(val["value"], depth + 1)}' \
                      f'{" " * (depth + 1) * INDENT}}}\n'

        elif status == 'removed':
            result += f'{" " * depth * INDENT}' \
                      f'{" " * (INDENT - 2) + "- "}{key}: ' \
                      f'{make_value(val["value"], depth + 1)}\n'

        elif status == 'added':
            result += f'{" " * depth * INDENT}' \
                      f'{" " * (INDENT - 2) + "+ "}{key}: ' \
                      f'{make_value(val["value"], depth + 1)}\n'

        else:
            result += f'{" " * (depth + 1) * INDENT}{key}: ' \
                      f'{make_value(val["value"], depth + 1)}\n'

    return result


def format_stylish(diff: dict) -> str:
    """
    Returns a string representation of the differences between two dictionaries
    """
    result = make_stylish_string(diff, 0)
    return f'{{\n{result}}}'
