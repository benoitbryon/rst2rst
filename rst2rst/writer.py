"""reStructuredText document tree Writer."""

__docformat__ = 'reStructuredText'

from textwrap import TextWrapper

import docutils
from docutils import frontend, nodes, utils, writers, languages, io
from docutils.error_reporting import SafeString
from docutils.transforms import writer_aux
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
        """Character used for indentation."""

        self.blockquote_indent = 2
        """Indentation level for blockquotes."""

        self.wrap_length = 79


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

        self.spacer = ''
        """Buffer (string) that is to be inserted between two elements.

        The spacer isn't always inserted. As an example, it is not inserted at
        the end of the document.

        The spacer is typically assigned on depart_*() and inserted on next
        element's visit_*().

        """

    @property
    def indentation(self):
        """Return current indentation as unicode."""
        return self.options.indentation_char * sum(self._indentation_levels)

    @property
    def indentation_level(self):
        """Return current indentation level."""
        return self._indentation_levels[-1]

    def indent(self, levels):
        """Increase indentation by ``levels`` levels."""
        self._indentation_levels.append(levels)

    def dedent(self):
        """Decrease indentation by ``levels`` levels."""
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
        wrapper = TextWrapper(width=width, initial_indent=indent,
                              subsequent_indent=indent)
        return wrapper.fill(text)

    def visit_Text(self, node):
        self.body.append(self.spacer)
        text = node.astext()
        text = self.wrap(text)
        self.body.append(text)

    def depart_Text(self, node):
        pass

    def visit_abbreviation(self, node):
        pass

    def depart_abbreviation(self, node):
        pass

    def visit_acronym(self, node):
        pass

    def depart_acronym(self, node):
        pass

    def visit_address(self, node):
        pass

    def depart_address(self, node):
        pass

    def visit_admonition(self, node):
        pass

    def depart_admonition(self, node=None):
        pass

    def visit_attribution(self, node):
        pass

    def depart_attribution(self, node):
        pass

    def visit_author(self, node):
        pass

    def depart_author(self, node):
        pass

    def visit_authors(self, node):
        pass

    def depart_authors(self, node):
        pass

    def visit_block_quote(self, node):
        self.indent(self.options.blockquote_indent)


    def depart_block_quote(self, node):
        self.dedent()

    def visit_bullet_list(self, node):
        pass

    def depart_bullet_list(self, node):
        pass

    def visit_caption(self, node):
        pass

    def depart_caption(self, node):
        pass

    def visit_citation(self, node):
        pass

    def depart_citation(self, node):
        pass

    def visit_citation_reference(self, node):
        pass

    def depart_citation_reference(self, node):
        pass

    def visit_classifier(self, node):
        pass

    def depart_classifier(self, node):
        pass

    def visit_colspec(self, node):
        pass

    def depart_colspec(self, node):
        pass

    def write_colspecs(self):
        pass

    def visit_comment(self, node):
        pass

    def visit_compound(self, node):
        pass

    def depart_compound(self, node):
        pass

    def visit_container(self, node):
        pass

    def depart_container(self, node):
        pass

    def visit_contact(self, node):
        pass

    def depart_contact(self, node):
        pass

    def visit_copyright(self, node):
        pass

    def depart_copyright(self, node):
        pass

    def visit_date(self, node):
        pass

    def depart_date(self, node):
        pass

    def visit_decoration(self, node):
        pass

    def depart_decoration(self, node):
        pass

    def visit_definition(self, node):
        pass

    def depart_definition(self, node):
        pass

    def visit_definition_list(self, node):
        pass

    def depart_definition_list(self, node):
        pass

    def visit_definition_list_item(self, node):
        pass

    def depart_definition_list_item(self, node):
        pass

    def visit_description(self, node):
        pass

    def depart_description(self, node):
        pass

    def visit_docinfo(self, node):
        pass

    def depart_docinfo(self, node):
        pass

    def visit_docinfo_item(self, node, name, meta=True):
        pass

    def depart_docinfo_item(self):
        pass

    def visit_doctest_block(self, node):
        pass

    def depart_doctest_block(self, node):
        pass

    def visit_document(self, node):
        pass

    def depart_document(self, node):
        pass

    def visit_emphasis(self, node):
        pass

    def depart_emphasis(self, node):
        pass

    def visit_entry(self, node):
        pass

    def depart_entry(self, node):
        pass

    def visit_enumerated_list(self, node):
        pass

    def depart_enumerated_list(self, node):
        pass

    def visit_field(self, node):
        pass

    def depart_field(self, node):
        pass

    def visit_field_body(self, node):
        pass

    def depart_field_body(self, node):
        pass

    def visit_field_list(self, node):
        pass

    def depart_field_list(self, node):
        pass

    def visit_field_name(self, node):
        pass

    def depart_field_name(self, node):
        pass

    def visit_figure(self, node):
        pass

    def depart_figure(self, node):
        pass

    def visit_footer(self, node):
        pass

    def depart_footer(self, node):
        pass

    def visit_footnote(self, node):
        pass

    def footnote_backrefs(self, node):
        pass

    def depart_footnote(self, node):
        pass

    def visit_footnote_reference(self, node):
        pass

    def depart_footnote_reference(self, node):
        pass

    def visit_generated(self, node):
        pass

    def depart_generated(self, node):
        pass

    def visit_header(self, node):
        pass

    def depart_header(self, node):
        pass

    def visit_image(self, node):
        pass

    def depart_image(self, node):
        pass

    def visit_inline(self, node):
        pass

    def depart_inline(self, node):
        pass

    def visit_label(self, node):
        pass

    def depart_label(self, node):
        pass

    def visit_legend(self, node):
        pass

    def depart_legend(self, node):
        pass

    def visit_line(self, node):
        pass

    def depart_line(self, node):
        pass

    def visit_line_block(self, node):
        pass

    def depart_line_block(self, node):
        pass

    def visit_list_item(self, node):
        pass

    def depart_list_item(self, node):
        pass

    def visit_literal(self, node):
        pass

    def visit_literal_block(self, node):
        pass

    def depart_literal_block(self, node):
        pass

    def visit_math(self, node, math_env=''):
        pass

    def depart_math(self, node):
        pass

    def visit_math_block(self, node):
        pass

    def depart_math_block(self, node):
        pass

    def visit_meta(self, node):
        pass

    def depart_meta(self, node):
        pass

    def add_meta(self, tag):
        pass

    def visit_option(self, node):
        pass

    def depart_option(self, node):
        pass

    def visit_option_argument(self, node):
        pass

    def depart_option_argument(self, node):
        pass

    def visit_option_group(self, node):
        pass

    def depart_option_group(self, node):
        pass

    def visit_option_list(self, node):
        pass

    def depart_option_list(self, node):
        pass

    def visit_option_list_item(self, node):
        pass

    def depart_option_list_item(self, node):
        pass

    def visit_option_string(self, node):
        pass

    def depart_option_string(self, node):
        pass

    def visit_organization(self, node):
        pass

    def depart_organization(self, node):
        pass

    def should_be_compact_paragraph(self, node):
        pass

    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        self.body.append('\n')
        self.spacer = '\n'

    def visit_problematic(self, node):
        pass

    def depart_problematic(self, node):
        pass

    def visit_raw(self, node):
        pass

    def visit_reference(self, node):
        pass

    def depart_reference(self, node):
        pass

    def visit_revision(self, node):
        pass

    def depart_revision(self, node):
        pass

    def visit_row(self, node):
        pass

    def depart_row(self, node):
        pass

    def visit_rubric(self, node):
        pass

    def depart_rubric(self, node):
        pass

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    def visit_sidebar(self, node):
        pass

    def depart_sidebar(self, node):
        pass

    def visit_status(self, node):
        pass

    def depart_status(self, node):
        pass

    def visit_strong(self, node):
        pass

    def depart_strong(self, node):
        pass

    def visit_subscript(self, node):
        pass

    def depart_subscript(self, node):
        pass

    def visit_substitution_definition(self, node):
        pass

    def visit_substitution_reference(self, node):
        pass

    def visit_subtitle(self, node):
        pass

    def depart_subtitle(self, node):
        pass

    def visit_superscript(self, node):
        pass

    def depart_superscript(self, node):
        pass

    def visit_system_message(self, node):
        pass

    def depart_system_message(self, node):
        pass

    def visit_table(self, node):
        pass

    def depart_table(self, node):
        pass

    def visit_target(self, node):
        pass

    def depart_target(self, node):
        pass

    def visit_tbody(self, node):
        pass

    def depart_tbody(self, node):
        pass

    def visit_term(self, node):
        pass

    def depart_term(self, node):
        pass

    def visit_tgroup(self, node):
        pass

    def depart_tgroup(self, node):
        pass

    def visit_thead(self, node):
        pass

    def depart_thead(self, node):
        pass

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

    def visit_title_reference(self, node):
        pass

    def depart_title_reference(self, node):
        pass

    def visit_topic(self, node):
        pass

    def depart_topic(self, node):
        pass

    def visit_transition(self, node):
        pass

    def depart_transition(self, node):
        pass

    def visit_version(self, node):
        pass

    def depart_version(self, node):
        pass

    def unimplemented_visit(self, node):
        raise NotImplementedError('visiting unimplemented node type: %s'
                                  % node.__class__.__name__)
