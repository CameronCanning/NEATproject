from enum import Enum
import random
import copy
import neat

class Mutation():
    class Type(Enum):
        ADD_CONNECTION = 0
        ADD_NODE = 1
        DISABLE_CONNECTION = 2
        WEIGHT = 3

    def __init__(self):
        initial = 1.0/len(Mutation.Type)
        self.mutation_types = { Mutation.Type.ADD_CONNECTION : initial,
                                Mutation.Type.ADD_NODE : initial,
                                Mutation.Type.DISABLE_CONNECTION : initial,
                                Mutation.Type.WEIGHT : initial }
        self.set_thresholds(0.25, 0.03 , 0.02, 0.7)



    def set_thresholds(self, ac, an, dc, w):
        self.mutation_types[Mutation.Type.ADD_CONNECTION] = ac
        self.mutation_types[Mutation.Type.ADD_NODE] = an
        self.mutation_types[Mutation.Type.DISABLE_CONNECTION] = dc
        self.mutation_types[Mutation.Type.WEIGHT] = w

    def get_mutation(self, p):
        threshold = 0.0
        for type, value in self.mutation_types.items():
            threshold += value
            if p < threshold:
                return type
        return False

    def mutate(self, genome):
        p = random.random()
        mutated = False
        mutation = self.get_mutation(p)

        #switch would be better
        if mutation == Mutation.Type.ADD_CONNECTION:
            mutated = self.add_connection(genome)

        elif mutation == Mutation.Type.ADD_NODE:
            mutated = self.add_node(genome)

        elif mutation == Mutation.Type.DISABLE_CONNECTION:
            mutated = self.disable_connection(genome)

        else: #mutation == Type.WEIGHT:
            mutated = self.weight(genome)

        return mutated

    def add_node(self, genome):
        genome.at_node += 1

        if not genome.connections:
            return False

        connection = random.choice(list(genome.connections.values()))

        if not connection.enabled:
            return False

        connection.enabled = False
        genome.at_innovation += 1

        connection1 = copy.copy(connection)
        connection1.out = genome.at_node
        connection1.weight = 1.0
        connection1.enabled = True
        connection1.innovation = genome.at_innovation

        genome.connections[genome.at_innovation] = connection1
        genome.at_innovation += 1

        connection2 = copy.copy(connection)
        connection2.into = genome.at_node
        connection2.enabled = True
        connection2.innovation = genome.at_innovation

        genome.connections[genome.at_innovation] = connection2

        return True


    def add_connection(self, genome):

        into = random.choice(list(genome.nodes.keys()))
        out = random.choice(list(genome.nodes.keys())[neat.Genome.inputs:])

        if into == out:
            return False

        if into > out:
            temp = into
            into = out
            out = temp

        if into >= 1000 and out >= 1000:
            return False

        connection = neat.Connection()
        connection.into = into
        connection.out = out

        for connection2 in genome.connections.values():
            if connection == connection2:
                return False
                
        genome.at_innovation += 1
        connection.innovation = genome.at_innovation
        connection.weight = random.random() * 4 - 2

        genome.connections[genome.at_innovation] = connection

        return True

    def disable_connection(self, genome):
        if not genome.connections:
            return False

        connection = random.choice(list(genome.connections.values()))
        if connection.enabled:
            connection.enabled = False
        else:
            connection.enabled = True
        return True

    def weight(self, genome):
        if not genome.connections:
            return False

        connection = random.choice(list(genome.connections.values()))
        connection.weight += random.random() - 0.5

        return True
