# -*- coding: utf-8 -*-


def balanced_braces(input_text):
    """
    Function used for checking if braces in given input_text are balanced
    :param input_text: string
    :return: string, 'Braces are balanced' if braces are balanced
                     'Braces are not balanced' if braces are not balanced
    """
    braces_dict = {
        '(': ')',
        '{': '}',
        '[': ']'
    }

    found_open_braces_list = []
    for letter in input_text:
        if letter in braces_dict:
            found_open_braces_list.append(letter)
        elif letter in braces_dict.values():
            if len(found_open_braces_list) < 1:
                return u'Braces are not balanced'
            else:
                last_open_brace = found_open_braces_list.pop(-1)
                if not braces_dict[last_open_brace] == letter:
                    return u'Braces are not balanced'
        else:
            continue

    return u'Braces are balanced'
