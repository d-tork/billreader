from os import path
from billreader.classes import Bill, FileChecker

PROJ_PATH = path.dirname(path.dirname(path.abspath(__file__)))
BIND_MOUNT_DIR = path.join('/', 'common')

__all__ = ['PROJ_PATH', 'Bill', 'FileChecker', 'BIND_MOUNT_DIR']
