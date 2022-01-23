"""
Rename files on ingest to object storage.

"""
import os
import sys
import argparse
from datetime import datetime
import hashlib


def main():
    args = parse_cli_args()
    renamer = FileRenamer(src_path=args.filepath[0], dest_root=args.basename)
    renamer.rename_file()
    print(renamer.dest_path)
    sys.exit(0)


class FileRenamer(object):
    """Container for renaming files."""
    def __init__(self, src_path: str, dest_root: str):
        self.src_path = src_path
        self.dest_root = dest_root
        self.dest_path = self._create_dest_path()

    def rename_file(self):
        os.rename(self.src_path, self.dest_path)

    def _create_dest_path(self) -> str:
        base_path = os.path.dirname(self.src_path)
        dest_name = self._create_destination_name()
        dest_path = os.path.join(base_path, dest_name)
        return dest_path

    def _create_destination_name(self) -> str:
        modify_time_ts = os.path.getmtime(self.src_path)
        modify_time_utc = datetime.utcfromtimestamp(modify_time_ts)
        datetime_format = '%Y_%m_%d'  # 2022_01_18
        ts_formatted = modify_time_utc.strftime(datetime_format)

        filehash = create_file_hash(filepath=self.src_path)
        dest_name = f"{self.dest_root}-{ts_formatted}-{filehash}.pdf"
        return dest_name


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Rename files for ingest to object storage.')
    parser.add_argument('filepath', type=str, nargs=1, help='Filepath of pdf')
    parser.add_argument('--basename', type=str, default='billdownload',
        help='Root name of destination file.')
    args = parser.parse_args()
    return args


def create_file_hash(filepath: str) -> str:
    """Create a SHA-1 hash of the contents of a file."""
    with open(filepath, 'rb') as f:
        data = f.read()
        return hashlib.sha1(data).hexdigest()


if __name__ == '__main__':
    main()

