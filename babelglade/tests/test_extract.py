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

import unittest
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3from babel.messages.extract import DEFAULT_KEYWORDS
from babelglade.extract import extract_glade

DEFAULT_KEYWORDS = ""

class GladeExtractTests(unittest.TestCase):

    def setUp(self):
        self.glade_fileobj = StringIO("""\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE glade-interface SYSTEM "glade-2.0.dtd">
<glade-interface>
  <widget class="GtkWindow" id="window1">
    <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>
    <child>
      <widget class="GtkVBox" id="vbox1">
        <property name="visible">True</property>
        <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>
        <child>
          <widget class="GtkLabel" id="label1">
            <property name="visible">True</property>
            <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>
            <property name="label" translatable="yes" comments="A label with translator comments">This is a Label</property>
          </widget>
        </child>
        <child>
          <widget class="GtkButton" id="button1">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>
            <property name="label" translatable="yes" comments="This button also includes translator comments">A button</property>
          </widget>
          <packing>
            <property name="position">1</property>
          </packing>
        </child>
      </widget>
    </child>
  </widget>
</glade-interface>
""")

    def test_yield_four_item_tuples_with_comments(self):
        extracted = extract_glade(self.glade_fileobj, DEFAULT_KEYWORDS, True, {})
        for entry in list(extracted):
            assert len(entry) == 4, "extract_galde did not return a 4 tupple item"

    def test_yield_four_item_tuples_without_comments(self):
        extracted = extract_glade(self.glade_fileobj, DEFAULT_KEYWORDS, False, {})
        for entry in list(extracted):
            assert len(entry) == 4, "extract_galde did not return a 4 tupple item"
