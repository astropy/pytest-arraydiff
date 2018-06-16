from setuptools import setup

from pytest_arraydiff import __version__

# IMPORTANT: we deliberately use rst here instead of markdown because long_description
# needs to be in rst, and requiring pandoc to be installed to convert markdown to rst
# on-the-fly is over-complicated and sometimes the generated rst has warnings that
# cause PyPI to not display it correctly.

with open('README.rst') as infile:
    long_description = infile.read()

setup(
    version=__version__,
    url="https://github.com/astrofrog/pytest-arraydiff",
    name="pytest-arraydiff",
    description='pytest plugin to help with comparing array output from tests',
    long_description=long_description,
    packages=['pytest_arraydiff'],
    install_requires=['numpy', 'six', 'pytest'],
    license='BSD',
    author='Thomas Robitaille',
    author_email='thomas.robitaille@gmail.com',
    entry_points={'pytest11': ['pytest_arraydiff = pytest_arraydiff.plugin']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
)
