from setuptools import setup, find_packages


setup(
    name='billreader',
    version='1.0.0',
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
