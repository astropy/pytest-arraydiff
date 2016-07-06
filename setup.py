from setuptools import setup

from pytest_fits import __version__

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    with open('README.md') as infile:
        long_description = infile.read()

setup(
    version=__version__,
    url="https://github.com/astrofrog/pytest-fits",
    name="pytest-fits",
    description='pytest plugin to help with comparing FITS output from tests',
    long_description=long_description,
    packages = ['pytest_fits'],
    license='BSD',
    author='Thomas Robitaille',
    author_email='thomas.robitaille@gmail.com',
    entry_points = {'pytest11': ['pytest_fits = pytest_fits.plugin',]},
)
