import os
from setuptools import setup, find_packages

app_version = os.environ.get('APP_VERSION')

setup(
    name='billreader',
    version=app_version,
    packages=find_packages(include=['billreader']),
    install_requires=[
        'pdfminer.six>=20211012',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'billreader=billreader.__main__:main'
        ]
    }
)
