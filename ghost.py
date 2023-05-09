import pygame as pg

from animation import Animation
from settings import Settings as S

class Ghost:


    def __init__(self, type, algo, game):

        self.game = game
        self.screen = game.screen
        self.pacman = game.pacman

        # Graph Finding Attributes
        self.graph = game.graph.graph
        self.algo = algo
        self.path = None

        images = [[pg.transform.scale(pg.image.load(f'images/{type}{i}{j}.png'), (S.tile_size*2, S.tile_size*2)) for j in range(2)] for i in range(4)]

        # Animation Attributes
        self.right_anim = Animation(images[0], delay = 0.25, is_loop=True)
        self.up_anim    = Animation(images[1], delay = 0.25, is_loop=True)
        self.left_anim  = Animation(images[2], delay = 0.25, is_loop=True)
        self.down_anim  = Animation(images[3], delay = 0.25, is_loop=True)

        # Position Attributes
        self.rect = images[0][0].get_rect()
        self.rect.center = self.get_pos(21, 17)

        # Movement Attributes
        self.speed = 80 # pixels per second
        self.alpha = self.secs = 0
        self.cur_direction = 'left'
        self.direction = None
        self.moving = False

    def update(self):

        # Update Animations
        self.right_anim.update(self.game.dt)
        self.up_anim.update(self.game.dt)
        self.left_anim.update(self.game.dt)
        self.down_anim.update(self.game.dt)

        
        if not self.secs:
            self.moving = False

        if self.moving:
            self.alpha += self.game.dt / self.secs
            if self.alpha > 1:
                self.alpha = 1
                self.moving = False

            self.rect.center = tuple(pg.math.lerp(self.start[i], self.target[i], self.alpha) for i in range(2))

        else:

            x, y = self.get_x_y()
            cur_node = self.graph[f'{x}-{y}']

            x, y = self.game.pacman.get_x_y()
            target_node = self.graph[f'{x}-{y}']

            self.path = self.algo.get_path(cur_node, target_node)
            self.start = self.rect.center

            if len(self.path) == 1:
                self.target = self.start
            else:
                self.target = self.path[1].rect.center
            self.secs = self.get_distance(self.start, self.target) / self.speed
            self.alpha = 0
            self.moving = True 

        self.draw()

    def get_x_y(self):
        return tuple(p // S.tile_size for p in self.rect.center)
    
    def get_pos(self, x, y):
        return (x * S.tile_size + S.tile_size / 2, y * S.tile_size + S.tile_size / 2)
    
    def get_distance(self, v1, v2):
        return sum((v1[i] - v2[i]) ** 2 for i in range(len(v1))) ** 0.5

    def draw(self):

        for i in range(0, len(self.path)-1):
            pg.draw.line(self.screen, (0, 255, 0), self.path[i].rect.center, self.path[i+1].rect.center)

        match self.cur_direction:
            case 'left':
                image = self.left_anim.get_image()
            case 'right':
                image = self.right_anim.get_image()
            case 'up':
                image = self.up_anim.get_image()
            case 'down':
                image = self.down_anim.get_image()

        self.screen.blit(image, self.rect)

