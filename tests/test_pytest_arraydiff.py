import os
import sys
import subprocess
import tempfile

import pytest
import numpy as np

PY2 = sys.version_info[0] == 2

reference_dir = 'baseline'


@pytest.mark.array_compare(reference_dir=reference_dir)
def test_succeeds_func_default():
    return np.arange(3 * 5).reshape((3, 5))


@pytest.mark.array_compare(file_format='text', reference_dir=reference_dir)
def test_succeeds_func_text():
    return np.arange(3 * 5).reshape((3, 5))


@pytest.mark.array_compare(file_format='fits', reference_dir=reference_dir)
def test_succeeds_func_fits():
    return np.arange(3 * 5).reshape((3, 5)).astype(np.int64)


@pytest.mark.array_compare(file_format='fits', reference_dir=reference_dir)
def test_succeeds_func_fits_hdu():
    from astropy.io import fits
    return fits.PrimaryHDU(np.arange(3 * 5).reshape((3, 5)).astype(np.int64))


class TestClass(object):

    @pytest.mark.array_compare(file_format='fits', reference_dir=reference_dir)
    def test_succeeds_class(self):
        return np.arange(2 * 4 * 3).reshape((2, 4, 3)).astype(np.int64)


TEST_FAILING = """
import pytest
import numpy as np
from astropy.io import fits
@pytest.mark.array_compare
def test_fail():
    return np.ones((3, 4))
"""


def test_fails():

    tmpdir = tempfile.mkdtemp()

    test_file = os.path.join(tmpdir, 'test.py')
    with open(test_file, 'w') as f:
        f.write(TEST_FAILING)

    # If we use --arraydiff, it should detect that the file is missing
    code = subprocess.call('py.test --arraydiff {0}'.format(test_file), shell=True)
    assert code != 0

    # If we don't use --arraydiff option, the test should succeed
    code = subprocess.call('py.test {0}'.format(test_file), shell=True)
    assert code == 0


TEST_GENERATE = """
import pytest
import numpy as np
from astropy.io import fits
@pytest.mark.array_compare(file_format='{file_format}')
def test_gen():
    return np.arange(6 * 5).reshape((6, 5))
"""


@pytest.mark.parametrize('file_format', ('fits', 'text'))
def test_generate(file_format):

    tmpdir = tempfile.mkdtemp()

    test_file = os.path.join(tmpdir, 'test.py')
    with open(test_file, 'w') as f:
        f.write(TEST_GENERATE.format(file_format=file_format))

    gen_dir = os.path.join(tmpdir, 'spam', 'egg')

    # If we don't generate, the test will fail
    try:
        if PY2:
            subprocess.check_output(['pytest', '--arraydiff', test_file])
        else:
            subprocess.check_output(['pytest', '--arraydiff', test_file], timeout=10)
    except subprocess.CalledProcessError as grepexc:
        assert b'File not found for comparison test' in grepexc.output

    # If we do generate, the test should succeed and a new file will appear
    if PY2:
        code = subprocess.call(['pytest', '--arraydiff-generate-path={0}'.format(gen_dir), test_file])
    else:
        code = subprocess.call(['pytest', '--arraydiff-generate-path={0}'.format(gen_dir), test_file],
                               timeout=10)
    assert code == 0
    assert os.path.exists(os.path.join(gen_dir, 'test_gen.' + ('fits' if file_format == 'fits' else 'txt')))


TEST_DEFAULT = """
import pytest
import numpy as np
from astropy.io import fits
@pytest.mark.array_compare
def test_default():
    return np.arange(6 * 5).reshape((6, 5))
"""

@pytest.mark.parametrize('file_format', ('fits', 'text'))
def test_default_format(file_format):

    tmpdir = tempfile.mkdtemp()

    test_file = os.path.join(tmpdir, 'test.py')
    with open(test_file, 'w') as f:
        f.write(TEST_DEFAULT)

    gen_dir = os.path.join(tmpdir, 'spam', 'egg')

    # If we do generate, the test should succeed and a new file will appear
    code = subprocess.call('py.test -s --arraydiff-default-format={0}'
                           ' --arraydiff-generate-path={1} {2}'.format(file_format, gen_dir, test_file), shell=True)
    assert code == 0
    assert os.path.exists(os.path.join(gen_dir, 'test_default.' + ('fits' if file_format == 'fits' else 'txt')))


@pytest.mark.array_compare(reference_dir=reference_dir, rtol=0.5, file_format='fits')
def test_tolerance():
    return np.ones((3,4)) * 1.6


def test_nofile():
    pass
