# coding=utf-8
"""Python packaging."""
import os
from setuptools import setup, find_packages


def read_relative_file(filename):
    """Returns contents of the given file, which path is supposed relative
    to this module."""
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


setup(name='rst2rst',
      version=read_relative_file('version.txt').strip(),
      description='Transform reStructuredText documents. Standardize RST syntax',
      long_description=read_relative_file('README.rst'),
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
      url='https://github.com/benoitbryon/rst2rst',
      license='BSD',
      packages=['rst2rst'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['docutils'],
      entry_points={
          'console_scripts': [
              'rst2rst = rst2rst.scripts.rst2rst:main',
          ]
      },
      )
