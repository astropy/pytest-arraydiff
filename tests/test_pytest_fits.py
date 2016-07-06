import os
import subprocess
import tempfile

import pytest
import numpy as np
from astropy.io import fits

baseline_dir = 'baseline'


@pytest.mark.fits_compare(baseline_dir=baseline_dir)
def test_succeeds_func():
    data = np.arange(3 * 5 * 4).reshape((3, 5, 4))
    header = fits.Header()
    header['TEST'] = 'function'
    header['VALUE'] = 1.344
    return fits.PrimaryHDU(data, header)


class TestClass(object):

    @pytest.mark.fits_compare(baseline_dir=baseline_dir)
    def test_succeeds_class(self):
        data = np.arange(2 * 4 * 3).reshape((2, 4, 3))
        header = fits.Header()
        header['TEST'] = 'class'
        header['VALUE'] = 1.344
        return fits.PrimaryHDU(data, header)


TEST_FAILING = """
import pytest
import numpy as np
from astropy.io import fits
@pytest.mark.fits_compare
def test_fail():
    data = np.ones((3,4))
    header = fits.Header()
    header['TEST'] = 'tolerance'
    header['VALUE'] = 2
    return fits.PrimaryHDU(data, header)
"""


def test_fails():

    tmpdir = tempfile.mkdtemp()

    test_file = os.path.join(tmpdir, 'test.py')
    with open(test_file, 'w') as f:
        f.write(TEST_FAILING)

    # If we use --fits, it should detect that the file is missing
    code = subprocess.call('py.test --fits {0}'.format(test_file), shell=True)
    assert code != 0

    # If we don't use --fits option, the test should succeed
    code = subprocess.call('py.test {0}'.format(test_file), shell=True)
    assert code == 0


TEST_GENERATE = """
import pytest
import numpy as np
from astropy.io import fits
@pytest.mark.fits_compare
def test_gen():
    data = np.arange(6 * 5 * 3).reshape((6, 5, 3))
    header = fits.Header()
    header['TEST'] = 'generate'
    header['VALUE'] = 3.14
    return fits.PrimaryHDU(data, header)
"""


def test_generate():

    tmpdir = tempfile.mkdtemp()

    test_file = os.path.join(tmpdir, 'test.py')
    with open(test_file, 'w') as f:
        f.write(TEST_GENERATE)

    gen_dir = os.path.join(tmpdir, 'spam', 'egg')

    # If we don't generate, the test will fail
    p = subprocess.Popen('py.test --fits {0}'.format(test_file), shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    assert b'FITS file not found for comparison test' in p.stdout.read()

    # If we do generate, the test should succeed and a new file will appear
    code = subprocess.call('py.test --fits-generate-path={0} {1}'.format(gen_dir, test_file), shell=True)
    assert code == 0
    assert os.path.exists(os.path.join(gen_dir, 'test_gen.fits'))


@pytest.mark.fits_compare(baseline_dir=baseline_dir, rtol=0.5)
def test_tolerance():
    data = np.ones((3,4)) * 1.6
    header = fits.Header()
    header['TEST'] = 'tolerance'
    header['VALUE'] = 2
    return fits.PrimaryHDU(data, header)


def test_nofile():
    pass
