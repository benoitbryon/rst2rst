"""reStructuredText document tree Writer."""

__docformat__ = 'reStructuredText'

from textwrap import TextWrapper

import docutils
from docutils import frontend, nodes, utils, writers, languages, io
from docutils.transforms import writer_aux
try:
    from docutils.utils.error_reporting import SafeString
    from docutils.utils.math import unichar2tex, pick_math_environment
    from docutils.utils.math.latex2mathml import parse_latex_math
    from docutils.utils.math.math2html import math2html
except ImportError:
    from docutils.error_reporting import SafeString
    from docutils.math import unichar2tex, pick_math_environment
    from docutils.math.latex2mathml import parse_latex_math
    from docutils.math.math2html import math2html


class Options(object):
    """Options for rst to rst conversion."""
    def __init__(self):
        self.title_chars = [u'#', u'*', u'=', u'-', u'^', u'"']
        """List of symbols used to underline and overline titles.

        List indices are "heading level - 1", i.e. at index 0 is the symbol
        used to underline/overline "H1".

        """

        self.title_prefix = [u'', u'\n', u'', u'', u'', u'']
        """List of prefixes before title and overline (typically, blank lines).

        Indices represent heading level.

        """

        self.title_suffix = [u'\n\n'] * 6
        """List of suffixes after title and underline (typically, blank lines).

        Indices represent heading level.

        """

        self.title_overline = [True, True, False, False, False, False]
        """List of booleans specifying whether to overline the title or not.

        List indices represent heading level.

        """

        self.indentation_char = u' '
        """Character used for indentation.

        Should be space or tab. Default is space.

        """

        self.blockquote_indent = 2
        """Indentation level for blockquotes."""

        self.wrap_length = 79
        """Wrap length, i.e. maximum text width, as number of chararcters."""

        self.bullet_character = ['*'] * 6
        """List of symbols used for bullet lists."""


class Writer(writers.Writer):
    supported = ('txt')  # Formats this writer supports.
    config_section = 'rst writer'
    config_section_dependencies = ('writers',)

    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = RSTTranslator
        self.options = Options()

    def translate(self):
        self.visitor = self.translator_class(self.document, self.options)
        self.document.walkabout(self.visitor)
        self.output = self.visitor.astext()


class RSTTranslator(nodes.NodeVisitor):
    """RST writer."""

    optional = (
        'document',
    )

    def __init__(self, document, options):
        self.options = options
        nodes.NodeVisitor.__init__(self, document)

        # Document parts.
        self.header = []
        self.title = []
        self.subtitle = []
        self.body = []
        self.footer = []

        # Context helpers.
        self.section_level = 0
        """Current section/title level, starting at 0.

        Section level is incremented/decremented during :py:meth:`visit_title`
        and :py:meth:`depart_title`.

        """

        self._indentation_levels = [0]
        """Stack of current indentation level.

        See also :py:attr:`indentation_level`, :py:meth:`indent` and
        :py:meth:`dedent`.

        """

        self._indent_first_line = [u'']

        self.spacer = ''
        """Buffer (string) that is to be inserted between two elements.

        The spacer isn't always inserted. As an example, it is not inserted at
        the end of the document.

        The spacer is typically assigned on depart_*() and inserted on next
        element's visit_*().

        """

        self.list_level = 0
        """Current level in nested lists."""

    @property
    def indentation(self):
        """Return current indentation as unicode."""
        return self.options.indentation_char * sum(self._indentation_levels)

    @property
    def initial_indentation(self):
        """Return current first-line indentation as unicode."""
        if self._indent_first_line[-1] is None:
            return self.indentation
        else:
            return self._indent_first_line[-1]

    @property
    def indentation_level(self):
        """Return current indentation level."""
        return self._indentation_levels[-1]

    def indent(self, levels, first_line=None):
        """Increase indentation by ``levels`` levels."""
        self._indentation_levels.append(levels)
        self._indent_first_line.append(first_line)

    def dedent(self):
        """Decrease indentation by ``levels`` levels."""
        self._indent_first_line.pop()
        return self._indentation_levels.pop()

    def astext(self):
        content = self.header + self.title + self.subtitle + self.body \
            + self.footer
        return ''.join(content)

    def wrap(self, text, width=None, indent=None):
        """Return ``text`` wrapped to ``width`` and indented with ``indent``.

        By default:

        * ``width`` is ``self.options.wrap_length``
        * ``indent`` is ``self.indentation``.

        """
        width = width if width is not None else self.options.wrap_length
        indent = indent if indent is not None else self.indentation
        initial_indent = self.initial_indentation
        wrapper = TextWrapper(width=width,
                              initial_indent=initial_indent,
                              subsequent_indent=indent)
        return wrapper.fill(text)

    def visit_Text(self, node):
        self.body.append(self.spacer)
        text = node.astext()
        text = self.wrap(text)
        self.body.append(text)

    def depart_Text(self, node):
        pass

    # Blockquotes.

    def visit_block_quote(self, node):
        self.indent(self.options.blockquote_indent)

    def depart_block_quote(self, node):
        self.dedent()

    # END blockquotes.

    # Lists (bullets, enumerated...)

    def visit_bullet_list(self, node):
        self.body.append(self.spacer)
        self.list_level += 1
        self.spacer = ''

    def depart_bullet_list(self, node):
        self.spacer = '\n'
        self.list_level -= 1

    def visit_list_item(self, node):
        self.indent(2, '%s%s ' % (self.indentation, self.bullet_character))
        self.spacer = ''

    def depart_list_item(self, node):
        self.dedent()
        self.spacer = '\n  '

    @property
    def bullet_character(self):
        return self.options.bullet_character[self.list_level]

    # END lists (bullets, enumerated...)

    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        self.body.append('\n')
        self.spacer = '\n'

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    def visit_title(self, node):
        self.body.append(self.options.title_prefix[self.section_level])
        is_overlined = self.options.title_overline[self.section_level]
        if is_overlined:
            self.body.append(self.spacer)
            symbol = self.options.title_chars[self.section_level]
            overline = symbol * len(node.astext())
            self.body.append(overline + '\n')
            self.spacer = ''

    def depart_title(self, node):
        section_level = self.section_level
        symbol = self.options.title_chars[section_level]
        underline = symbol * len(node.astext())
        self.body.append('\n' + underline)
        self.spacer = self.options.title_suffix[self.section_level]
