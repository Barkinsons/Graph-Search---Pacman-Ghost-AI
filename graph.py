import pygame as pg

from settings import Settings as S

class Node:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.rect = pg.Rect(x * S.tile_size, y * S.tile_size, S.tile_size, S.tile_size)
        self.neighbors = []

    def add_neighbor(self, node):
        self.neighbors.append(node)

class Graph:

    def __init__(self, game):
        self.game = game

        self.graph = {}

        with open('map.txt', 'r') as f:
            lines = f.readlines()

        self.height = len(lines)
        self.width = len(lines[0]) - 1

        self.image = pg.transform.scale(pg.image.load(f'images/maze0.png'), (self.width * S.tile_size, self.height * S.tile_size))
        self.rect = self.image.get_rect()

        for y in range(self.height):
            for x in range(self.width):
                if lines[y][x] == 'O':
                    self.graph[f'{x}-{y}'] = Node(x, y)

        for n in self.graph.values():
                x, y = n.x, n.y
                
                # Left neighbor
                if f'{x-1}-{y}' in self.graph:
                    self.graph[f'{x}-{y}'].add_neighbor(self.graph[f'{x-1}-{y}']) 
                # Top neighbor
                if f'{x}-{y-1}' in self.graph:
                    self.graph[f'{x}-{y}'].add_neighbor(self.graph[f'{x}-{y-1}'])
                # Right neighbor
                if f'{x+1}-{y}' in self.graph:
                    self.graph[f'{x}-{y}'].add_neighbor(self.graph[f'{x+1}-{y}'])
                # Bottom neighbor
                if f'{x}-{y+1}' in self.graph:
                    self.graph[f'{x}-{y}'].add_neighbor(self.graph[f'{x}-{y+1}'])


    def update(self):
        self.draw()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
