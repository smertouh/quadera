# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-
#
# =============================================================================
# Copyright (©) 2015-2018 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
#
# This software is a computer program whose purpose is to [describe
# functionalities and technical features of your software].
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software. You can use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading, using, modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and, more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# =============================================================================

from copy import copy, deepcopy

import numpy as np
import pytest
from traitlets import TraitError
from datetime import datetime

from pint import DimensionalityError
from spectrochempy.api import NDArray
from spectrochempy.api import ur
from tests.utils import (raises)
from spectrochempy.core.units import ur
from spectrochempy.utils import SpectroChemPyWarning
from tests.utils import (assert_equal, assert_array_equal,
                         assert_array_almost_equal, assert_equal_units,
                         raises)
from tests.utils import NumpyRNGContext


# fixtures
# --------
@pytest.fixture(scope="module")
def ndarraysubclass():
    # return a simple ndarray
    # with some data
    with NumpyRNGContext(12345):
        dx = 10.*np.random.random((10, 10))-5.
    _nd = MinimalSubclass()
    _nd.data = dx
    return _nd.copy()

@pytest.fixture(scope="module")
def ndarraysubclasscplx():
    # return a complex ndarray
    # with some complex data
    with NumpyRNGContext(1245):
        dx = np.random.random((10, 20))
    _nd = MinimalSubclass()
    _nd.data = dx
    _nd.set_complex(axis=-1)  # this means that the data are complex in
    # the last dimension
    return _nd.copy()

# test initialization
# --------------------

class MinimalSubclass(NDArray):
    # in principle NDArray is not used directly and should be subclassed
    pass

def test_init_ndarray_subclass():
    # test initialization of an empty ndarray
    # check some of its properties
    a = MinimalSubclass()
    assert isinstance(a, NDArray)
    assert a.name != u'<no name>'  # must be the uuid in this case
    assert a.is_empty
    assert not a.is_masked
    assert not a.is_uncertain
    assert a.unitless
    assert a.is_untitled
    assert not a.meta
    assert a.date == datetime(1, 1, 1, 0, 0)
    a.date = datetime(2005,10,12)
    a.date = "25/12/2025"
    assert a.date == datetime(2025, 12, 25, 0, 0)

def test_set_ndarray_subclass():
    # test of setting some attributes of an empty ndarray
    # check some of its properties
    a = MinimalSubclass()
    a.name = 'xxxx'
    assert a.name == u'xxxx'
    a.title = 'yyyy'
    assert not a.is_untitled
    assert a.title == u"yyyy"
    a.meta = []
    a.meta.something = "a_value"
    assert a.meta.something == "a_value"

def test_set_simple_ndarray(ndarraysubclass):
    nd = ndarraysubclass.copy()
    assert nd.data.size == 100
    assert nd.shape == (10, 10)
    assert nd.size == 100
    assert nd.ndim == 2
    assert nd.is_complex == [False, False]
    assert nd.data[1,1] == 4.6130673607282127

def test_set_ndarray_with_units(ndarraysubclass):
    nd = ndarraysubclass.copy()

    assert nd.unitless # ,o units
    assert not nd.dimensionless # no unit so no dimension has no sense

    #with catch_warnings() as w:
    nd.to('m')  # should not change anything (but raise a warning)
    #assert w[0].category == SpectroChemPyWarning

    assert nd.unitless

    nd.units = 'm'
    assert nd.units == ur.meter

    nd1 = nd.to('km')
    assert nd.units == ur.kilometer
    assert nd1.units == ur.kilometer
    #with catch_warnings() as w:
    nd.ito('m')
    #assert w[0].category == SpectroChemPyDeprecationWarning
    nd.to('m')
    assert nd.units == ur.meter

    # change of units - ok if it can be casted to the current one
    nd.units = 'cm'

    # cannot change to incompatible units
    with pytest.raises(ValueError):
        nd.units = 'radian'

    # we can force them
    nd.change_units('radian')

    assert 1 * nd.units == 1. * ur.dimensionless
    assert nd.units.dimensionless
    assert nd.dimensionless
    with raises(DimensionalityError):
        nd1 = nd1.ito('km/s')  # should raise an error
    nd.units = 'm/km'
    assert nd.units.dimensionless
    assert nd.units.scaling == 0.001

    with raises(TypeError):
        nd.change_units(1 * ur.m)  # cannot use a quantity to set units


def test_set_ndarray_with_complex(ndarraysubclasscplx):
    nd = ndarraysubclasscplx.copy()
    assert nd.data.size == 200
    assert nd.size == 100
    assert nd.data.shape == (10, 20)
    assert nd.shape == (10, 10)  # the real shape
    assert nd.is_complex == [False, True]
    assert nd.ndim == 2
    nd.units = 'meter'
    assert nd.units == ur.meter


def test_copy_of_ndarray(ndarraysubclasscplx):
    nd = copy(ndarraysubclasscplx)
    assert nd is not ndarraysubclasscplx
    assert nd.data.size == 200
    assert nd.size == 100
    assert nd.data.shape == (10, 20)
    assert nd.shape == (10, 10)  # the real shape
    assert nd.is_complex == [False, True]
    assert nd.ndim == 2


def test_deepcopy_of_ndarray(ndarraysubclasscplx):
    # for this example there is no diif with copy (write another test for this)
    nd1 = ndarraysubclasscplx.copy()
    nd = deepcopy(nd1)
    assert nd is not nd1
    assert nd.data.size == 200
    assert nd.size == 100
    assert nd.data.shape == (10, 20)
    assert nd.shape == (10, 10)  # the real shape
    assert nd.is_complex == [False, True]
    assert nd.ndim == 2


def test_ndarray_with_uncertaincy(ndarraysubclass):
    nd = ndarraysubclass.copy()
    assert not nd.is_uncertain
    assert repr(nd).startswith('NDArray:')
    nd._uncertainty = np.abs(nd._data * .01)
    nd.change_units('second') # force a change of units
    assert nd.is_uncertain
    assert str(nd).startswith('NDArray:')
    assert str(nd.values[0,0]) == "4.30+/-0.04 second"
    print(nd)


def test_ndarray_with_mask(ndarraysubclass):
    nd = ndarraysubclass.copy()
    print(nd)
    assert not nd.is_masked
    assert str(nd).startswith('NDArray:')
    nd._mask[0] = True
    assert nd.is_masked
    print(nd)


def test_ndarray_units(ndarraysubclass):
    nd = ndarraysubclass.copy()
    nd2 = ndarraysubclass.copy()
    nd.units = 'm'
    nd2.units = 'km'
    assert nd.is_units_compatible(nd2)
    nd2.change_units('radian')
    assert not nd.is_units_compatible(nd2)


def test_ndarray_with_uncertaincy_and_units(ndarraysubclass):
    nd = ndarraysubclass.copy()
    nd.change_units('m')
    assert nd.units == ur.meter
    assert not nd.is_uncertain
    assert repr(nd).startswith('NDArray:')
    nd._uncertainty = np.abs(nd._data * .01)
    assert nd.is_uncertain
    assert str(nd).startswith('NDArray:')
    units = nd.units
    nd.units = None # should change nothing
    assert nd.units == units
    nd._mask[1,1] = True
    assert nd.is_masked
    print(nd)


def test_ndarray_with_uncertaincy_and_units_being_complex(ndarraysubclasscplx):
    nd = ndarraysubclasscplx.copy()
    nd.units = 'm'
    assert nd.units == ur.meter
    assert not nd.is_uncertain
    assert repr(nd).startswith('NDArray:')
    nd._uncertainty = nd._data * .01
    assert nd.is_uncertain
    assert str(nd).startswith('NDArray:')
    #print(nd)
    assert nd._uncertainty.size == nd.data.size


def test_ndarray_len_and_sizes(ndarraysubclass, ndarraysubclasscplx):
    nd = ndarraysubclass.copy()
    #print(nd.is_complex)
    assert not nd.is_complex[0]
    assert len(nd) == 10
    assert nd.shape == (10, 10)
    assert nd.size == 100
    assert nd.ndim == 2

    nd = ndarraysubclasscplx.copy()
    #print(nd.is_complex)
    assert nd.is_complex[1]
    assert len(nd) == 10
    assert nd.shape == (10, 10)
    assert nd.size == 100
    assert nd.ndim == 2


def test_slicing_byindex(ndarraysubclass):
    nd = ndarraysubclass.copy()
    nd3 = nd[7:10]
    assert_equal(nd3.data,nd.data[7:10])