from django.db import models

from netbox.config import ConfigItem

__all__ = (
    'custom_deconstruct',
)


EXEMPT_ATTRS = (
    'choices',
    'help_text',
    'verbose_name',
)

_deconstruct = models.Field.deconstruct


def custom_deconstruct(field):
    """
    Imitate the behavior of the stock deconstruct() method, but ignore the field attributes listed above.
    """
    name, path, args, kwargs = _deconstruct(field)

    # Remove any ignored attributes
    for attr in EXEMPT_ATTRS:
        kwargs.pop(attr, None)

    # Ignore any field defaults which reference a ConfigItem
    kwargs = {
        k: v for k, v in kwargs.items() if not isinstance(v, ConfigItem)
    }

    return name, path, args, kwargs
