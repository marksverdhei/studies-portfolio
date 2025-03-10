from ctypes import *
import unittest


class TestFoo(unittest.TestCase):
    def setUp(self):
        self.lib = lib = CDLL("./foo.so")
        lib.get42.restype = c_int

        lib.get32.restype = c_char

        lib.mul_2.argtypes = [c_double]
        lib.mul_2.restype = c_double

    def test_get42(self):
        result = self.lib.get42()
        self.assertEqual(result, 42)
        result = self.lib.get42()
        self.assertEqual(result, 42)

    def test_get32(self):
        result = self.lib.get32()
        self.assertEqual(result, b" ")
        n = ord(result)
        self.assertEqual(n, 32)

    def test_mul_2(self):
        self.assertEqual(self.lib.mul_2(5.), 10.)
        self.assertEqual(self.lib.mul_2(10.), 20.)

if __name__ == '__main__':
    unittest.main()
