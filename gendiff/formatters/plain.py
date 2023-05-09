CHANGE_INDICATORS = ['  - ', '  + ']


def is_complex(value):
    if type(value) in (dict, set, list, tuple):
        return '[complex value]'
    else:
        return value


def generate_added(key, value, path):
    return f"Property '{path}{key[4:]}' was added with value " \
                          f"{is_complex(value)}\n"


def generate_removed_or_removed(key, path, value, _dict):
    added_key = CHANGE_INDICATORS[1] + key[4:]
    if added_key in _dict:
        return f"Property '{path}{key[4:]}' was updated. " \
                  f"From with {is_complex(value)} to " \
                  f"{is_complex(_dict[added_key])}\n"
    else:
        return f"Property '{path}{key[4:]}' was removed\n"





def gen_plain_string(_dict):
    result = ''
    removed, added = CHANGE_INDICATORS

    def _iter(_dict: dict, path=None) -> None:
        if path is None:
            path = ''
        nonlocal result

        for key, value in _dict.items():
            if key[4:] in result:
                continue

            if key.startswith(added):
                result += generate_added(key, value, path)

            elif key.startswith(removed):
                result += generate_removed_or_removed(key, path, value, _dict)

            elif isinstance(value, dict):
                path += f'{key[4:]}.'
                _iter(value, path)

    _iter(_dict)
    return result

'''
Property 'common.follow' was added with value: false
Property 'common.setting2' was removed
Property 'common.setting3' was updated. From true to null
Property 'common.setting4' was added with value: 'blah blah'
Property 'common.setting5' was added with value: [complex value]
Property 'common.setting6.doge.wow' was updated. From '' to 'so much'
Property 'common.setting6.ops' was added with value: 'vops'
Property 'group1.baz' was updated. From 'bas' to 'bars'
Property 'group1.nest' was updated. From [complex value] to 'str'
Property 'group2' was removed
Property 'group3' was added with value: [complex value]
'''