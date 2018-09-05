import sys
import numpy as np
from PIL import Image


images_path = '/Users/dmytrobudashnyi/usr/projects/linear_algebra/'
textures_dict = {
    'dirt_road': images_path + 'textures/16_dirt_road_texture.jpg'
}
sprites_dict = {
    'tank0_gun': images_path + 'sprites/tank_amazon_green/Amazon Green Gun.png',
    'tank0_hull': images_path + 'sprites/tank_amazon_green/Amazon Green Hull.png',
    'tank0_turret': images_path + 'sprites/tank_amazon_green/Amazon Green Turret.png',
}

def R(angle):
    return np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

def tank_rt(angle, center1, center2):
    r = R(-angle)
    tr = np.array([center2 - (r.dot(center1))]).T
    m = np.hstack((r, tr))
    m1 = np.vstack([m, np.array([0, 0, 1])])
    m2 = np.linalg.inv(m1)
    #print(m2)
    return m2

class Tank(object):

    def __init__(self, sprite_name):
        self.scene_number = 0
        self._config = dict(
            sprite_name=sprite_name,
            hull_center=[82, 47],
            turret_center=[36, 35],
            gun_center=[-25, 15],
            center_delta=np.array([0, 0]),
            tank_angle=0,
            turret_angle=0,
        )

    def move(self, step):
        angle = self._config['tank_angle']
        x = np.cos(angle) * step
        y = np.sin(angle) * step
        #print('XY = ', x, y)
        self._config['center_delta'][0] += x
        self._config['center_delta'][1] += y

    def turn(self, angle_degrees):
        self._config['tank_angle'] += np.radians(angle_degrees)

    def turn_turret(self, angle_degrees):
        self._config['turret_angle'] += np.radians(angle_degrees)

    def show(self, terrain_file_name):
        terrain_file = Image.open(terrain_file_name)
        terrain = terrain_file.load()

        sprite_name = self._config['sprite_name']
        gun_file = Image.open(sprites_dict['{0}_gun'.format(sprite_name)])
        hull_file = Image.open(sprites_dict['{0}_hull'.format(sprite_name)])
        turret_file = Image.open(sprites_dict['{0}_turret'.format(sprite_name)])
        gun = gun_file.load()
        hull = hull_file.load()
        turret = turret_file.load()

        dshape = terrain_file.size

        terrain_center = np.array([int(dshape[0] / 2), int(dshape[1] / 2)])
        rt_hull = tank_rt(
            self._config['tank_angle'],
            terrain_center - self._config['center_delta'],
            self._config['hull_center']
        )
        W, H = hull_file.size
        for x2 in range(W):
            for y2 in range(H):
                x1, y1, _ = map(int, rt_hull.dot(np.array([x2, y2, 1])))
                if x1 > 0 and x1 < dshape[0] and y1 > 0 and y1 < dshape[1]:
                    (r1, g1, b1) = terrain[x1, y1]
                    (r2, g2, b2, a) = hull[x2, y2]
                    coef = a / 255
                    val = (
                        int(r2 * coef + r1 * (1 - coef)),
                        int(g2 * coef + g1 * (1 - coef)),
                        int(b2 * coef + b1 * (1 - coef)),
                    )
                    terrain[x1, y1] = val

        rt_gun = tank_rt(
            self._config['tank_angle'] + self._config['turret_angle'],
            terrain_center - self._config['center_delta'],
            self._config['gun_center']
        )
        W, H = gun_file.size
        for x2 in range(W):
            for y2 in range(H):
                x1, y1, _ = map(int, rt_gun.dot(np.array([x2, y2, 1])))
                if x1 > 0 and x1 < dshape[0] and y1 > 0 and y1 < dshape[1]:
                    (r1, g1, b1,) = terrain[x1, y1]
                    (r2, g2, b2, a) = gun[x2, y2]
                    coef = a / 255
                    val = (
                        int(r2 * coef + r1 * (1 - coef)),
                        int(g2 * coef + g1 * (1 - coef)),
                        int(b2 * coef + b1 * (1 - coef)),
                    )
                    terrain[x1, y1] = val

        rt_turret = tank_rt(
            self._config['tank_angle'] + self._config['turret_angle'],
            terrain_center - self._config['center_delta'],
            self._config['turret_center']
        )
        W, H = turret_file.size
        for x2 in range(W):
            for y2 in range(H):
                x1, y1, _ = map(int, rt_turret.dot(np.array([x2, y2, 1])))
                if x1 > 0 and x1 < dshape[0] and y1 > 0 and y1 < dshape[1]:
                    (r1, g1, b1) = terrain[x1, y1]
                    (r2, g2, b2, a) = turret[x2, y2]
                    coef = a / 255
                    val = (
                        int(r2 * coef + r1 * (1 - coef)),
                        int(g2 * coef + g1 * (1 - coef)),
                        int(b2 * coef + b1 * (1 - coef)),
                    )
                    terrain[x1, y1] = val
        terrain_file.save(images_path + 'results/scene_{0:0>9}.png'.format(
            self.scene_number
        ))
        self.scene_number += 1
        

tank0 = Tank(sprite_name='tank0')

# Stay
for i in range(10):
    print('#', end='')
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Turn
for i in range(90):
    print('#', end='')
    tank0.turn(0.5)
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Go
for i in range(30):
    print('#', end='')
    tank0.move(-i * 0.3)
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Stay
for i in range(10):
    print('#', end='')
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Turn
for i in range(90):
    print('#', end='')
    tank0.turn(-0.5)
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Stay
for i in range(30):
    print('#', end='')
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Go
for i in range(30):
    print('#', end='')
    tank0.move(-i * 0.3)
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Stay
for i in range(30):
    print('#', end='')
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Turn the turret
for i in range(90):
    print('#', end='')
    tank0.turn_turret(1)
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Stay
for i in range(30):
    print('#', end='')
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Turn
for i in range(180):
    print('#', end='')
    tank0.turn(0.5)
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Stay
for i in range(30):
    print('#', end='')
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Go north
for i in range(20):
    print('#', end='')
    tank0.move(-i * 0.3)
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()

# Stay
for i in range(90):
    print('#', end='')
    tank0.show(textures_dict['dirt_road'])
    sys.stdout.flush()


