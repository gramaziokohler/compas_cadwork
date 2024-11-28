from __future__ import print_function
import os
from datetime import datetime

__title__ = "compas_cadwork"
__description__ = "COMPAS package for integrating with cadwork"
__url__ = "https://github.com/gramaziokohler/compas_cadwork"
__version__ = "0.9.0"
__author__ = "Gramazio Kohler Research"
__author_email__ = "gramaziokohler@arch.ethz.ch"
__license__ = "MIT license"
__copyright__ = "Copyright {} Gramazio Kohler Research".format(datetime.today().year)

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

__all_plugins__ = ["compas_cadwork.scene"]
