"""
********************************************************************************
compas_cadwork
********************************************************************************

.. currentmodule:: compas_cadwork


.. toctree::
    :maxdepth: 1


"""

from __future__ import print_function

import os


from .__version__ import __author__
from .__version__ import __author_email__
from .__version__ import __copyright__
from .__version__ import __description__
from .__version__ import __license__
from .__version__ import __title__
from .__version__ import __url__
from .__version__ import __version__

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = [
    "HOME",
    "DATA",
    "DOCS",
    "TEMP",
    "__author__",
    "__author_email__",
    "__copyright__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
]

__all_plugins__ = ["compas_cadwork.artists"]
