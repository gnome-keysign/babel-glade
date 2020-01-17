# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id$
# =============================================================================
#             $URL$
# $LastChangedDate$
#             $Rev$
#   $LastChangedBy$
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================
from __future__ import unicode_literals

import xml.etree.ElementTree as etree


def extract_glade(fileobj, keywords, comment_tags, options):
    """Extracts translatable strings from Glade files or GtkBuilder UI XML.

    :param fileobj: the file-like object to extract from, iterable by lines
    :param keywords: a list of translation keywords to extract, with the same
        names and meanings as C/Python i18n function names.
    :param comment_tags: a list of translator tags to search for and
        include in the results. This is ignored.
    :param options: a dictionary of additional options (optional)
    :return: An iterator over ``(lineno, funcname, message, comments)``
        tuples whose interpretation depends on ``funcname``.
    :rtype: iterator

    Properties must be marked translatable="yes". The "context" and
    "comments" attributes are respected. The yielded tuples are returned
    as if you used ``gettext()`` or ``pgettext()`` in C or Python code.
    This means that translatable XML strings with contexts are are only
    extracted if the string ``"pgettext"`` is present in ``keywords``,
    and XML strings without context are only extracted if ``"gettext"``
    is present. The shorthand ``_`` and ``C_`` aliases from ``g18n.h``
    are valid ``keywords`` too.

    By default, Babel passes both these function names in ``keywords``,
    amongst others, so you don't normally need to worry about this.

    See also:

    * babel.messages.extract.extract()
    * http://babel.pocoo.org/en/latest/messages.html#writing-extraction-methods
    * https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html

    """
    parser = etree.XMLPullParser(["end"])
    pgettext_wanted = ("pgettext" in keywords) or ("C_" in keywords)
    gettext_wanted = "gettext" in keywords
    truthy_values = [s.casefold() for s in ["yes", "true", "1", "y", "t"]]
    for line_idx, line_data in enumerate(fileobj):
        parser.feed(line_data)
        for event, elem in parser.read_events():
            assert event == "end"
            translatable_attr = elem.attrib.get("translatable", "no")
            if not translatable_attr.casefold() in truthy_values:
                continue

            comments = []
            if "comments" in elem.attrib:
                comments.append(elem.attrib["comments"])

            # Babel's interpretation of the yielded tuple depends on the
            # function name returned as part of it. This tells Babel what
            # the elements of the returned messages list or tuple mean.
            func_name = None
            if "context" in elem.attrib and pgettext_wanted:
                func_name = "pgettext"
                context = elem.attrib["context"]
                messages = [context, elem.text]
            elif gettext_wanted and "context" not in elem.attrib:
                # Returned strings are equivalent to a list or tuple
                # of length 1, like the arguments to C gettext()/_().
                func_name = "gettext"
                messages = elem.text

            if func_name is None:
                continue
            yield (line_idx + 1, func_name, messages, comments)


# All localestrings from https://specifications.freedesktop.org/desktop-entry-spec/latest/ar01s05.html
TRANSLATABLE = (
    'Name',
    'GenericName',
    'Comment',
    'Icon',
    'Keywords',
)


def extract_desktop(fileobj, keywords, comment_tags, options):
    for lineno, line in enumerate(fileobj, 1):
        if line.startswith(b'[Desktop Entry]'):
            continue

        for t in TRANSLATABLE:
            if not line.startswith(t.encode('utf-8')):
                continue
            else:
                l = line.decode('utf-8')
                comments = []
                key_value = l.split('=', 1)
                key, value = key_value[0:2]

                funcname = key # FIXME: Why can I not assign that name to funcname?
                funcname = ''
                message = value
                comments.append(key)
                yield (lineno, funcname, message.strip(), comments)
