from typing import Any, Tuple


def traverse_dict(dict_: dict, keys: Tuple[str, ...]) -> Any:
    """Traverse a dict, going deeper for every key in a tuple."""
    value = dict_

    for key in keys:
        value = value[key]

    return value
