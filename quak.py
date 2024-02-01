from __future__ import annotations
import keyboard
from math import sin, cos, sqrt, pow, pi
from numpy import array, true_divide
import time
import functools
from Singleton import Singleton
from cursor import move_cursor, addstr
from Header import *


class Raycast:
    raycast_step = 0.2
    max_dist = 20

    @staticmethod
    def raycast(origin, direction, max_dist, mask=None):
        dist = 0
        walls = Game().terrain.walls
        xpstep = sin(direction) * Raycast.raycast_step
        ypstep = cos(direction) * Raycast.raycast_step
        p = [origin[0], origin[1]]
        while dist < max_dist:
            p[0] += xpstep
            p[1] += ypstep
            for wall in walls:
                if wall.contains(*p):
                    return wall, dist
            dist += Raycast.raycast_step
        return None, None


class Display:
    width = 100
    height = 20


class Camera():
    POV = 0.7*pi

    def __init__(self, anchor) -> None:
        self.anchor = anchor

    def render(self):
        pixel_angle = self.POV/Display.width
        move_cursor(0, 0)
        dd = {}

        direction = self.anchor.rot - self.POV/2
        for x in range(Display.width):
            direction += pixel_angle
            origin = self.anchor.pos
            dd[x] = Raycast.raycast(origin, direction, Game.fog_dist)

        for y in range(Display.height):
            texture_row = ''
            for x in range(Display.width):
                center_offset = abs(Display.height/2 - y)
                target = dd[x]
                if target[0] and target[1]:
                    dist = target[1]
                    n_ceiling = Display.height/max(dist, 0.01)
                    if center_offset < n_ceiling:
                        texture_row += target[0].get_texture(dist)
                    else:
                        texture_row += self.get_floor(center_offset, y)
                else:
                    texture_row += self.get_floor(center_offset, y)
            addstr(texture_row)

    @functools.cache
    def get_floor(self, offset, y):
        if y <= Display.height/2:
            return ' '
        if offset < 1/3*Display.height/2:
            return '.'
        elif offset < 2/3*Display.height/2:
            return 'x'
        return '#'


class Player:
    SPAWN_POINT = float(2), float(2)
    ROT_SPEED = 1*pi
    PLAYER_SPEED = 2

    def __init__(self) -> None:
        self.pos = array(self.SPAWN_POINT)
        self.rot = 0

    def update(self):
        if keyboard.is_pressed('a'):
            self.rot -= self.ROT_SPEED*Game.delta_time
        if keyboard.is_pressed('d'):
            self.rot += self.ROT_SPEED*Game.delta_time
        if keyboard.is_pressed('w'):
            dx, dy = sin(self.rot), cos(self.rot)
            self.pos += self.PLAYER_SPEED * array([dx, dy]) * Game.delta_time
        if keyboard.is_pressed('s'):
            dx, dy = sin(self.rot), cos(self.rot)
            self.pos -= self.PLAYER_SPEED * array([dx, dy]) * Game.delta_time
        return self


class Wall:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def contains(self, x, y):
        difx, difpy = x-self.x, y-self.y
        return -Game.UNIT < difx and difx < Game.UNIT and -Game.UNIT < difpy and difpy < Game.UNIT

    @staticmethod
    @functools.cache
    def get_texture(dist):
        if dist < 1/5*Game.fog_dist:
            return chr(9619)
        elif dist < 2/5*Game.fog_dist:
            return chr(9618)
        elif dist < Game.fog_dist:
            return chr(9617)
        else:
            return ' '


class Game(metaclass=Singleton):
    delta_time = 1/30
    fog_dist = 20
    UNIT = 1

    def __init__(self) -> None:
        from os import system
        system('cls')
        system(f'MODE {Display.width},{Display.height}')
        self.terrain = Terrain()
        self.player = Player()
        self.camera = Camera(anchor=self.player)

    def game_loop(self):
        while True:
            start = time.time()
            self.player.update()
            self.camera.render()
            elapsed = time.time() - start
            move_cursor(0, 0)
            addstr(f'FPS: {1/(elapsed+0.00001):.2f}')


class Terrain:
    SIZE = WIDTH, DEPTH, HEIGHT = 100, 100, 2  # x, y, z
    UNIT = 10

    terrain = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

    ]

    def __init__(self) -> None:
        rows = len(self.terrain)
        cols = len(self.terrain[0])
        self.walls = [
            Wall(x, y) for y in range(rows) for x in range(cols) if self.terrain[y][x]
        ]


if __name__ == '__main__':
    Game().game_loop()
