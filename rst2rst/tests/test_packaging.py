# -*- coding: utf-8 -*-
"""Tests around project's distribution and packaging."""
import unittest


class PEP396TestCase(unittest.TestCase):
    """Check's PEP 396 compliance, i.e. package's __version__ attribute."""
    def get_version(self):
        """Return rst2rst.__version__."""
        from rst2rst import __version__
        return __version__

    def test_version_present(self):
        """Check that rst2rst.__version__ exists."""
        try:
            self.get_version()
        except ImportError:
            self.fail('rst2rst package has no attribute __version__.')

    def test_version_match(self):
        """Check that rst2rst.__version__ matches pkg_resources information."""
        try:
            import pkg_resources
        except ImportError:
            self.fail('Cannot import pkg_resources module. It is part of '
                      'setuptools, which is a dependency of rst2rst.')
        installed_version = pkg_resources.get_distribution('rst2rst').version
        self.assertEqual(installed_version, self.get_version(),
                         'Version mismatch: version.txt tells "%s" whereas '
                         'pkg_resources tells "%s". '
                         'YOU MAY NEED TO RUN ``make update`` to update the '
                         'installed version in development environment.'
                         % (self.get_version(), installed_version))
