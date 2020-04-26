from cube import Cube
from solver import solver
from rubik3D import Game
import time
import sys

def main():
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
    else:
        print("Please enter a scramble pattern")
        return
    cube = Cube()
    print(f'inpput: {pattern}')
    cube.scramble(pattern)
    start = time.time()
    solved = solver(cube)
    print(solved)
    print(f"len: {len(solved.split(' '))}")
    end = time.time()
    print(f"Time elapsed: {end - start}")

    graph = input("Do you want to display 3D render ? y/n\n")
    if graph == "y":
        game = Game()
        game.setScramble(pattern)
        game.setSolver(solved)
        game.game_mode = "solver"
        game.run()
    return

if __name__ == "__main__":
    main()