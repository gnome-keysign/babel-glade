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
    version = '0.7.0',
    license = 'BSD',
    author  = 'Pedro Algarvio',
    author_email = 'ufs@ufsoft.org',
    maintainer = 'Tobias Mueller',
    maintainer_email = 'tobiasmue@gnome.org',
    description = 'Babel l10n support for Glade, GtkBuilder, and .desktop files',
    long_description = """
This package contains message catalog extractors for the following
formats, extending Babel_ so it can handle them.

    * The older "Glade v2" XML format;
    * The new GtkBuilder-compatible "UI Definition XML" format used by
      Glade_ 3.8 and above;
    * The AppData XML dialect, because it's similar;
    * FreeDesktop.org ".desktop" files.

To make these formats translatable, install this package. Then in your
own projects map some source and data files to the simple extractor
names "glade" and "desktop" that are provided by this package. You can
then use Babel's setuptools integration or its command line interface
for routine i18n lifecycle tasks.

.. _Babel: http://babel.pocoo.org/en/latest/index.html
.. _Glade: https://glade.gnome.org/


""",
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
