"""Various utilities."""
import os


class LazyString(object):
    """A str-like object which value is computed when the object is actually
    used as a string. Function argument must return a string.

    >>> s = LazyString(str, 'Hello world!')
    >>> print s
    Hello world!
    >>> def print_a_and_return_b(a, b):
    ...     print a
    ...     return b
    >>> s = LazyString(print_a_and_return_b, 'Hello', 'world')
    >>> s == 'world'
    Hello
    True

    """
    def __init__(self, function, *args, **kwargs):
        """Constructs a "lazy" str-like object.

        The call to "function" is delayed.
        The "function" parameter receives any additional args only when the
        LazyString instance is used as a str.

        """
        self.function=function
        self.args=args
        self.kwargs=kwargs

    def __str__(self):
        """Executes self.function to convert LazyString instance to a real
        str."""
        if not hasattr(self, '_str'):
            self._str=self.function(*self.args, **self.kwargs)
        return self._str

    def __mod__(self, operand):
        """Handles string formating operator."""
        return str(self) % operand

    def __eq__(self, other):
        """Equality operator."""
        return str(self) == other

    def __cmp__(self, other):
        """Comparison operator."""
        return cmp(str(self), other)


def read_relative_file(filename, relative_to=None):
    """Returns contents of the given file, which path is supposed relative
    to this module."""
    if relative_to is None:
        relative_to = __file__
    with open(os.path.join(os.path.dirname(relative_to), filename)) as f:
        return f.read()


def read_version():
    """Return version number from version.txt."""
    return read_relative_file('version.txt').strip()
