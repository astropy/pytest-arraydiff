[![Travis Build Status](https://travis-ci.org/astrofrog/pytest-mpl.svg?branch=master)](https://travis-ci.org/astrofrog/pytest-mpl)
[![AppVeyor Build status](https://ci.appveyor.com/api/projects/status/mf7hs44scg5mvcyo?svg=true)](https://ci.appveyor.com/project/astrofrog/pytest-mpl)

About
-----

This is a [py.test](http://pytest.org) plugin to faciliate the generation and
comparison of FITS files produced during tests (this is a spin-off from
[pytest-mpl](https://github.com/astrofrog/pytest-mpl)).

The basic idea is that you can write a test that generates an Astropy HDU or
HDUList object. You can then either run the tests in a mode to **generate**
the reference FITS files from those HDUs or HDULists, or you can run the tests
in **comparison** mode, which will compare the results of the tests to the
reference ones within some tolerance.

For more information on how to write tests to do this, see the **Using**
section below.

Installing
----------

This plugin is compatible with Python 2.7, and 3.3 and later, and requires
[pytest](http://pytest.org), [numpy](http://www.numpy.org), and
[astropy](http://www.astropy.org) to be installed.

To install, you can do:

    pip install https://github.com/astrofrog/pytest-mpl/archive/master.zip

You can check that the plugin is registered with pytest by doing:

    py.test --version

which will show a list of plugins:

    This is pytest version 2.7.1, imported from ...
    setuptools registered plugins:
      pytest-fits-0.1 at ...

Using
-----

To use, you simply need to mark the function where you want to compare images
using ``@pytest.mark.fits_compare``, and make sure that the function
returns an Astropy HDU or HDUList object::

    python
    import pytest
    import numpy as np
    from astropy.io import fits

    @pytest.mark.fits_compare
    def test_succeeds():
        data = np.arange(3 * 5 * 4).reshape((3, 5, 4))
        header = fits.Header()
        header['TEST'] = 'example'
        header['VALUE'] = 1.344
        return fits.PrimaryHDU(data, header)

To generate the reference FITS files, run the tests with the
``--fits-generate-path`` option with the name of the directory where the
generated images should be placed:

    py.test --fits-generate-path=baseline

If the directory does not exist, it will be created. The directory will be
interpreted as being relative to where you are running ``py.test``. Make sure
you manually check the reference images to ensure they are correct.

Once you are happy with the generated FITS files, you should move them to a
sub-directory called ``baseline`` relative to the test files (this name is
configurable, see below). You can also generate the baseline images directly
in the right directory.

You can then run the tests simply with:

    py.test --fits

and the tests will pass if the images are the same. If you omit the ``--fits``
option, the tests will run but will only check that the code runs without
checking the output images.

Options
-------

The ``@pytest.mark.fits_compare`` marker can take an argument which is the
relative tolerance for floating point values (which defaults to 1e-7):

```python
@pytest.mark.fits_compare(rtol=20)
def test_image():
    ...
```

You can also pass keyword arguments to the Astropy FITS ``writeto`` methods
by using ``writeto_kwargs``:

```python
@pytest.mark.fits_compare(writeto_kwargs={'output_verify': 'silentfix'})
def test_image():
    ...
```

Other options include the name of the baseline directory (which defaults to
``baseline`` ) and the filename of the plot (which defaults to the name of the
test with a ``.fits`` suffix):

```python
@pytest.mark.fits_compare(baseline_dir='baseline_images',
                               filename='other_name.fits')
def test_image():
    ...
```

The baseline directory in the decorator above will be interpreted as being
relative to the test file. Note that the baseline directory can also be a
URL (which should start with ``http://`` or ``https://`` and end in a slash).

Finally, you can also set a custom baseline directory globally when running
tests by running ``py.test`` with:

    py.test --fits --fits-baseline-path=baseline_images

This directory will be interpreted as being relative to where the tests are
run. In addition, if both this option and the ``baseline_dir`` option in the
``fits_compare`` decorator are used, the one in the decorator takes
precedence.

Test failure example
--------------------

If the images produced by the tests are correct, then the test will pass, but if they are not, the test will fail with a message similar to the following:

```
E               Exception: 
E                fitsdiff: 1.2.1
E                a: /var/folders/zy/t1l3sx310d3d6p0kyxqzlrnr0000gr/T/tmp7067vdm6/baseline-test_succeeds_func.fits
E                b: /var/folders/zy/t1l3sx310d3d6p0kyxqzlrnr0000gr/T/tmp7067vdm6/test_succeeds_func.fits
E                Maximum number of different data values to be reported: 10
E                Data comparison level: 1e-07
E               
E               Primary HDU:
E               
E                  Data contains differences:
E                    Data differs at [3, 3, 3]:
E                       a> 50
E                       b> 100
E                    1 different pixels found (1.67% different).
```

The file paths included in the exception are then available for inspection:

Running the tests for pytest-fits
--------------------------------

If you are contributing some changes and want to run the tests, first install
the latest version of the plugin then do:

    cd tests
    py.test --fits

The reason for having to install the plugin first is to ensure that the plugin
is correctly loaded as part of the test suite.
