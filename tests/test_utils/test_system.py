#  -*- coding: utf-8 -*-

import pytest

from spectrochempy.utils import (
    get_user,
    get_user_and_node,
    get_node,
    is_kernel,
    sh,
    is_windows,
)


def test_get_user():
    res = get_user()
    assert res is not None


def test_get_node():
    res = get_node()
    assert res is not None


def test_get_user_and_node():
    res = get_user_and_node()
    assert res is not None


def test_is_kernel():
    res = is_kernel()
    assert not res


# @pytest.mark.skip("problem with one of the commit - look at this later")
@pytest.mark.skipif(
    is_windows(), reason="Fail under Windows OS due to one of the commits"
)
def test_sh():
    res = sh.git("show", "HEAD")
    assert res is not None
