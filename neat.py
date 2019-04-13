import random
from scipy.special import expit
from enum import Enum

class Node():
    LayerTypes = Enum('LayerTypes', 'I O H')
    def __init__(self, id, type = 'H'):
        self.id = id
        self.type = Node.LayerTypes[type]
        self.value = 0.0
        self.incoming = set()
    def __str__(self):
        return str(self.id)
    @staticmethod
    def sigmoid(self):
        return expit(self.value)

class Connection():
    def __init__(self, weight, enabled, innovation = -1, from_node = None, to_node = None):
        self.from_node = from_node
        #self.to_node = to_node
        self.weight = weight
        self.enabled = enabled
        self.innovation = innovation

    def disable(self):
        self.enabled = False

class Genome():
    input_size = 3*3
    output_size = 2
    max_nodes = 10000
    @staticmethod
    def mutate(g_1, g_2):
        return g_1

    def __init__(self):
        self.nodes = []
        self.input_nodes = []
        self.input_size = 0
        self.connections = {}
        self.fitness = 0
    #creates simple genome
    def generate_simple(self):
        #create input nodes
        for i in range(Genome.input_size):
            input_node = Node(i, 'I')
            self.nodes.append(node)
            self.input_nodes.append(node)
        for i in range(Genome.output_size):
            output_node = Node(Genome.max_nodes+i, 'O')
            for node in self.input_nodes:
                output_node.incoming.add(node)
            self.nodes[Genome.max_nodes+i] = Node(Genome.max_nodes+i)

    def evaluate(self, inputs):
        #nodes are kept in order
        for i in range(len(inputs)):


class Species():
    def __init__(self):
        self.genomes = {}
        self.topFitness = 0
        self.averageFitness = 0

class Pool():
    def __init__(self):
        self.species = {}

genome = Genome()
genome.generate_simple()
for g in genome.nodes:
    print(g)
for x in genome.nodes[10000].incoming:
    print(x)
