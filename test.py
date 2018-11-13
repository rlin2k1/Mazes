""" test.py
Solving Levels of Mazes with HTTP: POST and GET Requests

Author(s):
    Roy Lin

Date Created:
    November 11th, 2018
"""
# ---------------------------------------------------------------------------- #
# Import Statements for the Necessary Packages / Modules
# ---------------------------------------------------------------------------- #
import requests #Send HTTP/1.1 Requests
import json #For JSON Parsing

solution_path = set()
direction_dict = {"RIGHT": "LEFT", "LEFT": "RIGHT", "UP": "DOWN", "DOWN": "UP"}

current_location = [0, 0]
length = 9

def solve_maze(maze, direction):
    print(current_location)
    result = ""
    if(direction == "UP"):
        current_location[0] = current_location[0] - 1
        if(current_location[0] < 0):
            result = "OUT_OF_BOUNDS"
            current_location[0] = current_location[0] + 1
        elif(maze[current_location[0]][current_location[1]] == 'W'):
            result = "WALL"
            current_location[0] = current_location[0] + 1
        else:
            result = "SUCCESS"
    elif(direction == "DOWN"):
        current_location[0] = current_location[0] + 1
        if(current_location[0] >= length):
            result = "OUT_OF_BOUNDS"
            current_location[0] = current_location[0] - 1
        elif(maze[current_location[0]][current_location[1]] == 'W'):
            result = "WALL"
            current_location[0] = current_location[0] - 1
        else:
            result = "SUCCESS"
    elif(direction == "LEFT"):
        current_location[1] = current_location[1] - 1
        if(current_location[1] < 0):
            result = "OUT_OF_BOUNDS"
            current_location[1] = current_location[1] + 1
        elif(maze[current_location[0]][current_location[1]] == 'W'):
            result = "WALL"
            current_location[1] = current_location[1] + 1
        else:
            result = "SUCCESS"
    elif(direction == "RIGHT"):
        current_location[1] = current_location[1] + 1
        if(current_location[1] >= length):
            result = "OUT_OF_BOUNDS"
            current_location[1] = current_location[1] - 1
        elif(maze[current_location[0]][current_location[1]] == 'W'):
            result = "WALL"
            current_location[1] = current_location[1] - 1
        else:
            result = "SUCCESS"
    print(current_location)
    if(maze[current_location[0]][current_location[1]] == 1):
        result = 'END'

    print(result)

    if(result == 'END'):
        return True
    elif(result == 'OUT_OF_BOUNDS' or result == 'WALL'):
        return False
    print(solution_path)
    if(tuple(current_location) in solution_path):
        direction = direction_dict[direction]
        if(direction == "UP"):
            current_location[0] = current_location[0] + 1
        if(direction == "DOWN"):
            current_location[0] = current_location[0] - 1
        if(direction == "LEFT"):
            current_location[1] = current_location[1] - 1
        if(direction == "RIGHT"):
            current_location[1] = current_location[1] + 1
        print("BUT RETURNED FALSE")
        return False
    current_loc = current_location
    solution_path.add(tuple(current_loc))
    print("CURRENT LOC: " + str(current_loc))
    if(solve_maze(maze, "UP") or solve_maze(maze, "DOWN") or solve_maze(maze, "LEFT") or solve_maze(maze, "RIGHT")):
        return True
    print("SOLUTION PATH BEFORE REMOVAL: " + str(solution_path))
    solution_path.remove(tuple(current_loc))
    return False

def main():
    #maze = [[0, 0, 1]]
    maze = [
    [0, "W", "W", 0, 0, "W", 0, 0, 0],
    [0, 0, "W", 0, "W", 0, 0, "W", 0], 
    [0, "W", "W", 0, "W", "W", 0, "W", 0],
    [0, 0, 0, 0, 0, "W", 1, "W", 0],
    [0, "W", "W", "W", 0, "W", "W", "W", 0],
    ["W", 0, 0, 0, 0, 0, 0, "W", 0],
    [0,  0, "W", "W", "W", "W", 0, "W", 0],
    [0, "W", 0, 0, 0, "W", "W", "W", 0],
    [0, 0, 0, "W", 0, 0, 0, 0, 0],
    ]
    start = current_location
    solution_path.add(tuple(start))
    #Check Boundary Conditions of Current Location and Maze Size!
    if(solve_maze(maze, "UP")):
        print("FINISHED PROCEEDING UP")
    if(solve_maze(maze, "DOWN")):
        print("FINISHED PROCEEDING DOWN")
    if(solve_maze(maze, "LEFT")):
        print("FINISHED PROCEEDING LEFT")
    if(solve_maze(maze, "RIGHT")):
        print("FINISHED PROCEEDING RIGHT")
    print("---------------------------------------------------------------")
    return 0

if __name__ == "__main__":
    main()