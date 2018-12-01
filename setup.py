from setuptools import setup, find_packages
from ulis43 import __version__

install_requires = [
    'pygame>=1.9.4',
    'pyyaml>=3.13'
]

setup(
    name='ulis43',
    version=__version__,
    description='u lost in space bruh',
    long_description='yup',
    author='Jimmy Etienne, Yassine El Khadiri',
    licence='WTFPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=find_packages(exclude=['scripts', 'docs', 'tests']),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'ulis43=ulis43.cli:run'
        ]
    }
)
