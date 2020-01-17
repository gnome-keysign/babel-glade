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


def _slurp(name):
    import os.path
    path = os.path.join(os.path.dirname(__file__), name)
    with open(path, encoding="utf-8") as fp:
        return fp.read()


setup(
    name    = 'BabelGladeExtractor',
    version = '0.7.0',
    license = 'BSD',
    author  = 'Pedro Algarvio',
    author_email = 'ufs@ufsoft.org',
    maintainer = 'Tobias Mueller',
    maintainer_email = 'tobiasmue@gnome.org',
    description = 'Babel l10n support for Glade, GtkBuilder, and .desktop files',
    long_description = _slurp("README.md"),
    long_description_content_type = "text/markdown",
    url = 'https://github.com/GNOME-Keysign/babel-glade',
    keywords = ['PyGTK', 'PyGObject', 'Glade', 'GtkBuilder', 'gettext', 'Babel', 'I18n', 'L10n'],
    install_requires = ['Babel'],
    test_suite = "babelglade.tests.suite",
    entry_points = """
    [babel.extractors]
    glade = babelglade.extract:extract_glade
    desktop = babelglade.extract:extract_desktop

    [distutils.commands]
    compile_catalog = babel.messages.frontend:compile_catalog
    """,
    packages = ['babelglade', 'babelglade.tests'],
    include_package_data=True
)
