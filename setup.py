from setuptools import setup, find_packages


setup(
    name='billreader',
    version='0.1.0',
    packages=find_packages(include=['billreader']),
    install_requires=[
        'pdfminer.six>=20211012',
    ]
)