# coding=utf-8
"""Python packaging."""
import os
from setuptools import setup


def read_relative_file(filename):
    """Returns contents of the given file, which path is supposed relative
    to this module."""
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


NAME = 'rst2rst'
README = read_relative_file('README.rst')
VERSION = read_relative_file(os.path.join(NAME, 'version.txt')).strip()


setup(name=NAME,
      version=VERSION,
      description='Transform reStructuredText documents. Standardize RST syntax',
      long_description=README,
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Documentation',
                   'Topic :: Software Development :: Documentation',
                   'Topic :: Software Development :: Quality Assurance',
                   'Topic :: Text Processing',
                   ],
      keywords='rst writer reStructuredText',
      author='Benoit Bryon',
      author_email='benoit@marmelune.net',
      url='https://github.com/benoitbryon/%s' % NAME,
      license='BSD',
      packages=[NAME],
      zip_safe=False,
      install_requires=['setuptools', 'docutils'],
      entry_points={
          'console_scripts': [
              'rst2rst = rst2rst.scripts.rst2rst:main',
          ]
      },
      )
