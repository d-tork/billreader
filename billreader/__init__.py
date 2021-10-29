from os import path
from billreader.classes import Bill

PROJ_PATH = path.dirname(path.dirname(path.abspath(__file__)))

__all__ = ['PROJ_PATH', 'Bill']
