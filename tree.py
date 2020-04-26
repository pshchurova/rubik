from cube import Cube
from random import shuffle

class TreeCube:
    def __init__(self, cube: Cube, run, allowed=["F", "R", "U", "B", "L", "D"], move=""):
        self.run = run
        self.childs = []
        self.cube = cube
        self.move = move
        self.depth = 0
        self.max_depth = 0
        self.all_allowed = allowed.copy()
        self.moves = {
            "F" : self.rotate, "R": self.rotate, "U": self.rotate, "B": self.rotate, "L": self.rotate, "D": self.rotate,
            "F'" : self.prime, "R'": self.prime, "U'": self.prime, "B'": self.prime, "L'": self.prime, "D'": self.prime,
            "F2" : self.double, "R2": self.double, "U2": self.double, "B2": self.double, "L2": self.double, "D2": self.double,
        }
        if self.move != "":
            allowed = [k for k in allowed if k[0] != self.move[0]]
            if self.move[0] == "B":
                allowed = [k for k in allowed if k[0] != "F"]
            elif self.move[0] == "D":
                allowed = [k for k in allowed if k[0] != "U"]
            elif self.move[0] == "L":
                allowed = [k for k in allowed if k[0] != "R"]
        self.allowed = allowed.copy()
        for i in allowed:
            if len(i) == 1:
                if i + "'" not in self.allowed:
                    self.allowed.append(i + "'")
                if i + "2" not in self.allowed:
                    self.allowed.append(i + "2")

    def appendChild(self, child):
        self.childs.append(child)
 
    def rotate(self, face, prime=False, double=False):
        cube = Cube()
        cube.copy(self.cube)
        if prime:
            cube.faces[face](True)
        elif double:
            cube.faces[face]()
            cube.faces[face]()
        else:
            cube.faces[face]()
        return (cube)

    def prime(self, face):
        return(self.rotate(face, prime=True))

    def double(self, face):
        return(self.rotate(face, double=True))

    def searchChilds(self, func, **kwargs):
        for move in self.allowed:
            cube = self.moves[move](move[0])
            node = TreeCube(cube, self.run, allowed=self.all_allowed, move=move)
            node.depth = self.depth + 1
            self.childs.append(node)
            if func(cube, **kwargs):
                return (move)

    def nextDepth(self, depth, func, **kwargs):
        while self.depth <= depth and self.run.is_set():
            if self.depth < depth:
                for child in self.childs:
                    m = child.nextDepth(depth, func, **kwargs)
                    if m != None:
                        return (self.move + " " + m)
            else:
                m = self.searchChilds(func, **kwargs)
                if m != None:
                    return (self.move + " " + m)
                return
            if self.depth == 0:
                depth += 1
            else:
                return

    def search(self, func, **kwargs):
        m = self.searchChilds(func, **kwargs)
        if m != None:
            return (self.move + " " + m)
        return(self.nextDepth(1, func, **kwargs))
        