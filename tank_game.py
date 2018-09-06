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
    return np.array(
        [[np.cos(angle), -np.sin(angle)],
         [np.sin(angle), np.cos(angle)]]
    )


class Tank(object):

    def __init__(self, sprite_name):
        self._config = dict(
            sprite_name=sprite_name,
            hull_center=[82, 47],
            turret_center=[46, 35],
            gun_center=[-15, 15],
            tank_center=np.array([150, 150]),
            center_delta=[0, 0],
            tank_angle=0,
            turret_angle=0,
        )
        self.moved = True
        self.tank_file = None

    @staticmethod
    def _tank_srt(angle, center1, center2):
        r = R(-angle)
        tr = np.array([center2 - (r.dot(center1))]).T
        m = np.hstack((r, tr))
        m1 = np.vstack([m, np.array([0, 0, 1])])
        m2 = np.linalg.inv(m1)
        return np.asarray(m).reshape(-1)

    def move(self, step):
        angle = self._config['tank_angle']
        x = np.cos(angle) * step
        y = np.sin(angle) * step
        self._config['center_delta'][0] += x
        self._config['center_delta'][1] += y
        self.moved = True

    def turn(self, angle_degrees):
        self._config['tank_angle'] += np.radians(angle_degrees)
        self.moved = True

    def turn_turret(self, angle_degrees):
        self._config['turret_angle'] += np.radians(angle_degrees)
        self.moved = True

    def make_tank(self):
        if not self.moved and self.tank_file:
            return self.tank_file

        tank_size = (340, 340)
        sprite_name = self._config['sprite_name']
        gun_file = Image.open(sprites_dict['{0}_gun'.format(sprite_name)])
        hull_file = Image.open(sprites_dict['{0}_hull'.format(sprite_name)])
        turret_file = Image.open(sprites_dict['{0}_turret'.format(sprite_name)])
        gun = gun_file.load()
        hull = hull_file.load()
        turret = turret_file.load()

        srt_hull = self._tank_srt(
            0,
            self._config['tank_center'],
            self._config['hull_center']
        )
        hull_file2 = hull_file.transform(
            tank_size,
            Image.AFFINE,
            srt_hull,
            resample=Image.BILINEAR)

        srt_gun = self._tank_srt(
            self._config['turret_angle'],
            self._config['tank_center'],
            self._config['gun_center']
        )
        gun_file2 = gun_file.transform(
            tank_size,
            Image.AFFINE,
            srt_gun,
            resample=Image.BILINEAR)

        srt_turret = self._tank_srt(
            self._config['turret_angle'],
            self._config['tank_center'],
            self._config['turret_center']
        )
        turret_file2 = turret_file.transform(
            tank_size,
            Image.AFFINE,
            srt_turret,
            resample=Image.BILINEAR)

        tank_file = Image.composite(gun_file2, hull_file2, gun_file2)
        self.tank_file = Image.composite(turret_file2, tank_file, turret_file2)

        self.moved = False
        return self.tank_file


class Scene(object):

    def __init__(self, terrain_file_name):
        self.scene_number = 0
        self.scene_size = (1350, 854)
        self.terrain_file = Image.open(terrain_file_name)
        self.scene_file = None

    def get_scene(self, tank):
        if self.scene_file and not tank.moved and tank.tank_file:
            return self.scene_file

        srt_tank = tank._tank_srt(
            tank._config['tank_angle'],
            np.array(self.scene_size) / 2 + np.array(tank._config['center_delta']),
            tank._config['tank_center']
        )
        tank_file = tank.make_tank()
        tank_file2 = tank_file.transform(
            self.scene_size,
            Image.AFFINE,
            srt_tank,
            resample=Image.BILINEAR)

        self.scene_file = Image.composite(tank_file2, self.terrain_file, tank_file2)
        return self.scene_file

    def show(self, tank):
        scene_file = self.get_scene(tank)
        scene_file.save(images_path + 'results/scene_{0:0>9}.png'.format(
            self.scene_number
        ))

        self.scene_number += 1


tank0 = Tank(sprite_name='tank0')
scene = Scene(textures_dict['dirt_road'])

#tank0.turn(45)
#tank0.show(textures_dict['dirt_road'])
#sys.stdout.flush()

# Stay
print('Stay...', end='')
for i in range(50):
    print('#', end='')
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Turn
print('Turn...', end='')
for i in range(90):
    print('#', end='')
    tank0.turn(0.5)
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Go
print('Go.....', end='')
for i in range(30):
    print('#', end='')
    tank0.move(i * 0.3)
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Stay
print('Stay...', end='')
for i in range(30):
    print('#', end='')
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Turn
print('Turn...', end='')
for i in range(90):
    print('#', end='')
    tank0.turn(-0.5)
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Stay
print('Stay...', end='')
for i in range(50):
    print('#', end='')
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Go
print('Go.....', end='')
for i in range(30):
    print('#', end='')
    tank0.move(i * 0.3)
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Stay
print('Stay...', end='')
for i in range(50):
    print('#', end='')
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Turn the turret
print('Turret.', end='')
for i in range(90):
    print('#', end='')
    tank0.turn_turret(1)
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Stay
print('Stay...', end='')
for i in range(50):
    print('#', end='')
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Turn
print('Turn...', end='')
for i in range(180):
    print('#', end='')
    tank0.turn(0.5)
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Stay
print('Stay...', end='')
for i in range(50):
    print('#', end='')
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Go north
print('Go.....', end='')
for i in range(20):
    print('#', end='')
    tank0.move(i * 0.3)
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Stay
print('Stay...', end='')
for i in range(50):
    print('#', end='')
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Combined move
print('Combo..', end='')
for i in range(90):
    print('#', end='')
    tank0.turn(0.5)
    tank0.turn_turret(-1)
    tank0.move(-i * 0.1)
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Stay
print('Stay...', end='')
for i in range(120):
    print('#', end='')
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Combined move
print('Combo..', end='')
for i in range(90):
    print('#', end='')
    tank0.turn(0.5)
    step = 0.1 + 0.2 * (i / 90)
    tank0.move(i * step)
    scene.show(tank0)
    sys.stdout.flush()
print('')

# Stay
print('Stay...', end='')
for i in range(50):
    print('#', end='')
    scene.show(tank0)
    sys.stdout.flush()
print('')

