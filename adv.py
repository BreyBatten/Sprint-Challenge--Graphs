from room import Room
from player import Player
from world import World

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

# Implement a BFS, which will require a Queue
# Queue keeps track of enqueue a value, a dequeue, and size of the queue
class Queue:
    def __init__(self):
        self.storage = []

    def enqueue(self, value):
        self.storage.append(value)

    def dequeue(self):
        return self.storage.pop(0)

    def size(self):
        return len(self.storage)

# AMA pseudo code:
# DFT
## Explore the graph in some direction
## As we go, log our directions in our traversal path
# BFS
## When we hit a dead end, find the nearest unvisited room: nearest question mark
## As we go to the nearest unexplored exit, log our path again

## Repeat until all rooms are visited
#(explore with DFT, backtrack with BFS)

# How do we:
## when you move into a room, update the previous room
## Exiting DFT and running BFS
## Stop BFS and run DFT
## Convert BFS path into directions for your traversal_path

# Loop DFT and BFS
# Run a DFT to go all the way down a path
# Then run BFS from end of path until you get to room with unexplored exit
# Re-run DFT

# create a class
class AdvGraph:
    def __init__(self):
        self.rooms = {}
        self.player = Player(world.starting_room)
        self.last_room = self.player.current_room.id
        self.travel_map(None, True)

    def travel_map(self, current_direction, first_room=False):
        self.last_room = self.player.current_room.id

        if not first_room:
            self.player.travel(current_direction)
            traversal_path.append(current_direction)

        room_id = self.player.current_room.id

        if room_id not in self.rooms:
            directions = self.player.current_room.get_exits()
            self.rooms[room_id] = {}
            for direction in directions:
                self.rooms[room_id][direction] = '?'

        if current_direction is not None:
            if current_direction == 'n':
                self.rooms[room_id]['s'] = self.last_room
            elif current_direction == 's':
                self.rooms[room_id]['n'] = self.last_room
            elif current_direction == 'e':
                self.rooms[room_id]['w'] = self.last_room
            elif current_direction == 'w':
                self.rooms[room_id]['e'] = self.last_room
            self.rooms[self.last_room][current_direction] = room_id         

    # need to keep track of paths we haven't gone down yet
    def unexplored_paths(self):
        current_room = self.rooms[self.player.current_room.id]
        unexplored_directions = []

        for direction in current_room:
            if current_room[direction] == '?':
                unexplored_directions.append(direction)
        return unexplored_directions

    # we have to explore the unexplored paths we are keeping track of above
    def explore(self):
        current_unexplored = self.unexplored_paths()

        while(len(current_unexplored) > 0):
            random_direction = current_unexplored[random.randint(0, len(current_unexplored) - 1)]
            self.travel_map(random_direction)
            current_unexplored = self.unexplored_paths()

    # we need to implement our BFS and backtrack out of dead-ends
    def backtrack(self):
        q = Queue()
        q.enqueue([(self.player.current_room.id, None)])
        visited = set()

        while q.size() > 0:
            current_path = q.dequeue()
            current_vector = current_path[-1]
            current_room = current_vector[0]

            visited.add(current_room)

            for direction in self.rooms[current_room]:
                next_location = self.rooms[current_room][direction]
                if next_location == '?':
                    for vector in current_path:
                        if vector[1] != None:
                            self.player.travel(vector[1])
                            traversal_path.append(vector[1])
                    return
            
                if next_location not in visited:
                    path_copy = current_path[:]
                    path_copy.append((next_location, direction))
                    q.enqueue(path_copy)

    def find_all_rooms(self):
        while True:
            self.explore()

            if len(self.rooms) == len(room_graph):
                return
            self.backtrack()

adv_graph = AdvGraph()
adv_graph.find_all_rooms()

# TRAVERSAL TEST
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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
