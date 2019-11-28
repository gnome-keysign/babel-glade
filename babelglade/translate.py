import codecs
import logging

import os
import xml.etree.ElementTree as etree

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

    infp.close()
    outfp.close()


def translate_appdata_file(infile, outfile, localedir):
    catalogs = get_catalogs(localedir)
    tree = etree.parse(infile)
    root = tree.getroot()
    add_translations(root, catalogs)
    tree.write(outfile, encoding='utf-8', xml_declaration=True)


def add_translations(parent, catalogs):
    tail = parent.text
    last_tail = None
    for pos, elem in enumerate(parent, start=1):
        if elem.get("translatable") == "yes":
            elem.attrib.pop("translatable", None)
            elem.attrib.pop("comments", None)  # Are comments allowed?
            last_tail = elem.tail
            elem.tail = tail
            message = elem.text
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
                    tr.tail = tail
                    parent.insert(pos, tr)
        else:
            add_translations(elem, catalogs)
    if last_tail:
        parent[-1].tail = last_tail

def get_catalogs(localedir):
    # glob in Python 3.5 takes ** syntax
    # pofiles = glob.glob(os.path.join(localedir, '**.po', recursive=True))
    pofiles = sorted([os.path.join(dirpath, f)
               for dirpath, dirnames, files in os.walk(localedir)
               for f in files if f.endswith('.po')])
    logging.debug('Loading %r', pofiles)
    catalogs = {}

    for pofile in pofiles:
        with open(pofile, 'r') as f:
            catalog = read_po(f)
        catalogs[catalog.locale] = catalog
        logging.info("Found %d strings for %s", len(catalog), catalog.locale)
        # logging.debug("Strings for %r", catalog, catalog.values())
    if not catalogs:
        logging.warning("Could not find pofiles in %r", pofiles)
    return catalogs
