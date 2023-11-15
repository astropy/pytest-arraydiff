.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.5811772.svg
   :target: https://doi.org/10.5281/zenodo.5811772
   :alt: 10.5281/zenodo.5811772

.. image:: https://github.com/astropy/pytest-arraydiff/workflows/CI/badge.svg
    :target: https://github.com/astropy/pytest-arraydiff/actions
    :alt: CI Status

.. image:: https://img.shields.io/pypi/v/pytest-arraydiff.svg
    :target: https://pypi.org/project/pytest-arraydiff
    :alt: PyPI Status

About
-----

This is a `py.test <http://pytest.org>`__ plugin to facilitate the
generation and comparison of data arrays produced during tests, in particular
in cases where the arrays are too large to conveniently hard-code them
in the tests (e.g. ``np.testing.assert_allclose(x, [1, 2, 3])``).

The basic idea is that you can write a test that generates a Numpy array (or
other related objects depending on the format, e.g. pandas DataFrame).
You can then either run the
tests in a mode to **generate** reference files from the arrays, or you can run
the tests in **comparison** mode, which will compare the results of the tests to
the reference ones within some tolerance.

At the moment, the supported file formats for the reference files are:

-  A plain text-based format (based on Numpy ``loadtxt`` output)
-  The FITS format (requires `astropy <http://www.astropy.org>`__). With this
   format, tests can return either a Numpy array for a FITS HDU object.
-  A pandas HDF5 format using the pandas HDFStore

For more information on how to write tests to do this, see the **Using**
section below.

Installing
----------

This plugin is compatible with Python 2.7, and 3.5 and later, and
requires `pytest <http://pytest.org>`__ and
`numpy <http://www.numpy.org>`__ to be installed.

To install, you can do::

    pip install pytest-arraydiff

You can check that the plugin is registered with pytest by doing::

    py.test --version

which will show a list of plugins::

    This is pytest version 2.7.1, imported from ...
    setuptools registered plugins:
      pytest-arraydiff-0.1 at ...

Using
-----

To use, you simply need to mark the function where you want to compare
arrays using ``@pytest.mark.array_compare``, and make sure that the
function returns a plain Numpy array::

    python
    import pytest
    import numpy as np

    @pytest.mark.array_compare
    def test_succeeds():
        return np.arange(3 * 5 * 4).reshape((3, 5, 4))

To generate the reference data files, run the tests with the
``--arraydiff-generate-path`` option with the name of the directory
where the generated files should be placed::

    py.test --arraydiff-generate-path=reference

If the directory does not exist, it will be created. The directory will
be interpreted as being relative to where you are running ``py.test``.
Make sure you manually check the reference arrays to ensure they are
correct.

Once you are happy with the generated data files, you should move them
to a sub-directory called ``reference`` relative to the test files (this
name is configurable, see below). You can also generate the baseline
arrays directly in the right directory.

You can then run the tests simply with::

    py.test --arraydiff

and the tests will pass if the arrays are the same. If you omit the
``--arraydiff`` option, the tests will run but will only check that the
code runs without checking the output arrays.

Options
-------

The ``@pytest.mark.array_compare`` marker take an argument to specify
the format to use for the reference files:

.. code:: python

    @pytest.mark.array_compare(file_format='text')
    def test_array():
        ...

The default file format can also be specified using the
``--arraydiff-default-format=<format>`` flag when running ``py.test``,
and ``<format>`` should be either ``fits`` or ``text``.

The supported formats at this time are ``text`` and ``fits``, and
contributions for other formats are welcome. The default format is
``text``.

Additional arguments are the relative and absolute tolerances for floating
point values (which default to 1e-7 and 0, respectively):

.. code:: python

    @pytest.mark.array_compare(rtol=20, atol=0.1)
    def test_array():
        ...

You can also pass keyword arguments to the writers using the
``write_kwargs``. For the ``text`` format, these arguments are passed to
``savetxt`` while for the ``fits`` format they are passed to Astropy's
``fits.writeto`` function.

.. code:: python

    @pytest.mark.array_compare(file_format='fits', write_kwargs={'output_verify': 'silentfix'})
    def test_array():
        ...

Other options include the name of the reference directory (which
defaults to ``reference`` ) and the filename for the reference file
(which defaults to the name of the test with a format-dependent
extension).

.. code:: python

    @pytest.mark.array_compare(reference_dir='baseline_arrays',
                                   filename='other_name.fits')
    def test_array():
        ...

The reference directory in the decorator above will be interpreted as
being relative to the test file. Note that the baseline directory can
also be a URL (which should start with ``http://`` or ``https://`` and
end in a slash).

Finally, you can also set a custom baseline directory globally when
running tests by running ``py.test`` with::

    py.test --arraydiff --arraydiff-reference-path=baseline_arrays

This directory will be interpreted as being relative to where the tests
are run. In addition, if both this option and the ``reference_dir``
option in the ``array_compare`` decorator are used, the one in the
decorator takes precedence.

Test failure example
--------------------

If the arrays produced by the tests are correct, then the test will
pass, but if they are not, the test will fail with a message similar to
the following::

    E               AssertionError:
    E
    E               a: /var/folders/zy/t1l3sx310d3d6p0kyxqzlrnr0000gr/T/tmpbvjkzt_q/test_to_mask_rect-mode_subpixels-subpixels_18.txt
    E               b: /var/folders/zy/t1l3sx310d3d6p0kyxqzlrnr0000gr/T/tmpbvjkzt_q/reference-test_to_mask_rect-mode_subpixels-subpixels_18.txt
    E
    E               Not equal to tolerance rtol=1e-07, atol=0
    E
    E               (mismatch 47.22222222222222%)
    E                x: array([[ 0.      ,  0.      ,  0.      ,  0.      ,  0.404012,  0.55    ,
    E                        0.023765,  0.      ,  0.      ],
    E                      [ 0.      ,  0.      ,  0.      ,  0.112037,  1.028704,  1.1     ,...
    E                y: array([[ 0.      ,  0.      ,  0.      ,  0.      ,  0.367284,  0.5     ,
    E                        0.021605,  0.      ,  0.      ],
    E                      [ 0.      ,  0.      ,  0.      ,  0.101852,  0.935185,  1.      ,...

The file paths included in the exception are then available for
inspection.

Running the tests for pytest-arraydiff
--------------------------------------

If you are contributing some changes and want to run the tests, first
install the latest version of the plugin then do::

    cd tests
    py.test --arraydiff

The reason for having to install the plugin first is to ensure that the
plugin is correctly loaded as part of the test suite.
