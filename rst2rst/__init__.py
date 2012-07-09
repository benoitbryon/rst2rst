"""rst2rst package."""
from utils import LazyString, read_version
from writer import Writer  # Required for docutils.core.publish_cmdline() to
                           # find the writer matching "rst2rst".


__version__ = LazyString(read_version)
