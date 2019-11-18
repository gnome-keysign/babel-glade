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

def suite():
    from babelglade.tests import test_extract
    suite = unittest.TestSuite()
    suite.addTest(test_extract.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
