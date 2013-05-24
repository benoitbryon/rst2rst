# -*- coding: utf-8 -*-
"""Tests around fixtures: check behaviour obtained with sample files."""
from difflib import unified_diff
import os
import re
import unittest

from docutils.core import publish_string

from rst2rst.utils.tempdir import temporary_directory


#: Absolute path to ``rst2rst.tests`` module.
TESTS_DIR = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

#: Absolute path to :file:`fixtures` directory within ``rst2rst.tests`` module.
FIXTURE_DIR = os.path.join(TESTS_DIR, 'fixtures')


def fixture_names(fixture_dir=FIXTURE_DIR):
    """Return list of fixture names.

    By default, ``fixtures_dir`` is
    :py:attr:`rst2rst.tests.test_fixtures.FIXTURE_DIR`.

    Fixture names are computed from filenames in ``fixture_dir``.

    """
    return [
        re.match(r'^(.+?)-input\.txt$', f).group(1)
        for f in os.listdir(fixture_dir)
        if f.endswith('-input.txt')
    ]


class FixturesNamesTestCase(unittest.TestCase):
    """:py:func:`fixture_names` return list of fixture names in directory."""
    def test_capture(self):
        """fixture_names() grabs all *-input.txt file in a directory."""
        filenames = ('one.txt',
                     'two-input.txt',
                     'threeinput.txt',
                     'four-five-six-input.txt',
                     'seven-output.txt',
                     'eight-input',
                     'nine-input.rst',
                     'ten_input.txt')
        expected_names = ['two', 'four-five-six']  # Order does not matter.
        with temporary_directory() as directory:
            for filename in filenames:  # Create the files.
                open(os.path.join(directory, filename), 'w').write('fake')
            names = fixture_names(directory)
        self.assertEqual(sorted(names), sorted(expected_names))

    def test_not_empty(self):
        """fixture_names() actually finds some fixtures."""
        self.assertTrue(fixture_names())


def fixture_method(name):
    """Return function that checks fixture by ``name`` in a TestCase."""
    return lambda obj: obj.run_fixture(*(obj.fixture_paths(name)))


def fixtures_class(cls, bases, attrs):
    """Dynamically add a test method for each available fixture."""
    docstring = """"rst2rst" writer publish "{name}" fixture as expected."""
    for fixture_name in fixture_names():
        method_name = 'test_{name}'.format(name=fixture_name)
        attrs[method_name] = fixture_method(fixture_name)
        attrs[method_name].__name__ = method_name  # Required for nose.
        attrs[method_name].__doc__ = docstring.format(name=fixture_name)
    return type(cls, bases, attrs)


class WriterTestCase(unittest.TestCase):
    """Test suite for the rst2rst.writer.Writer class."""
    # Specific metaclass, in order to have one test_* method for each available
    # fixture. Benefits:
    #
    # * Better overview/progress notifications ;
    # * Failure of a fixture does not preclude trying out other fixtures.
    __metaclass__ = fixtures_class

    def get_fixture_dir(self):
        """Return :py:attr:`rst2rst.tests.test_fixtures.FIXTURE_DIR`."""
        return FIXTURE_DIR

    def fixture_paths(self, name):
        """Return ``(input, output)`` filenames for fixture ``name``.

        Also asserts both files exist.

        """
        paths = []
        for suffix in ['input', 'output']:
            filename = '%s-%s.txt' % (name, suffix)
            path = os.path.join(self.get_fixture_dir(), filename)
            self.assertTrue(
                os.path.exists(path),
                "Missing file '%s' for fixture '%s'" % (filename, name))
            paths.append(path)
        return paths

    def run_fixture(self, source, reference):
        """Assert rst2rst writer converts ``source`` to ``reference``.

        Both ``source`` and ``reference`` are paths to files.

        """
        input_str = open(source).read()
        real = publish_string(source=input_str, writer_name='rst2rst')
        expected = open(reference).read()
        if real != expected:
            # Report error with a diff.
            real_lines = real.replace('\n', '\\n\n').splitlines(True)
            expected_lines = expected.replace('\n', '\\n\n').splitlines(True)
            diff = ''.join(unified_diff(expected_lines, real_lines))
            msg = "Content generated from %s differs from content at %s" \
                  "\nDiff:\n%s" % (os.path.basename(source),
                                   os.path.basename(reference),
                                   diff)
            self.fail(msg)


class FixtureTestTestCase(unittest.TestCase):
    def test_fixtures_methods(self):
        """WriterTestCase has test method for every fixture."""
        test_class = WriterTestCase
        for name in fixture_names():
            method_name = 'test_{name}'.format(name=name)
            self.assertTrue(callable(getattr(test_class, method_name)))
