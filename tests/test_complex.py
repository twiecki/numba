#! /usr/bin/env python
# ______________________________________________________________________
'''test_complex

Test Numba's ability to generate code that supports complex numbers.
'''
# ______________________________________________________________________

import unittest

from numba.decorators import numba_compile
from numba.utils import debugout

import numpy
import itertools

# ______________________________________________________________________

def get_real_fn (in_num):
    return in_num.real

def get_imag_fn (in_num):
    ret_val = in_num.imag
    return ret_val

def get_conj_fn (in_num):
    return in_num.conjugate()

def get_complex_constant_fn ():
    return (3. + 4.j).conjugate()

def prod_sum_fn (coeff, inval, ofs):
    #debugout('prod_sum_fn(): coeff = ', coeff, ', inval = ', inval, ', ofs = ',
    #         ofs)
    ret_val = (coeff * inval) + ofs
    #debugout('prod_sum_fn() ==> ', ret_val)
    return ret_val

# ______________________________________________________________________

class TestComplex (unittest.TestCase):
    def test_get_real_fn (self):
        num0 = 3 + 2j
        num1 = numpy.complex128(num0)
        compiled_get_real_fn = numba_compile(arg_types = ['D'])(get_real_fn)
        self.assertEqual(compiled_get_real_fn(num0), 3.)
        self.assertEqual(get_real_fn(num0), compiled_get_real_fn(num0))
        self.assertEqual(compiled_get_real_fn(num1), 3.)
        self.assertEqual(get_real_fn(num1), compiled_get_real_fn(num1))

    def test_get_imag_fn (self):
        num0 = 0 - 2j
        num1 = numpy.complex128(num0)
        compiled_get_imag_fn = numba_compile(arg_types = ['D'])(get_imag_fn)
        self.assertEqual(compiled_get_imag_fn(num0), -2.)
        self.assertEqual(get_imag_fn(num0), compiled_get_imag_fn(num0))
        self.assertEqual(compiled_get_imag_fn(num1), -2.)
        self.assertEqual(get_imag_fn(num1), compiled_get_imag_fn(num1))

    def test_get_conj_fn (self):
        num0 = 4 - 1.5j
        num1 = numpy.complex128(num0)
        compiled_get_conj_fn = numba_compile(arg_types = ['D'],
                                             ret_type = 'D')(get_conj_fn)
        self.assertEqual(compiled_get_conj_fn(num0), 4 + 1.5j)
        self.assertEqual(get_conj_fn(num0), compiled_get_conj_fn(num0))
        self.assertEqual(compiled_get_conj_fn(num1), 4 + 1.5j)
        self.assertEqual(get_conj_fn(num1), compiled_get_conj_fn(num1))

    def test_get_complex_constant_fn (self):
        compiled_get_complex_constant_fn = numba_compile(
            arg_types = [], ret_type = 'D')(get_complex_constant_fn)
        self.assertEqual(get_complex_constant_fn(),
                         compiled_get_complex_constant_fn())

    def test_prod_sum_fn (self):
        compiled_prod_sum_fn = numba_compile(arg_types = ['D', 'D', 'D'],
                                             ret_type = 'D')(prod_sum_fn)
        rng = numpy.arange(-1., 1.1, 0.5)
        for ar, ai, xr, xi, br, bi in itertools.product(rng, rng, rng, rng, rng,
                                                        rng):
            a = numpy.complex128(ar + ai * 1j)
            x = numpy.complex128(xr + xi * 1j)
            b = numpy.complex128(br + bi * 1j)
            self.assertEqual(prod_sum_fn(a, x, b),
                             compiled_prod_sum_fn(a, x, b))

# ______________________________________________________________________

if __name__ == "__main__":
    unittest.main()

# ______________________________________________________________________
# End of test_complex.py
