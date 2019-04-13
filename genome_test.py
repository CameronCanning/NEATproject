import unittest
import neat
class TestGenome(unittest.TestCase):
    def setUp(self):
        self.input_size = 9
        self.output_size = 2
        self.genome = Genome()

    def test_basic(self):
        
