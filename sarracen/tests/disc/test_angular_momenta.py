import pandas as pd
import numpy as np
from numpy.testing import assert_array_equal, assert_allclose
from sarracen import SarracenDataFrame
from sarracen.disc import angular_momenta
import pytest


def test_mass_equivalency():
    """ Column mass result should equal global params mass result. """

    # randomly place particles
    rng = np.random.default_rng(seed=5)
    x = rng.random(100)
    y = rng.random(100)
    z = rng.random(100)
    vx = rng.random(100)
    vy = rng.random(100)
    vz = rng.random(100)
    mass = [3.2e-4] * 100

    sdf = SarracenDataFrame(data={'x': x, 'y': y, 'z': z,
                                  'vx': vx, 'vy': vy, 'vz': vz,
                                  'mass': mass})
    Lx1, Ly1, Lz1 = angular_momenta(sdf)

    sdf = SarracenDataFrame(data={'x': x, 'y': y, 'z': z,
                                  'vx': vx, 'vy': vy, 'vz': vz},
                            params={'mass': 3.2e-4})
    Lx2, Ly2, Lz2 = angular_momenta(sdf)

    assert_array_equal(Lx1, Lx2)
    assert_array_equal(Ly1, Ly2)
    assert_array_equal(Lz1, Lz2)


def test_parts_vs_whole():
    """ Profiles should be the same for matching bins. """

    # randomly place particles
    rng = np.random.default_rng(seed=5)
    x = rng.random(100)
    y = rng.random(100)
    z = rng.random(100)
    vx = rng.random(100)
    vy = rng.random(100)
    vz = rng.random(100)
    mass = [3.2e-4] * 100

    sdf = SarracenDataFrame(data={'x': x, 'y': y, 'z': z,
                                  'vx': vx, 'vy': vy, 'vz': vz,
                                  'mass': mass})
    Lx_in, Ly_in, Lz_in = angular_momenta(sdf, r_in=0.0, r_out=0.5, bins=100)
    Lx_out, Ly_out, Lz_out = angular_momenta(sdf, r_in=0.5, r_out=1.0, bins=100)
    Lx_all, Ly_all, Lz_all = angular_momenta(sdf, r_in=0.0, r_out=1.0, bins=200)

    assert_array_equal(Lx_in, Lx_all[:100])
    assert_array_equal(Lx_out, Lx_all[100:])
    assert_array_equal(Ly_in, Ly_all[:100])
    assert_array_equal(Ly_out, Ly_all[100:])
    assert_array_equal(Lz_in, Lz_all[:100])
    assert_array_equal(Lz_out, Lz_all[100:])