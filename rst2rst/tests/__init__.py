"""rst2rst tests."""
from difflib import unified_diff
from glob import glob
import os
from unittest import TestCase

from docutils.core import publish_string


class PEP396TestCase(TestCase):
    """Check's PEP 396 compliance, i.e. package's __version__ attribute."""
    def get_version(self):
        """Return rst2rst.__version__."""
        try:
            from rst2rst import __version__
        except ImportError:
            self.fail('rst2rst package has no attribute __version__.')
        return __version__

    def test_version_present(self):
        """Check that rst2rst.__version__ is a string."""
        self.assertTrue(isinstance(self.get_version(), basestring))

    def test_version_match(self):
        """Check that rst2rst.__version__ matches pkg_resources information."""
        try:
            import pkg_resources
        except ImportError:
            self.fail('Cannot import pkg_resources module. It is part of ' \
                      'setuptools, which is a dependency of rst2rst.')
        installed_version = pkg_resources.get_distribution('rst2rst').version
        self.assertEqual(installed_version, self.get_version(),
                         'Version mismatch: version.txt tells "%s" whereas ' \
                         'pkg_resources tells "%s". ' \
                         'YOU MAY NEED TO RUN ``make update`` to update the ' \
                         'installed version in development environment.' \
                         % (self.get_version(), installed_version))


class WriterTestCase(TestCase):
    """Test suite for the rst2rst.writer.Writer class."""
    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(WriterTestCase, self).__init__(*args, **kwargs)
        current_dir = os.path.dirname(__file__)
        current_dir = os.path.normpath(os.path.abspath(current_dir))
        self.fixtures_dir = os.path.join(current_dir, 'fixtures')

    def test_fixtures_dir(self):
        """Make sure fixtures dir exists."""
        self.assertTrue(os.path.exists(self.fixtures_dir))

    def test_repeatability(self):
        """Make sure that a converted document keeps the same if converted
        again."""
        
    def test_output(self):
        """Check that parsing input files provides the expected output files.
        """
        input_filenames = glob(os.path.join(self.fixtures_dir, '*-input.txt'))
        if not input_filenames:
            self.fail('No fixtures found')
        for input_filename in input_filenames:
            with open(input_filename) as input_file:
                input_str = input_file.read()
            real_output = publish_string(source=input_str,
                                         writer_name='rst2rst')
            output_filename = input_filename.replace('input.txt', 'output.txt')
            output_filename = os.path.join(self.fixtures_dir, output_filename)
            with open(output_filename) as output_file:
                theoric_output = output_file.read()
            if real_output != theoric_output:
                theoric_output = theoric_output.replace('\n', '\\n\n')
                real_output = real_output.replace('\n', '\\n\n')
                diff = []
                real_output_lines = real_output.splitlines(True)
                theoric_output_lines = theoric_output.splitlines(True)
                for line in unified_diff(real_output_lines,
                                         theoric_output_lines):
                    diff.append(line)
                diff = ''.join(diff)
                msg = "Content generated from %s differs from content at %s" \
                      "\nDiff:\n%s" % (
                          input_filename,
                          output_filename,
                          diff
                      )
                self.fail(msg)
