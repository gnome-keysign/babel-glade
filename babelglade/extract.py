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

from lxml import etree


def extract_glade(fileobj, keywords, comment_tags, options):
    tree = etree.parse(fileobj)
    root = tree.getroot()
    to_translate = []
    for elem in root.iter():
        # do we need to check if the element starts with "gtk-"?
        if elem.get("translatable") == "yes":
            line_no = elem.sourceline
            func_name = None
            message = elem.text
            comment = []
            if elem.get("comments"):
                comment = [elem.get("comments")]
            to_translate.append([line_no, func_name, message, comment])
    return to_translate
