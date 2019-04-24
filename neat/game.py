import random
import neat

class Game():
    difficultly = 50
    dimention = 25
    def __init__(self):
        self.players = {}
        self.board = [[False for x in range(Game.dimention)] for y in range(Game.dimention)]
        self.start = (0, 0)
        self.end = (24, 24)
        self.player = None
        self.new_board()

    def play(self):
        while self.players:
            for id in list(self.players):
                self.move(self.players[id])
                self.evaluate(self.players[id])

    def setup(self, population):
        self.players = {}
        id = 0
        for species in population.species:
            for genome in species.genomes:
                self.players[id] = Player(genome, id)
                id += 1

    def new_board(self):
        for i in range(1,5):
            for j in range(5):
                self.board[i*5][j*5] = True
        self.board[0][5] = True
        self.board[5][0] = True
        self.board[24][20] = True
        self.board[2][5] = True
        self.board[5][4] = True
        self.board[5][2] = True
        self.board[6][10] = True
        self.board[7][10] = True
        self.board[8][10] = True
        self.board[9][10] = True

    def move_top(self):
        self.move(self.player)
        if not Game.inbounds(self.player.position):
            return True
        elif self.off_path(self.player.position):
            return True
        elif self.player.moves > 100:
            return True
        return False
    def move(self, player):
        inputs = self.get_inputs(player)
        output = player.genome.evaluate(inputs)
        move = Player.moves[min(range(len(output)), key = output.__getitem__)]
        player.position = tuple(map(sum, zip(move, player.position)))
        player.moves += 1
        #input(player.position)

    def evaluate(self, player):
        if not Game.inbounds(player.position):
            self.players.pop(player.id)
        elif self.off_path(player.position):
            self.players.pop(player.id)
        #not progressing
        elif player.moves > 100:
            player.fitness = 1
            self.players.pop(player.id)
        elif player.position == self.end:
            player.genome.fitness = 1000 - player.genome.fitness
            self.players.pop(player.id)
        else:
            x, y = player.position
            player.genome.fitness = x * y


    def get_inputs(self, player):
        inputs = [0,0,0,0,0,0,0,0]

        for i in range(len(Player.vision)):
            position = tuple(map(sum, zip(player.position, Player.vision[i])))
            if not Game.inbounds(position):
                inputs[i] = 1
            elif self.off_path(position):
                inputs[i] = 1
        return inputs

    def off_path(self, position):
        x, y = position

        if self.board[x][y]:
            return True
        return False

    @staticmethod
    def inbounds(position):
        x, y = position
        if 0 <= x < Game.dimention and 0 <= y < Game.dimention:
            return True
        return False


class Player():
    vision = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
    moves = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    def __init__(self, genome, id):
        self.position = (0, 0)
        self.vision = []
        self.moves = 0
        self.genome = genome
        self.id = id
