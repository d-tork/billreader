import os
from billreader.classes import Bill, FileChecker

PROJ_ROOT = os.environ.get('PROJ_ROOT')
BIND_MOUNT_DIR = os.path.join('/', 'common')

__all__ = ['Bill', 'FileChecker',
           'PROJ_ROOT', 'BIND_MOUNT_DIR']
