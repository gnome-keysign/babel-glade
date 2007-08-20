#!/usr/bin/env python
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

from setuptools import setup

setup(
    name    = 'BabelGladeExtractor',
    version = '0.3',
    license = 'BSD',
    author  = 'Pedro Algarvio',
    author_email = 'ufs@ufsoft.org',
    maintainer = 'Pedro Algarvio',
    maintainer_email = 'ufs@ufsoft.org',
    description = 'Babel Glade XML files translatable strings extractor',
    url = 'http://babel.edgewall.org/wiki/BabelGladeExtractor',
    keywords = ['PyGTK', 'Glade', 'gettext', 'Babel', 'I18n', 'L10n'],
    install_requires = ['Babel'],
    test_suite = "babelglade.tests.suite",
    entry_points = """
    [babel.extractors]
    glade = babelglade.extract:extract_glade
    """,
    packages = ['babelglade']

)
