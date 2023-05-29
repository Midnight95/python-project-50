def is_complex(value):
    """
    Checks if a value is a complex data type
    and returns '[complex value]' if True,
    otherwise returns the input value.
    """
    _complex = (dict, set, list, tuple)
    return '[complex value]' if isinstance(value, _complex) else value


def make_quotes(value):
    """
    Adds single quotes to a string value and returns it.
    If the value is 'null', 'true' or 'false',
    it returns the input value without quotes.
    If the value is a complex data type,
    it calls the is_complex() function to format it.
    """
    if isinstance(value, str) and value not in {'null', 'true', 'false'}:
        return f"'{value}'"
    else:
        return is_complex(value)


def generate_added(key: str, value, path: str) -> str:
    """
    Generates a message indicating that a property has been added
    """
    return f'Property \'{path}{key}\' was added with value: ' \
        f'{make_quotes(value["value"])}\n'


def generate_updated(key: str, value, path: str) -> str:
    """
    Generates a message indicating that a property has been updated
    """
    return f'Property \'{path}{key}\' was updated. ' \
        f'From {make_quotes(value["old_value"])} to ' \
        f'{make_quotes(value["new_value"])}\n'


def generate_removed(key: str, path: str) -> str:
    """
    Generates a message indicating that a property has been removed
    """
    return f'Property \'{path}{key}\' was removed\n'


def format_plain(_dict):  # noqa C901
    """
    Generates a plain text string that summarizes the differences
    between two dictionaries. Returns the string output.
    """
    result = ''

    def _iter(_dict: dict, path='') -> str:
        nonlocal result

        for key, value in _dict.items():
            new_path = path
            status = value.get('status')

            if status == 'added':
                result += generate_added(key, value, path)

            elif status == 'updated':
                result += generate_updated(key, value, path)

            elif status == 'removed':
                result += generate_removed(key, path)

            elif status == 'nested':
                sub_path = f'{key}.'
                new_path += sub_path
                _iter(value['value'], new_path)

        return result

    return _iter(_dict)[:-1]
