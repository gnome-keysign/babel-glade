# BabelGladeExtractor

This package contains message catalog extractors for the following
formats, extending [Babel][babel] so it can handle them.

* The new XML format used by [Glade][glade] 3.8 and above, properly
  known as the [GtkBuilder UI Definitions][uixml] format;

* The older "GladeXML" format used by libglade and older versions of
  Glade;

* The GNOME [AppData XML][appdataxml] dialect, because it's similar;

* FreeDesktop.org [Desktop Entry][desktopfile] files.

## Getting started

To make these formats translatable, install this package using pip:

```shell
pip3 install BabelGladeExtractor
```

Then in your own projects, map some source and data files to the simple
extractor names "glade" and "desktop" that are provided by this package.
In your `setup.py`, add a section like

```ini
[extract_messages]
mapping_file = babel.cfg
output_file = subdir/myproject.pot
input_dirs = .
```

Next, create a separate `babel.cfg` file, and add sections to it for
each format you want to translate.

```ini
[glade: **.ui]

[desktop: **.desktop]

```

You can then use Babel's [setuptools integration][babelsetuptools] or
its [command line interface][babelcli] for your routine i18n lifecycle
tasks.

```shell
python3 setup.py extract_messages
```

There's a lot more to it than this, naturally. See Babel's extensive
[Working with Message Catalogs][babelpo] documentation for a detailed
explanation of how to get translatable strings into your Python code.

In Glade 3.22, when you are editing a string property in a sidebar,
click the edit icon on the right hand side of the text entry. In the
dialog that pops up, enter the text in the main text box, and make sure
that the Translatable checkbox is ticked. You can also add some helpful
[context][pocontext] or comments for your translators if you need to
give them a hint. BabelGladeExtractor will handle the corresponding XML
attributes appropriately when it extracts strings for translation.

[babel]: http://babel.pocoo.org/
[glade]: https://glade.gnome.org/
[uixml]: https://developer.gnome.org/gtk3/stable/GtkBuilder.html#BUILDER-UI
[appdataxml]: https://wiki.gnome.org/Initiatives/GnomeGoals/AppDataGnomeSoftware
[desktopfile]: https://specifications.freedesktop.org/desktop-entry-spec/
[babelsetuptools]: http://babel.pocoo.org/en/latest/setup.html
[babelcli]: http://babel.pocoo.org/en/latest/cmdline.html
[babelpo]: http://babel.pocoo.org/en/latest/messages.html
[pocontext]: https://www.gnu.org/software/gettext/manual/html_node/Contexts.html#Contexts
