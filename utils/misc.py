#!/usr/bin/env python
# -*- coding: utf-8 -*-


def fill_zero(data, max_length=3):
    data = str(int(data))
    zero_num = max_length - len(data)
    if zero_num >= 1:
        return '0' * zero_num + str(data)
    return data


def safe_int(value, default=0):
    try:
        value = int(value)
    except:
        value = default
    return value


if type('') is not type(b''):
    bytes_type = bytes
    unicode_type = str
    basestring_type = str
else:
    bytes_type = str
    unicode_type = unicode
    basestring_type = basestring

_UTF8_TYPES = (bytes_type, type(None))


def utf8(text):
    """
        Converts a string argument to a byte string.

        If the argument is already a byte string or None, it is returned unchanged.
        Otherwise it must be a unicode string and is encoded as utf8.
    """
    if isinstance(text, _UTF8_TYPES):
        return text
    assert isinstance(text, unicode_type), \
        "Expected bytes, unicode, or None; got %r" % type(text)
    return text.encode("utf-8")


_TO_UNICODE_TYPES = (unicode_type, type(None))


def to_unicode(text):
    """
        Converts a string argument to a unicode string.

        If the argument is already a unicode string or None, it is returned
        unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(text, _TO_UNICODE_TYPES):
        return text
    assert isinstance(text, bytes_type), \
        "Expected bytes, unicode, or None; got %r" % type(text)
    return text.decode("utf-8",'ignore')

_BASESTRING_TYPES = (basestring_type, type(None))


def to_basestring(value):
    """Converts a string argument to a subclass of basestring.

    In python2, byte and unicode strings are mostly interchangeable,
    so functions that deal with a user-supplied argument in combination
    with ascii string constants can use either and should return the type
    the user supplied.  In python3, the two types are not interchangeable,
    so this method is needed to convert byte strings to unicode.
    """
    if isinstance(value, _BASESTRING_TYPES):
        return value
    if not isinstance(value, bytes_type):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.decode("utf-8",'ignore')


def recursive_unicode(obj):
    """
    Walks a simple data structure, converting byte strings to unicode.
    Supports lists, tuples, and dictionaries.
    """
    if isinstance(obj, dict):
        return dict((recursive_unicode(k), recursive_unicode(v)) for (k, v) in obj.items())
    elif isinstance(obj, list):
        return list(recursive_unicode(i) for i in obj)
    elif isinstance(obj, tuple):
        return tuple(recursive_unicode(i) for i in obj)
    elif isinstance(obj, bytes_type):
        return to_unicode(obj)
    else:
        return obj