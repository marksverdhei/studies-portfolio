import numpy as np
from scipy.sparse import csr_matrix
import unittest
from ctypes import *

LIB_PATH = "bin/snn.so"
SIMPLE_GRAPH_PATH = b"data/simple-graph.txt"

char_dp = POINTER(POINTER(c_char))

class TestSNN(unittest.TestCase):

    def setUp(self):
        self.lib = lib = CDLL(LIB_PATH)

        lib.read_graph_from_file1.argtypes = [
            c_char_p, POINTER(c_int),
            POINTER(char_dp),
        ]

        lib.read_graph_from_file2.argtypes = [
            POINTER(c_char), POINTER(c_int),
            POINTER(c_int), POINTER(c_int)
        ]

        self.simple_graph_matrix = [
            [0, 1, 1, 1, 0],
            [1, 0, 1, 1, 0],
            [1, 1, 0, 1, 1],
            [1, 1, 1, 0, 1],
            [0, 0, 1, 1, 0]
        ]

        self.simple_csr = csr_matrix(self.simple_graph_matrix)

    def call_read_graph_from_file(self, filename):
        N = c_int(0)
        table2D = char_dp()
        self.lib.read_graph_from_file1(
            filename,
            byref(N),
            byref(table2D)
        )

        return N, table2D

    # TESTS START HERE

    def test_read_graph_from_file1(self):
        N, table2D = self.call_read_graph_from_file(SIMPLE_GRAPH_PATH)
        n = N.value
        self.assertEqual(n, 5)

        # This will segfault if N is inccorect
        table_data = [[ord(table2D[i][j]) for j in range(n)] for i in range(n)]

        self.assertEqual(self.simple_graph_matrix, table_data)


    def test_read_graph_from_file2(self):
        # N = c_int(0)
        # self.lib.read_graph_from_file2(
        #     SIMPLE_GRAPH_PATH,
        #
        # )
        # n = N.value
        pass

    def test_create_snn_graph1(self):
        raise NotImplementedError("Implement this test when you get here")

    def test_create_snn_graph2(self):
        raise NotImplementedError("Implement this test when you get here")



if __name__ == '__main__':
    unittest.main()
