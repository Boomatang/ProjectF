try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

confing = [
    'descritption': 'Fayino'
    'author': 'Boomatang
]

setup(**config, requires=['flask']')
