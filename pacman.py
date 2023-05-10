import pygame as pg
from animation import Animation
from settings import Settings as S

class Pacman:

    images_r = [pg.transform.scale(pg.image.load(f'images/pacman{n}.png'), (S.tile_size*1.75, S.tile_size*1.75)) for n in range(3)]
    images_u = [pg.transform.rotate(pg.transform.scale(pg.image.load(f'images/pacman{n}.png'), (S.tile_size*1.75, S.tile_size*1.75)),  90) for n in range(3)]
    images_l = [pg.transform.rotate(pg.transform.scale(pg.image.load(f'images/pacman{n}.png'), (S.tile_size*1.75, S.tile_size*1.75)), 180) for n in range(3)]
    images_d = [pg.transform.rotate(pg.transform.scale(pg.image.load(f'images/pacman{n}.png'), (S.tile_size*1.75, S.tile_size*1.75)), 270) for n in range(3)]

    def __init__(self, game):

        self.game = game
        self.screen = game.screen
        self.graph = game.graph.graph

        # Animation Attributes
        self.anim_move_r = Animation(Pacman.images_r, delay=0.1, is_loop=True)
        self.anim_move_u = Animation(Pacman.images_u, delay=0.1, is_loop=True)
        self.anim_move_l = Animation(Pacman.images_l, delay=0.1, is_loop=True)
        self.anim_move_d = Animation(Pacman.images_d, delay=0.1, is_loop=True)

        # Position Attributes
        self.rect = Pacman.images_r[0].get_rect()
        self.rect.center = self.get_pos(13, 23)


        # Movement Attributes
        self.speed = 100 # pixels per second
        self.alpha = self.secs = 0
        self.cur_direction = 'left'
        self.direction = None
        self.moving = False

    
    def update(self):

        # Update direction
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.direction = 'left'
        elif keys[pg.K_RIGHT]:
            self.direction = 'right'
        elif keys[pg.K_UP]:
            self.direction = 'up'
        elif keys[pg.K_DOWN]:
            self.direction = 'down'

        # Movement
        if not self.secs:
            self.moving = False

        if self.moving:
            
            self.alpha += self.game.dt / self.secs
            if self.alpha > 1:
                self.alpha = 1
                self.moving = False

            self.rect.center = tuple(pg.math.lerp(self.start[i], self.target[i], self.alpha) for i in range(2))

        else:
            
            self.start = self.rect.center
            x, y = self.get_x_y()

            match self.direction:
                case 'left':
                    if f'{x-1}-{y}' in self.graph:
                        self.target = self.get_pos(x-1, y)
                        self.cur_anim = self.anim_move_l
                        self.cur_direction = 'left'
                case 'right':
                    if f'{x+1}-{y}' in self.graph:
                        self.target = self.get_pos(x+1, y)
                        self.cur_anim = self.anim_move_r
                        self.cur_direction = 'right'
                case 'up':
                    if f'{x}-{y-1}' in self.graph:
                        self.target = self.get_pos(x, y-1)
                        self.cur_anim = self.anim_move_u
                        self.cur_direction = 'up'
                case 'down':
                    if f'{x}-{y+1}' in self.graph:
                        self.target = self.get_pos(x, y+1)
                        self.cur_anim = self.anim_move_d
                        self.cur_direction = 'down'

            if self.direction != self.cur_direction:
                match self.cur_direction:
                    case 'left':
                        if f'{x-1}-{y}' in self.graph:
                            self.target = self.get_pos(x-1, y)
                        else: self.target = self.start
                    case 'right':
                        if f'{x+1}-{y}' in self.graph:
                            self.target = self.get_pos(x+1, y)
                        else: self.target = self.start
                    case 'up':
                        if f'{x}-{y-1}' in self.graph:
                            self.target = self.get_pos(x, y-1)
                        else: self.target = self.start
                    case 'down':
                        if f'{x}-{y+1}' in self.graph:
                            self.target = self.get_pos(x, y+1)
                        else: self.target = self.start
    
            self.alpha = 0
            self.secs = self.get_distance(self.start, self.target) / self.speed
            self.moving = True
        
        # Update animations
        self.anim_move_r.update(self.game.dt)
        self.anim_move_u.update(self.game.dt)
        self.anim_move_l.update(self.game.dt)
        self.anim_move_d.update(self.game.dt)

        # Draw pacman
        self.draw()

    def get_x_y(self):
        return tuple(p // S.tile_size for p in self.rect.center)
    
    def get_pos(self, x, y):
        return (x * S.tile_size + S.tile_size / 2, y * S.tile_size + S.tile_size / 2)
    
    def get_distance(self, v1, v2):
        return sum((v1[i] - v2[i]) ** 2 for i in range(len(v1))) ** 0.5
    

    def draw(self):
        match self.cur_direction:
            case 'left':
                image = self.anim_move_l.get_image()
            case 'right':
                image = self.anim_move_r.get_image()
            case 'up':
                image = self.anim_move_u.get_image()
            case 'down':
                image = self.anim_move_d.get_image()

        self.screen.blit(image, self.rect)