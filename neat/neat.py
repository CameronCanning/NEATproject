import random
import copy
import mutation
import game
import sys
from collections import OrderedDict
from scipy.special import expit

class Population():

    def __init__(self):
        self.species = []
        self.size = 0
        self.max_size = 100
        self.top_genome = None
        self.average_fitness = 0
        self.generation = 0
        self.innovation = 0
        self.mutation = mutation.Mutation()
        self.game = game.Game()
        for i in range(self.max_size):
            genome = Genome()
            genome.create_simple()
            self.add_genome(genome)
        self.evaluate_fitness()
        self.rank_and_remove(False)

    @staticmethod
    def same_species(genome1, genome2):
        delta_threshold = 1
        c_de = 2.0
        c_w = 0.4
        delta_de = c_de * Population.disjoint_amount(genome1, genome2)
        delta_w = c_w * Population.weight_difference(genome1, genome2)
        return delta_de + delta_w < delta_threshold

    @staticmethod
    def weight_difference(genome1, genome2):
        sum = 0
        connections = 0
        for innovation in genome1.connections:
            if innovation in genome2.connections:
                sum += abs(genome1.connections[innovation].weight -
                           genome2.connections[innovation].weight)
                connections += 1
        if connections == 0:
            return 0
        return sum / connections

    @staticmethod
    def disjoint_amount(genome1, genome2):
        innovations1 = set(genome1.connections.keys())
        innovations2 = set(genome2.connections.keys())
        overlap = innovations1 & innovations2
        disjoint1 = innovations1 - overlap
        disjoint2 = innovations2 - overlap
        return len(disjoint1) + len(disjoint2)

    def add_genome(self, genome):
        found_species = False
        self.size += 1
        for species in self.species:
            if Population.same_species(random.choice(species.genomes), genome):
                species.genomes.append(genome)
                found_species = True
                break

        if not found_species:
            new_species = Species()
            new_species.genomes.append(genome)
            self.species.append(new_species)

    def evaluate_fitness(self):
        self.game.setup(self)
        self.game.play()

    def breed(self):
        while self.size < self.max_size:
            for species in self.species:
                if species.genomes:
                    genome1 = random.choice(species.genomes)
                    genome2 = random.choice(species.genomes)
                    child = genome1.crossover(genome2)
                    child.generate_nodes()
                    self.mutation.mutate(child)
                    child.generate_nodes()
                    self.add_genome(child)


    def next_generation(self, amount = 1):
        for i in range(amount):
            self.rank_and_remove(True)
            self.breed()
            self.evaluate_fitness()
            self.generation += 1

    def rank_and_remove(self, remove):
        self.size = 0
        for i in range(len(self.species)):
            if self.species[i].genomes:
                self.species[i].genomes.sort(key = lambda genome: genome.fitness, reverse = True)
                if remove:
                    size = len(self.species[i].genomes)
                    if size > 1:
                        amount = int(size/2)
                        self.size += amount
                        self.species[i].genomes = self.species[i].genomes[:amount]
            else:
                self.species.pop(i)

        total_pop = 0
        for species in self.species:
            total_species = 0
            for genome in species.genomes:
                total_species += genome.fitness
            species.top_genome = species.genomes[0]

            if self.top_genome:
                if species.top_genome.fitness > self.top_genome.fitness:
                    self.top_genome = species.top_genome
            else:
                self.top_genome = species.top_genome

            species.average_fitness = total_species/len(species.genomes)
            total_pop += species.average_fitness

        self.average_fitness = total_pop/len(self.species)

    def setup_player(self):
        self.game.player = game.Player(self.top_genome, -1)

class Species():
    def __init__(self):
        self.genomes = []
        self.top_genome = None
        self.average_fitness = 0

class Connection():
    # into out
    # o----o
    def __init__(self):
        self.into = None
        self.out = None
        self.weight = 0.0
        self.enabled = True
        self.innovation = None
    def __str__(self):
        return str((self.into, self.out))
    def __eq__(self, other):
        return (self.into, self.out) == (other.into, other.out)
    def __hash__(self):
        return hash((self.into, self.out))


class Node():
    def __init__(self, id = None, layer = 0):
        self.id = id
        self.incoming = set()
        self.value = 0.0
        self.layer = layer
    def __str__(self):
        return str(self.id)
    def __lt__(self, other):
        return self.id < other.id
    def __eq__(self, other):
        return self.id == other.id
    def __hash__(self):
        return hash(self.id)

class Genome():
    inputs = 8
    outputs = 4
    max_nodes = 1000
    def __init__(self):
        self.connections = OrderedDict()
        self.nodes = OrderedDict()
        self.fitness = 0
        self.at_innovation = 0
        self.at_node = 0

    def __str__(self):
        string = 'Top Genome:\n'
        for connection in self.connections.values():
            string += (str((str(connection), round(connection.weight,3), connection.enabled))) +'\n'
        return string

    def generate_nodes(self):
        self.nodes = {}
        self.at_node = Genome.inputs - 1
        for i in range(Genome.inputs):
            self.nodes[i] = Node(i)

        for i in range(Genome.outputs):
            self.nodes[Genome.max_nodes + i] = Node(Genome.max_nodes + i)

        #for i in range(len(self.connections)):
        for connection in self.connections.values():
            #connection = self.connections[i]
            if connection.enabled:
                if connection.out not in self.nodes:
                    self.nodes[connection.out] = Node(connection.out)
                    if connection.out > self.at_node:
                        at_node = connection.out
                node = self.nodes[connection.out]
                node.incoming.add(connection)
                if connection.into not in self.nodes:
                    self.nodes[connection.into] = Node(connection.into)
                    if connection.into > self.at_node:
                        at_node = connection.out


    def create_simple(self):
        innovation = 0
        #create connections
        for i in range(Genome.inputs):
            for o in range(Genome.outputs):
                connection = Connection()
                connection.into = i
                connection.out = Genome.max_nodes + o
                connection.weight = random.random() * 4 - 2
                self.connections[innovation] = connection
                innovation += 1
        self.at_innovation = innovation
        self.generate_nodes()

    def evaluate(self, inputs):
        if Genome.inputs != len(inputs):
            raise ValueError('Inputs wrong size')

        for i in range(Genome.inputs):
            self.nodes[i].value = inputs[i]

        for node in self.nodes.values():
            sum = 0
            for connection in node.incoming:
                from_node = self.nodes[connection.into]
                sum += connection.weight * from_node.value
            if node.incoming:
                node.value = expit(sum)

        outputs = []
        for i in range(Genome.outputs):
            outputs.append(self.nodes[Genome.max_nodes + i].value)
        return outputs

    def crossover(self, other):
        child = Genome()
        if self.fitness > other.fitness:
            genome1 = self
            genome2 = other
        else:
            genome1 = other
            genome2 = self

        innovations1 = set(genome1.connections.keys())
        innovations2 = set(genome2.connections.keys())
        overlap = innovations1 & innovations2
        disjoint1 = innovations1 - overlap
        disjoint2 = innovations2 - overlap


        for innovation in overlap:
            if random.random() < 0.5:
                child.connections[innovation] = copy.copy(self.connections[innovation])
            else:
                child.connections[innovation] = copy.copy(other.connections[innovation])

        for innovation in disjoint1:
            child.connections[innovation] = copy.copy(self.connections[innovation])

        child.at_innovation = max(self.at_innovation, other.at_innovation)

        #todo copy mutationRates

        return child
