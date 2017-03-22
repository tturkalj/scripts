import json
from datetime import datetime

function_args_dict = {}


def get_args_hash(args, kwargs):
    """
    Function used for hashing string created from function args and kwargs
    :param args: list of arguments
    :param kwargs: dictionary of arguments
    :return: hash string
    """
    args_dict = dict(kwargs)
    for index, arg in enumerate(args):
        args_dict[index] = arg

    dump = json.dumps(args_dict, sort_keys=True)

    return hash(dump)


def cache_func(args_key, func_result):
    """
    Function used for storing function result for given args_key
    :param args_key: string
    :param func_result: object
    """
    global function_args_dict
    function_args_dict[args_key] = {
        'func_result': func_result,
        'call_counter': 0,
        'time_called': datetime.utcnow()
    }


def get_func_result_from_cache(args_key):
    """
    Function used for getting function result for given args_key.
    :param args_key: string
    :return: func_result, object
    """
    function_data = function_args_dict[args_key]
    call_counter = function_data['call_counter']
    call_counter += 1
    function_data['call_counter'] = call_counter
    function_args_dict[args_key] = function_data
    return function_data['func_result']


def cache_decorator(func):
    """
    Function used for caching function result for 5 minutes or 10 calls.
    Function is used as decorator
    :param func: function
    :return: wrapper_func, function
    """
    def wrapper_func(*args, **kwargs):
        args_key = get_args_hash(args, kwargs)
        function_data = function_args_dict.get(args_key, None)
        if not function_data:
            func_result = func(*args, **kwargs)
            cache_func(args_key, func_result)
        else:
            time_delta = datetime.utcnow() - function_data['time_called']
            if time_delta.total_seconds() / 60 > 5 or function_data['call_counter'] == 10:
                func_result = func(*args, **kwargs)
                cache_func(args_key, func_result)
            else:
                func_result = get_func_result_from_cache(args_key)
        return func_result

    return wrapper_func
