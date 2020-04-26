from time import sleep
from ursina import *



class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.title = 'rubik'
        window.borderless = False
        window.fullscreen = False
        Entity(model="quad", scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5, color=color.light_gray)
        Entity(model="quad", scale=20, texture='textures/black_arrow', texture_scale=(1, 1), rotation_x=90, y=-4.99, color=color.light_gray)
        Entity(model='sphere', scale=1000, double_sided=True, texture='textures/sky0')
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.model, self.texture = 'models/custom_cube', "textures/rubik_texture"
        self.load_game()
        self.scramble = ""
        self.solver = []
        self.game_mode = "game"
        self.next = []

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model=self.model, texture=self.texture, position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'UP': 'y', 'DOWN': 'y', 'FRONT': 'z', 'BACK': 'z'}
        self.rotation_dir = {'LEFT': -1, 'RIGHT': 1, 'UP': 1, 'DOWN': -1, 'FRONT': 1, 'BACK': -1}
        self.cubes_side_positions = {'LEFT': self.LEFT, 'RIGHT': self.RIGHT, 'UP': self.UP, 'DOWN': self.DOWN, 'FRONT': self.FRONT, 'BACK': self.BACK}
        self.animation_time = 0.5
        self.action_trigger = True

    def setScramble(self, s):
        self.scramble = s.split()

    def setSolver(self, s):
        self.solver = s.split()

    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger
        if len(self.next) > 0:
            self.nextMove(self.next)
        

    def rotate_side(self, side_name, prime=1):
        self.action_trigger = False
        cube_positions = self.cubes_side_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        rotation_dir = self.rotation_dir[side_name]
        rotation_dir = rotation_dir * prime
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(f'self.PARENT.animate_rotation_{rotation_axis}(90*{rotation_dir}, duration=self.animation_time)')
        invoke(self.toggle_animation_trigger, delay=self.animation_time + 0.11)

    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0

    def create_cube_positions(self):
        self.LEFT = {Vec3(-1, y, z) for y in range (-1,2) for z in range(-1, 2)}
        self.DOWN = {Vec3(x, -1, z) for x in range (-1,2) for z in range(-1, 2)}
        self.FRONT = {Vec3(x, y, -1) for x in range (-1,2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range (-1,2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range (-1,2) for z in range(-1, 2)}
        self.UP = {Vec3(x, 1, z) for x in range (-1,2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.DOWN | self.FRONT | self.BACK | self.RIGHT |self.UP

    def nextMove(self, pattern):
        faces = dict(zip('FRUBLD', 'FRONT RIGHT UP BACK LEFT DOWN'.split()))
        if pattern == []:
            return
        move = pattern[0]
        if len(move) > 2 or not move[0] in faces or (len(move) == 2 and (move[1] != "2" and move[1] != "'")):
            print(f"{move} not existing")
            return
        else:
            if len(move) == 2:
                if move[1] == "'":
                    self.rotate_side(faces[move[0]], -1)
                elif move[1] == "2":
                    self.rotate_side(faces[move[0]], 2)
            else:
                self.rotate_side(faces[move[0]])
        self.next = pattern[1:]
        

    def input(self, key):
        if self.game_mode == "game":
            keys = dict(zip('frubld', 'FRONT RIGHT UP BACK LEFT DOWN'.split()))
            if key in keys and self.action_trigger:
                self.rotate_side(keys[key])
            if key.split("-")[0] == "shift" and len(key.split("-")) == 2 and key.split("-")[1] in keys and self.action_trigger:
                key = key.split("-")[1]
                self.rotate_side(keys[key], -1)
                
        elif self.game_mode == "solver":
            if key == 's' and len(self.next) == 0 and self.action_trigger:
                self.nextMove(self.scramble)
            if key == 'r' and len(self.next) == 0 and self.action_trigger:
                self.nextMove(self.solver)

        if key == "+":
            if self.animation_time - 0.1 >= 0:
                self.animation_time = round(self.animation_time - 0.1, 2)
            speed = Text(text=str(self.animation_time), origin=(20, -12))
            speed.appear(speed=0.025)
            speed.fade_out(duration=0.3)
        if key == "-":
            if self.animation_time + 0.1 <= 5:
                self.animation_time = round(self.animation_time + 0.1, 2)
            speed = Text(text=str(self.animation_time), origin=(20, -12))
            speed.appear(speed=0.025)
            speed.fade_out(duration=0.3)

        if key == "escape":
            quit()
        super().input(key)


if __name__ == "__main__":
    game = Game()
    game.run()