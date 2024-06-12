import unittest

from server import server



class TestPktBuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.server = server.Listener('127.0.0.1', 8877)
    
    def tearDown(self) -> None:
        self.server.close()
    
    def test_send