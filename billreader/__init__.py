import os
from billreader.classes import Bill, FileChecker

PROJ_ROOT = os.environ.get('PROJ_ROOT')
DATA_ROOT = os.environ.get('DATA_ROOT')

__all__ = ['Bill', 'FileChecker',
           'PROJ_ROOT', 'DATA_ROOT']
