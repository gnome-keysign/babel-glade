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
# Copyright (C) 2007 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import os
import unittest
from babelglade.extract import extract_glade
# from babel.messages.extract import DEFAULT_KEYWORDS

DEFAULT_KEYWORDS = ("gettext", "pgettext")
GLADE2_FILE = "test_extract.glade2.xml"
GTKBUILDER_FILE = "test_extract.gtkbuilder.xml"


def relative(test_file):
    return os.path.join(os.path.dirname(__file__), test_file)


class GladeExtractTests(unittest.TestCase):

    def test_glade2_yield_four_item_tuples_with_keywords(self):
        with open(relative(GLADE2_FILE), "r") as fp:
            extracted = extract_glade(fp, DEFAULT_KEYWORDS, None, {})
            extracted = list(extracted)
        assert len(extracted) > 0, "extract_glade is not respecting presence of keywords"
        for entry in extracted:
            assert len(entry) == 4, "extract_glade did not return a tuple of length 4"

    def test_glade2_yield_no_tuples_without_keywords(self):
        with open(relative(GLADE2_FILE), "r") as fp:
            extracted = extract_glade(fp, (), None, {})
            extracted = list(extracted)
        assert len(extracted) == 0, "extract_glade is not respecting absence of keywords"

    def test_gtkbuilder_yield_pgettext_tuples_for_elems_with_context(self):
        with open(relative(GTKBUILDER_FILE), "r") as fp:
            extracted = extract_glade(fp, ["pgettext"], None, {})
            extracted = list(extracted)
        assert len(extracted) == 2, "extract_glade is not handling elems with context like pgettext"
        for entry in extracted:
            assert len(entry) == 4, "extract_glade did not return a tuple of length 4"
            lineno, funcname, message, comments = entry
            assert funcname == "pgettext", "extract_glade is not returning the right funcname (pgettext) for elems with context"
            assert isinstance(message, tuple) or isinstance(message, list), "extract_glade is not returning a tuple or a list when pretending it extracted from pgettext()"
            assert len(message) == 2, "extract_glade is not returning (ctx, msg) when pretending it extracted from pgettext()"

    def test_gtkbuilder_yield_gettext_tuples_for_elems_without_context(self):
        with open(relative(GTKBUILDER_FILE), "r") as fp:
            extracted = extract_glade(fp, ["gettext"], None, {})
            extracted = list(extracted)
        assert len(extracted) == 1, "extract_glade is not handling elems without context like gettext"
        for entry in extracted:
            assert len(entry) == 4, "extract_glade did not return a tuple of length 4"
            lineno, funcname, message, comments = entry
            assert funcname == "gettext", "extract_glade is not returning the right funcname (gettext) for elems without any context"
