0.6.1 (2023-11-27)
------------------

- Fix broken ``single_reference=True`` usage. [#43]

0.6 (2023-11-15)
----------------

- Add ability to compare to Pandas DataFrames and store them as HDF5 files [#23]

- Fix ``array_compare`` so that the ``atol`` parameter is correctly used with
  FITS files. [#33]

- Test inside ``pytest_runtest_call`` hook. [#36]

0.5 (2022-01-12)
----------------

- Removed `astropy` as required dependency. [#31]

- Formally register `array_compare` as marker.

0.4 (2021-12-31)
----------------

- Minimum Python version is now 3.7. [#30]

- Various infrastructure updates.

0.3 (2018-12-05)
----------------

- Fixed compatibility with pytest 4+. [#15]

0.2 (2018-01-29)
----------------

- Fix compatibility with recent versions of Astropy and Numpy. [#8, #10]

- Add back support for returning HDUs from tests. [#5]

0.1 (2016-11-26)
----------------

- Initial version
