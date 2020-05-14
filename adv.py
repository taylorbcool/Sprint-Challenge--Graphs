from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
explored = {0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}}

# create opposite dict for utility purposes (immediately assigning one exit upon entering a room, turning around in dead end, etc)
opposite = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

# this makes sure we loop until all rooms are explored
while len(explored) < len(room_graph):
    # find exits that exist in current room
    if 'n' not in player.current_room.get_exits():
        explored[player.current_room.id]['n'] = None
    if 's' not in player.current_room.get_exits():
        explored[player.current_room.id]['s'] = None
    if 'w' not in player.current_room.get_exits():
        explored[player.current_room.id]['w'] = None
    if 'e' not in player.current_room.get_exits():
        explored[player.current_room.id]['e'] = None   

    # if current room has unexplored rooms
    if '?' in explored[player.current_room.id].values():
        # create list of valid directions to travel
        directions = []

        # iterate current room exits and add '?' to list directions
        for each in player.current_room.get_exits():
            # if '?' that means we haven't traveled there yet
            if explored[player.current_room.id][each] == '?':
                directions.append(each)

        # choose random direction to travel from valid exits
        direction = random.choice(directions)
        # current room becomes prev room when we leave
        prev_room = player.current_room.id
        # move to the randomly chosen room
        player.travel(direction)
        # add this new room to the old rooms entry in explored dict
        explored[prev_room][direction] = player.current_room.id

        # check to see if this room has been explored
        # if not, add the '?' to each 
        if player.current_room.id not in explored:
            explored[player.current_room.id] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}
        
        # using opposite dict, assign the last room to the opposite of the last direction traveled
        explored[player.current_room.id][opposite[direction]] = prev_room

        # finally, add the direction to traversal path
        traversal_path.append(direction)
        print(traversal_path)

    # if current room's exits have all been explored
    else:
        # pretty standard BFT code
        q = Queue()
        path = [player.current_room.id]
        q.enqueue(path)

        visited = set()

        while q.size() > 0:
            path = q.dequeue()
            current_room = path[-1]

            if current_room not in visited:
                visited.add(current_room)

            # check for unexplored exits
            if '?' in explored[current_room].values():
                # explore them
                for room in range(len(path) - 1):
                    direction = ''
                    # iterate through this room and traverse unexplored exits
                    for key, value in explored[path[room]].items():
                        if value == path[room + 1]:
                            direction = key
                    # get moving
                    player.travel(direction)
                    traversal_path.append(direction)
                    print(traversal_path)
                # not sure how else to break the loop here
                break

            else:
                # if all exits are explored this lets us move backward and find an unexplored exit
                for each in explored[current_room].values():
                    if each is not None:
                        new_path = list(path)
                        new_path.append(each)
                        q.enqueue(new_path)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
