#!/usr/bin/env python2

""" DNS TYPE and QTYPE values

This module contains an Enum for TYPE and QTYPE values. This Enum also contains
a method for converting Enum values to strings. See sections 3.2.2 and 3.2.3 of
RFC 1035 for more information.
"""

class Type(object):
    """ DNS TYPE and QTYPE

    Usage:
        >>> Type.A
        1
        >>> Type.CNAME
        5
    """
    A = 1
    NS = 2
    CNAME = 5
    SOA = 6
    WKS = 11
    PTR = 12
    HINFO = 13
    MINFO = 14
    MX = 15
    TXT = 16
    AAAA = 28
    ANY = 255

    by_string = {
        "A": A,
        "NS": NS,
        "CNAME": CNAME,
        "SOA": SOA,
        "WKS": WKS,
        "PTR": PTR,
        "HINFO": HINFO,
        "MINFO": MINFO,
        "MX": MX,
        "TXT": TXT,
        "AAAA": AAAA,
        "*": ANY
    }

    by_value = dict([(y, x) for x, y in by_string.items()])

    @staticmethod
    def to_string(type_):
        """ Convert a Type to a string

        Usage:
            >>> Type.to_string(Type.A)
            'A'
        """
        return Type.by_value[type_]

    @staticmethod
    def from_string(string):
        """ Convert a string to a Type

        Usage:
            >>> Type.from_string('CNAME')
            5
        """
        return Type.by_string[string]
