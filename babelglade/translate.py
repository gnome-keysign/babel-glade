import codecs
import logging

import os
from lxml import etree

from babel.messages.pofile import read_po

log = logging.getLogger(__name__)


def translate_desktop_file(infile, outfile, localedir):
    infp = codecs.open(infile, 'rb', encoding='utf-8')
    outfp = codecs.open(outfile, 'wb', encoding='utf-8')

    catalogs = get_catalogs(localedir)

    for line in (x.strip() for x in infp):
        log.debug('Found in original (%s): %r', type(line), line)
        # We intend to ignore the first line
        if line.startswith('[Desktop'):
            additional_lines = []
        else:
            additional_lines = []
            # This is a rather primitive approach to generating the translated
            # desktop file.  For example we don't really care about all the
            # keys in the file.  But its simplicity is a feature and we
            # ignore the runtime overhead, because it should only run centrally
            # once.
            key, value = line.split('=', 1)
            log.debug("Found key: %r", key)
            for locale, catalog in catalogs.items():
                translated = catalog.get(value)
                log.debug("Translated %r[%r]=%r: %r (%r)",
                          key, locale, value, translated,
                          translated.string if translated else '')
                if translated and translated.string \
                              and translated.string != value:
                    additional_line = u'{keyword}[{locale}]={translated}'.format(
                                        keyword=key,
                                        locale=locale,
                                        translated=translated.string,
                                    )
                    additional_lines.append(additional_line)
                log.debug("Writing more lines: %s", additional_lines)

        # Write the new file.
        # First the original line found it in the file, then the translations.
        outfp.writelines((outline+'\n' for outline in ([line] + additional_lines)))


def translate_appdata_file(infile, outfile, localedir):
    catalogs = get_catalogs(localedir)
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(infile, parser)
    root = tree.getroot()
    for elem in root.iter():
        # We remove any possible tailing whitespaces to allow lxml to format the output
        elem.tail = None
        if elem.get("translatable") == "yes":
            elem.attrib.pop("translatable", None)
            elem.attrib.pop("comments", None)  # Are comments allowed?
            message = elem.text
            parent = elem.getparent()
            pos = parent.getchildren().index(elem) + 1
            for locale, catalog in catalogs.items():
                translated = catalog.get(message)
                if translated and translated.string \
                        and translated.string != message:
                    log.debug("Translated [%s]%r: %r (%r)",
                              locale, message, translated, translated.string)
                    tr = etree.Element(elem.tag)
                    attrib = tr.attrib
                    attrib["{http://www.w3.org/XML/1998/namespace}lang"] = str(locale)
                    tr.text = translated.string
                    parent.insert(pos, tr)
    tree.write(outfile, encoding='utf-8', pretty_print=True)


def get_catalogs(localedir):
    # glob in Python 3.5 takes ** syntax
    # pofiles = glob.glob(os.path.join(localedir, '**.po', recursive=True))
    pofiles = [os.path.join(dirpath, f)
               for dirpath, dirnames, files in os.walk(localedir)
               for f in files if f.endswith('.po')]
    logging.debug('Loading %r', pofiles)
    catalogs = {}

    for pofile in pofiles:
        catalog = read_po(open(pofile, 'r'))
        catalogs[catalog.locale] = catalog
        logging.info("Found %d strings for %s", len(catalog), catalog.locale)
        # logging.debug("Strings for %r", catalog, catalog.values())
    if not catalogs:
        logging.warning("Could not find pofiles in %r", pofiles)
    return catalogs
