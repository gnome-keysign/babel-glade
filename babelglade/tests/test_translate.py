
import os
import unittest
from babelglade.translate import translate_desktop_file, translate_appdata_file

def relative(test_file):
    return os.path.join(os.path.dirname(__file__), test_file)


class TranslateTestCase(unittest.TestCase):

    def test_desktop_file(self):
        translate_desktop_file(relative("test.raw.desktop"), "test.desktop", relative("locale"))

        with open("test.desktop") as desktop:
            content = desktop.read()

        assert "Comment=This should be translated." in content
        assert "Comment[nl]=Dit moet worden vertaald." in content
        assert "Comment[fr]=Cela devrait être traduit." in content

    def test_appdata_xml(self):
        translate_appdata_file(relative("test.raw.appdata.xml"), "test.appdata.xml", relative("locale"))

        with open("test.appdata.xml") as desktop:
            content = desktop.read()

        assert "<p>This should be translated.</p>" in content
        assert '<p xml:lang="fr">Cela devrait être traduit.</p>' in content
        assert '<p xml:lang="nl">Dit moet worden vertaald.</p>' in content
        assert """<p>
      Multi line
      text.
    </p>""" in content
        assert """<p xml:lang="fr">
      Texte
      multi-ligne.
    </p>""" in content
        assert """<p xml:lang="nl">
      Meerregelige
      tekst.
    </p>""" in content