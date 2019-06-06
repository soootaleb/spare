
import inspect, sys, click, logging as log, coloredlogs

from models.image import Image
from descriptors import AngularDistanceDescriptor

from functions import get_commands

logger = log.getLogger('cli')

log.SUCCESS = 25  # between WARNING and INFO
log.addLevelName(log.SUCCESS, 'SUCCESS')
setattr(logger, 'success', lambda message, *args: logger._log(log.SUCCESS, message, args))

coloredlogs.install(fmt='%(message)s', logger=logger, level=log.DEBUG, level_styles={
    'debug': { 'color': 'blue' },
    'info': { 'color': 'green', 'bold': True },
    'success': { 'color': 'magenta', 'bold': True },
    'result': { 'color': 'green', 'bold': True },
    'warning': { 'color': 'yellow' },
    'error': { 'color': 'red' },
    'critical': { 'color': 'red', 'bold': True },
})
