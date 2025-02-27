from .example_mod import do_primes
from .constants import *
from .util import square
from .suite import Suite1D, Suite2D
from .version import version as __version__
# from importlib.metadata import version as _version, PackageNotFoundError
# try:
#     __version__ = _version(__name__)
# except PackageNotFoundError:
#     pass


# Then you can be explicit to control what ends up in the namespace,
__all__ = ['do_primes']
