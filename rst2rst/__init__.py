"""rst2rst."""
import os

from writer import Writer


current_dir = os.path.dirname(os.path.abspath(__file__))
__version__ = open(os.path.join(current_dir, 'version.txt')).read().strip()

