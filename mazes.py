""" mazes.py
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

def solve_maze_levels():
    direction_dict = {"RIGHT": "LEFT", "LEFT": "RIGHT", "UP": "DOWN", "DOWN": "UP"}
    # ---------------------------------------------------------------------------- #
    # Obtain the Access Token for the Rest of the Simulation
    # ---------------------------------------------------------------------------- #
    student_uid = {
        "uid":"704767891"
    }
    token_url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session"
    r = requests.post(token_url, student_uid).json()
    access_token = r['token']
    print("ACCESS TOKEN: " + access_token)

    maze_url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=" + access_token
    r = requests.get(maze_url).json()
    status = r['status']
    maze = [[]]
    current_location1 = [0, 0]

    def solve_maze(url, direction, h):
        direction_json = {
            "action":direction
        }
        r = requests.post(url, direction_json).json()
        #print(r['result'])
        if(r['result'] == 'END'):
            return True
        elif(r['result'] == 'OUT_OF_BOUNDS' or r['result'] == 'WALL'):
            return False
        
        current_location1 = h
        if(direction == "UP"):
            current_location1[1] = current_location1[1] - 1
        elif(direction == "DOWN"):
            current_location1[1] = current_location1[1] + 1
        elif(direction == "LEFT"):
            current_location1[0] = current_location1[0] - 1
        elif(direction == "RIGHT"):
            current_location1[0] = current_location1[0] + 1
            
        if(maze[current_location1[1]][current_location1[0]] == 1):
            #Go Back One
            new_direction = direction_dict[direction]
            direction_json = {
                "action":new_direction
            }
            r = requests.post(url, direction_json).json()
            if(new_direction == "UP"):
                current_location1[1] = current_location1[1] - 1
            elif(new_direction == "DOWN"):
                current_location1[1] = current_location1[1] + 1
            elif(new_direction == "LEFT"):
                current_location1[0] = current_location1[0] - 1
            elif(new_direction == "RIGHT"):
                current_location1[0] = current_location1[0] + 1
            return False

        maze[current_location1[1]][current_location1[0]] = 1
        if(current_location1[1] - 1 >= 0 and maze[current_location1[1] - 1][current_location1[0]] != 'X' and maze[current_location1[1] - 1][current_location1[0]] != 1):
            if(solve_maze(url, "UP", current_location1)):
                return True
            else:
                maze[current_location1[1] - 1][current_location1[0]] = 'X'
        if(current_location1[1] + 1 < maze_size[1] and maze[current_location1[1] + 1][current_location1[0]] != 'X' and maze[current_location1[1] + 1][current_location1[0]] != 1):
            if(solve_maze(url, "DOWN", current_location1)):
                return True
            else:
                maze[current_location1[1] + 1][current_location1[0]] = 'X'
        if(current_location1[0] - 1 >= 0 and maze[current_location1[1]][current_location1[0] - 1] != 'X' and maze[current_location1[1]][current_location1[0] - 1] != 1):
            if(solve_maze(url, "LEFT", current_location1)):
                return True
            else:
                maze[current_location1[1]][current_location1[0] - 1] = 'X'
        if(current_location1[0] + 1 < maze_size[0] and maze[current_location1[1]][current_location1[0] + 1] != 'X' and maze[current_location1[1]][current_location1[0] + 1] != 1):
            if(solve_maze(url, "RIGHT", current_location1)):
                return True
            else:
                maze[current_location1[1]][current_location1[0] + 1] != 'X'

        #Go Back One
        new_direction = direction_dict[direction]
        direction_json = {
            "action":new_direction
        }
        r = requests.post(url, direction_json)
        if(new_direction == "UP"):
            current_location1[1] = current_location1[1] - 1
        elif(new_direction == "DOWN"):
            current_location1[1] = current_location1[1] + 1
        elif(new_direction == "LEFT"):
            current_location1[0] = current_location1[0] - 1
        elif(new_direction == "RIGHT"):
            current_location1[0] = current_location1[0] + 1
        return False
    # ------------------------------------------------------------------------ #
    # Solve the Maze!
    # ------------------------------------------------------------------------ #
    while(status != "FINISHED"):
        maze_size = r['maze_size']
        current_location1 = r['current_location']
        maze = [ [0] * maze_size[0] for _ in range(maze_size[1])]
        maze[current_location1[1]][current_location1[0]] = 1

        if(not solve_maze(maze_url, "UP", current_location1)):
            if(not solve_maze(maze_url, "DOWN", current_location1)):
                if(not solve_maze(maze_url, "LEFT", current_location1)):
                    solve_maze(maze_url, "RIGHT", current_location1)

        r = requests.get(maze_url).json()
        status = r['status']
        print("Levels Completed: " + str(r['levels_completed']))
    print("DONE")

if __name__ == "__main__":
    solve_maze_levels()