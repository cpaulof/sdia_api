import unittest

from server import pkt_builder as p



class TestPktBuilder(unittest.TestCase):
    def test_build_uint32(self):
        ex1 = b"\x00\x00\x00\x01" # 1
        ex2 = b'\x00\x00\x13\x88' # 5000
        ex3 = b'\xff\xff\xff\xfe' # 4294967294
        self.assertEqual(p._build_uint32(1), ex1)
        self.assertEqual(p._build_uint32(5000), ex2)
        self.assertEqual(p._build_uint32(4294967294), ex3)
    
    def test_build_int32(self):
        ex1 = b"\x00\x00\x00\x01" # 1
        ex2 = b'\x00\x00\x13\x88' # 5000
        ex3 = b'\xff\xff\xff\xfe' # -2
        self.assertEqual(p._build_int32(1), ex1)
        self.assertEqual(p._build_int32(5000), ex2)
        self.assertEqual(p._build_int32(-2), ex3)
    
    def test_build_float(self):
        ex1 = b'A(\x00\x00' # 10.5
        ex2 = b'\xc1(\x00\x00' # -10.5

        self.assertEqual(p._build_float(10.5), ex1)
        self.assertEqual(p._build_float(-10.5), ex2)
    
    def test_build_string(self):
        ex1 = b'\x00\x00\x00\x0b-2.44:44.56' # 10.5
        ex2 = b'\x00\x00\x00\x10\x00Invalid params\x00' # -10.5

        self.assertEqual(p._build_string('-2.44:44.56'), ex1)
        self.assertEqual(p._build_string('\x00Invalid params\x00'), ex2)
    
    def test_build_bool(self):
        ex1 = b'\x00' # False
        ex2 = b'\x01' # True

        self.assertEqual(p._build_bool(False), ex1)
        self.assertEqual(p._build_bool(True), ex2)
    
    def test_build_int8(self):
        ex1 = b'\x0a' # 10
        ex2 = b'\xfe' # -2

        self.assertEqual(p._build_int8(10), ex1)
        self.assertEqual(p._build_int8(-2), ex2)

    def test_build_uint8(self):
        ex1 = b'\x0a' # 10
        ex2 = b'\xfe' # 254

        self.assertEqual(p._build_uint8(10), ex1)
        self.assertEqual(p._build_uint8(254), ex2)

