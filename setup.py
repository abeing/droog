"""A setuptools-based setup module for Droog."""

from setuptools import setup, find_packages

setup(
    name='droog',

    version='0.1.0',

    description='A zombie roguelike',
    long_description='A zombie roguelike',

    url='https://github.com/abeing/droog',

    author='Adam Miezianko',
    author_email='adam@theorylounge.org',

    license='None',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console :: Curses',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
        'Topic :: Games/Entertainment :: Role-Playing'
        'Topic :: Games/Entertainment :: Turn Based Strategy'
        ],

    keywords='droog roguelike',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'droog=droog.main:main',
        ]
    }
)
