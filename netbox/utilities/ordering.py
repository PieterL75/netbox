import re

__all__ = (
    'naturalize',
    'naturalize_interface',
)

INTERFACE_NAME_REGEX = r'(^(?P<type>[^\d\.:]+)?)' \
                       r'((?P<slot>\d+)/)?' \
                       r'((?P<subslot>\d+)/)?' \
                       r'((?P<position>\d+)/)?' \
                       r'((?P<subposition>\d+)/)?' \
                       r'((?P<id>\d+))?' \
                       r'(:(?P<channel>\d+))?' \
                       r'(\.(?P<vc>\d+))?' \
                       r'(?P<remainder>.*)$'


def naturalize_interface(value, model_instance=None, **kwargs):
    """
    Returns the Naturalization Function for an interface name according to
    the sorting function defined on the parent device's platform.

    :param value: The value to be naturalized
    :param model_instance: The model instance that owns the interface.
    :param **kwargs: Any arguments that need to be passed to the naturalization function.
    """
    if (model_instance
        and model_instance.parent_object
        and 'platform' in dir(model_instance.parent_object)
        and model_instance.parent_object.platform):
        sortfunction = model_instance.parent_object.platform.get_interfacesorting_function()
        return sortfunction(value, model_instance=model_instance, **kwargs)
    return naturalize_interface_default(value, model_instance=model_instance, **kwargs)


def naturalize(value, max_length, integer_places=8, **kwargs):
    """
    Take an alphanumeric string and prepend all integers to `integer_places` places to ensure the strings
    are ordered naturally. For example:

        site9router21
        site10router4
        site10router19

    becomes:

        site00000009router00000021
        site00000010router00000004
        site00000010router00000019

    :param value: The value to be naturalized
    :param max_length: The maximum length of the returned string. Characters beyond this length will be stripped.
    :param integer_places: The number of places to which each integer will be expanded. (Default: 8)
    """
    if not value:
        return value
    output = []
    for segment in re.split(r'(\d+)', value):
        if segment.isdigit():
            output.append(segment.rjust(integer_places, '0'))
        elif segment:
            output.append(segment)
    ret = ''.join(output)

    return ret[:max_length]


def naturalize_numeric(value, max_length, integer_places=8, **kwargs):
    """
    Take an alphanumeric string and prepend all integers to `integer_places` places to ensure the strings
    are ordered naturally, while ignoring the alpa part. For example:

        Eth9/1
        Eth9/1:5
        ex-10/0/1

    becomes:

        0000000900000001
        000000090000000100000005
        000000100000000000000001

    :param value: The value to be naturalized
    :param max_length: The maximum length of the returned string. Characters beyond this length will be stripped.
    :param integer_places: The number of places to which each integer will be expanded. (Default: 8)
    """
    if not value:
        return value
    output = []
    segments = re.split(r'(\d+)', value)
    if len(segments) == 1:
        # no digits found, return original value
        return value
    for segment in segments:
        if segment.isdigit():
            output.append(segment.rjust(integer_places, '0'))
    ret = ''.join(output)

    return ret[:max_length]


def naturalize_interface_default(value, max_length, **kwarg):
    """
    Similar in nature to naturalize(), but takes into account a particular naming format adapted from the old
    InterfaceManager.

    :param value: The value to be naturalized
    :param max_length: The maximum length of the returned string. Characters beyond this length will be stripped.
    """
    output = ''
    match = re.search(INTERFACE_NAME_REGEX, value)
    if match is None:
        return value

    # First, we order by slot/position, padding each to four digits. If a field is not present,
    # set it to 9999 to ensure it is ordered last.
    for part_name in ('slot', 'subslot', 'position', 'subposition'):
        part = match.group(part_name)
        if part is not None:
            output += part.rjust(4, '0')
        else:
            output += '9999'

    # Append the type, if any.
    if match.group('type') is not None:
        output += match.group('type')

    # Append any remaining fields, left-padding to six digits each.
    for part_name in ('id', 'channel', 'vc'):
        part = match.group(part_name)
        if part is not None:
            output += part.rjust(6, '0')
        else:
            output += '......'

    # Finally, naturalize any remaining text and append it
    if match.group('remainder') is not None and len(output) < max_length:
        remainder = naturalize(match.group('remainder'), max_length - len(output))
        output += remainder

    return output[:max_length]
