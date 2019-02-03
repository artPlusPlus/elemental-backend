from . import errors
from . import serialization
from . import transactions
from . import resources
from ._controller import Controller
from ._controller_events import ControllerEvents
from ._model import Model


__title__ = 'elemental-backend'
__summary__ = 'Data management capabilities for Elemental CMS'
__url__ = 'https://github.com/artPlusPlus/elemental-backend'

__version__ = '0.4.0.dev0'

__author__ = 'Matt Robinson'
__email__ = 'matt@technicalartisan.com'

__license__ = 'Mozilla Public License 2.0 (MPL 2.0)'
__copyright__ = 'Copyright 2016 Matt Robinson'

__all__ = (
    '__title__', '__summary__', '__url__', '__version__', '__author__',
    '__email__', '__license__', '__copyright__',
    'errors', 'serialization', 'transactions', 'resources',
    'Controller', 'ControllerEvents', 'Model'
)
