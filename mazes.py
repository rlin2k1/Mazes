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

# ---------------------------------------------------------------------------- #
# Solve the Maze!
# ---------------------------------------------------------------------------- #
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

    #maze_size1 = r['maze_size']
    #current_location = r['current_location']
    #levels_completed1 = r['levels_completed']
    #total_levels1 = r['total_levels']
    #status1 = r['status']
    #print(solution_path)
    #print(maze)
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
        #print("BUT RETURNED FALSE")
        return False
    # print("SUCCESSFULLY PROCEEDED " + direction)
    # print("Maze Size: " + str(maze_size1))
    # print("Current Location: " + str(current_location1))
    # print("Levels Completed: " + str(levels_completed1))
    # print("Total Levels: " + str(total_levels1))
    # print("Status: " + str(status1))

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

    #maze[current_location1[1]][current_location1[0]] = 0
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

while(status != "FINISHED"):
    maze_size = r['maze_size']
    current_location1 = r['current_location']
    maze = [ [0] * maze_size[0] for _ in range(maze_size[1])]
    maze[current_location1[1]][current_location1[0]] = 1

    solve_maze(maze_url, "UP", current_location1)
    solve_maze(maze_url, "DOWN", current_location1)
    solve_maze(maze_url, "LEFT", current_location1)
    solve_maze(maze_url, "RIGHT", current_location1)

    r = requests.get(maze_url).json()
    status = r['status']
    print("Levels Completed: " + str(r['levels_completed']))
print("DONE")

# def main():
#     print(maze)
#     print("Maze Size: " + str(maze_size))
#     print("Current Location: " + str(cl))
#     print("Levels Completed: " + str(levels_completed))
#     print("Total Levels: " + str(total_levels))
#     maze[cl[1]][cl[0]] = 1
#     #Check Boundary Conditions of Current Location and Maze Size!
#     if(solve_maze(maze_url, "UP")):
#         print("FINISHED PROCEEDING UP")
#         r = requests.get(maze_url).json()
#         status = r['status']
#         current_location = r['current_location']
#         print("Current Location: " + str(current_location))
#         #continue
#     if(solve_maze(maze_url, "DOWN")):
#         print("FINISHED PROCEEDING DOWN")
#         r = requests.get(maze_url).json()
#         status = r['status']
#         #continue
#     if(solve_maze(maze_url, "LEFT")):
#         print("FINISHED PROCEEDING LEFT")
#         r = requests.get(maze_url).json()
#         status = r['status']
#         #continue
#     if(solve_maze(maze_url, "RIGHT")):
#         print("FINISHED PROCEEDING RIGHT")
#         r = requests.get(maze_url).json()
#         status = r['status']
#         #continue
#     #solution_path.clear()
#     r = requests.get(maze_url).json()
#     status = r['status']
#     print("Status: " + str(status))
#     print("---------------------------------------------------------------")
#     # direction_json = {
#     #     "action":"DOWN"
#     # }
#     # r = requests.post(maze_url, direction_json).json()
#     # print(r['result'])
#     # r = requests.get(maze_url).json()
#     # maze_size = r['maze_size']
#     # current_location = r['current_location']
#     # levels_completed = r['levels_completed']
#     # total_levels = r['total_levels']
#     # print("Maze Size: " + str(maze_size))
#     # print("Current Location: " + str(current_location))
#     # print("Levels Completed: " + str(levels_completed))
#     # print("Total Levels: " + str(total_levels))
#     return 0

# if __name__ == "__main__":
#     main()