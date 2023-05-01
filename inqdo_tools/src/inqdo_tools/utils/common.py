"""
Commmon functions
=================
"""


import base64
import copy
import json
import os
from functools import reduce
from operator import itemgetter
from typing import Any, List, Tuple, Union

if "DEBUG_INQDO_TOOLS" in os.environ.keys():  # pragma: no cover
    from utils.error import ErrorHandler
    from utils.json import Json
else:
    from inqdo_tools.utils.error import ErrorHandler
    from inqdo_tools.utils.json import Json


@ErrorHandler.base_exception
def dict_set(dictionary: dict, keys: list, value: Any, deepcopy=False) -> dict:
    """
    Sets a value in a nested dictionary using a list of keys.

    :param dictionary: The dictionary to update.
    :type dictionary: dict

    :param keys: List of keys that determine the path to the nested dictionary.
    :type keys: list

    :param value: The value to set.
    :type value: any

    :param deepcopy: Optional flag that determines whether to create a deep copy of the dictionary.
    :type deepcopy: bool

    :return: The updated dictionary.
    :rtype: dict
    """
    d = dictionary
    if deepcopy:
        d = copy.deepcopy(dictionary)

    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value

    return d


@ErrorHandler.base_exception
def lower_key_dict(d: dict) -> dict:
    """Function to lower all the dict keys

    :rtype: dict
    """
    return {k.lower(): v for k, v in d.items()}


@ErrorHandler.base_exception
def dict_get_forced(
    dictionary: dict, keys: Union[Tuple[str], List[str]], default=None
) -> Union[dict, Any]:
    """
    Retrieves a value from a nested dictionary using a list of keys.

    :param dictionary: The dictionary to search.
    :type dictionary: dict

    :param keys: List of keys that determine the path to the nested value.
    :type keys: list

    :param default: Optional default value to return if the key is not found.
    :type default: any

    :return: The value at the specified path or the default value.
    :rtype: Union[dict, any]
    """
    value = lower_key_dict(d=dictionary)

    for p in keys:
        converted_value = lower_key_dict(d=value)
        if p.lower() in converted_value:
            value = converted_value[p.lower()]
        elif default is not None:
            return default
        else:
            print(f'Could not find "{p}" for path [{keys}].')

    return value


@ErrorHandler.base_exception
def dict_get(dictionary: dict, keys: list, default=None) -> Union[dict, Any]:
    """
    Retrieves a value from a nested dictionary using a list of keys.

    :param dictionary: The dictionary to search.
    :type dictionary: dict

    :param keys: List of keys that determine the path to the nested value.
    :type keys: list

    :param default: Optional default value to return if the key is not found.
    :type default: any

    :return: The value at the specified path or the default value.
    :rtype: Union[dict, any]
    """
    response = default
    try:
        response = reduce(lambda d, key: d.get(key) if d else default, keys, dictionary)
    except Exception:
        pass

    return response if response is not None else default


@ErrorHandler.base_exception
def from_json(s: str) -> dict:
    loaded = json.loads(s)

    if type(loaded) == str:
        loaded = json.loads(loaded)

    return loaded


@ErrorHandler.base_exception
def to_json(d: dict) -> str:
    return Json.compact(d)


@ErrorHandler.base_exception
def b64decode(b: str) -> dict:
    return from_json(base64.b64decode(b, validate=True).decode())


@ErrorHandler.base_exception
def b64encode(d: dict) -> str:
    return base64.b64encode(to_json(d).encode()).decode()


@ErrorHandler.base_exception
def destruct_dict(dict_to_destruct: dict, keys: list) -> tuple:
    """
    Destructs a dictionary by extracting specific keys.

    :param dict_to_destruct: The dictionary to destruct.
    :type dict_to_destruct: dict

    :param keys: List of keys to extract from the dictionary.
    :type keys: list

    :return: Tuple of values corresponding to the extracted keys.
    :rtype: tuple
    """

    return itemgetter(*keys)(dict_to_destruct)


def event_body_to_dict(event):
    """
    The event_body_to_dict function is used to process a Lambda event.
    This is done so that the same function can be used through the Lambda invoke console and through the API gateway.

    When the event is invoked through the Lambda invoke console,
    the json in the body is already loaded, and any errors that occur during this process will be silently passed.

    This function returns the processed event as a json.
    """
    if event is not None:
        try:
            event = json.loads(event["body"])
        except KeyError:
            pass
    return event
