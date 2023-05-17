def is_complex(value):
    _complex = (dict, set, list, tuple)
    return '[complex value]' if isinstance(value, _complex) else value


def make_quotes(value):
    if isinstance(value, str) and value not in {'null', 'true', 'false'}:
        return f"'{value}'"
    else:
        return is_complex(value)


def generate_added(key, value, path):
    return f'Property "{path}{key}" was added with value: ' \
                          f'{make_quotes(value["value"])}\n'


def generate_updated(key, path, value):
    return f'Property "{path}{key}" was updated. ' \
              f'From {make_quotes(value["new"])} to ' \
              f'{make_quotes(value["old"])}\n'


def generate_removed(key, path):
    return f'Property "{path}{key}" was removed. '


def gen_plain_string(_dict):
    result = ''

    def _iter(_dict: dict, path='') -> None:
        nonlocal result

        for key, value in sorted(_dict.items()):
            new_path = path
            status = value.get('status')

            if status == 'added':
                result += generate_added(key, value, path)

            elif status == 'removed':
                result += generate_removed(key, path)

            elif status == 'nested':
                sub_path = f'{key}.'
                new_path += sub_path
                _iter(value, new_path)

        return result

    return _iter(_dict)
