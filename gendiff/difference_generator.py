from gendiff.formatters.stylish_formatter import format_stylish
from gendiff.formatters.plain_formatter import format_plain
from gendiff.formatters.json_formatter import format_json
from gendiff.parser import load_file


def build_diff(first_item: dict, second_item: dict) -> dict:
    """
    Builds and returns a dictionary that represents the differences
    between two input dictionaries
    """
    result = {}
    keys = sorted(set(first_item.keys()) | set(second_item.keys()))

    for key in keys:
        first_value = first_item.get(key)
        second_value = second_item.get(key)

        if isinstance(first_value, dict) and isinstance(second_value, dict):
            result[key] = {
                'value': build_diff(first_value, second_value),
                'status': 'nested'
            }

        # Only first value is present
        elif key in first_item and key not in second_item:
            result[key] = {
                'value': first_value,
                'status': 'removed'
            }

        # Only second value is present
        elif key in second_item and key not in first_item:
            result[key] = {
                'value': second_value,
                'status': 'added'
            }

        # Both values are present and identical
        elif first_value == second_value:
            result[key] = {
                'value': first_value,
                'status': 'unchanged'
            }

        # Both values are present but different
        else:
            result[key] = {
                'old_value': first_value,
                'new_value': second_value,
                'status': 'updated'
            }

    return result


def generate_diff(old: str, new: str, formatter='stylish') -> str:
    """
    Generates diff between two files and
    returns it as a string in specified format
    """
    formatters = {
        'stylish': format_stylish,
        'plain': format_plain,
        'json': format_json
    }

    diff = build_diff(load_file(old), load_file(new))
    format = formatters.get(formatter, format_stylish)

    return format(diff)
