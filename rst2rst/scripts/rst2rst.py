try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description


def main():
    description = ('Generates RST documents from standalone reStructuredText '
                   'sources.  ' + default_description)
    publish_cmdline(writer_name='rst2rst',
                    description=description)
