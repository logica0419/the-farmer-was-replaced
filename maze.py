from __builtins__ import (
    East,
    Entities,
    Items,
    North,
    South,
    Unlocks,
    West,
    can_move,
    clear,
    get_entity_type,
    get_pos_x,
    get_pos_y,
    harvest,
    measure,
    move,
    num_drones,
    num_items,
    num_unlocked,
    plant,
    spawn_drone,
    use_item,
    wait_for,
)

north = 2
east = 3
south = 5
west = 7

directions = []
directions.append((north, North, South, 0, 1))
directions.append((east, East, West, 1, 0))
directions.append((south, South, North, 0, -1))
directions.append((west, West, East, -1, 0))

substance = 5 * 2 ** (num_unlocked(Unlocks.Mazes) - 1)


def init_search(maze, current_x, current_y, came_from):
    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)

    for dir in directions:
        if not can_move(dir[1]):
            continue

        maze[current_x][current_y] *= dir[0]

        if dir[1] == came_from:
            continue

        move(dir[1])
        init_search(maze, current_x + dir[3], current_y + dir[4], dir[2])
        move(dir[2])


def update_cell(maze, current_x, current_y):
    maze[current_x][current_y] = 1
    for dir in directions:
        if can_move(dir[1]):
            maze[current_x][current_y] *= dir[0]


def find_route(maze, current, treasure):
    visited = {treasure}
    routes = [[]]
    queue = [(treasure, 0, None)]

    while len(queue) > 0:
        pos, route_num, came_from = queue.pop(0)

        if pos == current:
            return routes[route_num]

        for dir in directions:
            if dir[1] == came_from or maze[pos[0]][pos[1]] % dir[0] != 0:
                continue

            new_pos = (pos[0] + dir[3], pos[1] + dir[4])
            if new_pos in visited:
                continue
            visited.add(new_pos)

            new_route_num = len(routes)
            routes.append(routes[route_num][:])
            routes[new_route_num].append(dir[2])

            queue.append((new_pos, new_route_num, dir[2]))

    return routes[0]


def search(base_pos_x, base_pos_y):
    maze = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ]

    current_x, current_y = 2, 2
    init_search(maze, current_x, current_y, None)

    while True:
        treasure = measure()

        route = find_route(
            maze,
            (current_x, current_y),
            (treasure[0] - base_pos_x, treasure[1] - base_pos_y),
        )
        for _ in range(len(route)):
            move(route.pop())
            update_cell(maze, get_pos_x() - base_pos_x, get_pos_y() - base_pos_y)

        if get_entity_type() != Entities.Treasure or not use_item(
            Items.Weird_Substance, substance
        ):
            harvest()
            break

        current_x, current_y = get_pos_x() - base_pos_x, get_pos_y() - base_pos_y

        if num_items(Items.Power) < 1000:
            break


def solve_maze():
    while num_drones() < 16:
        pass
    while get_pos_x() != 0 and can_move(West):
        pass
    while get_pos_y() != 0 and can_move(South):
        pass

    for _ in range(2):
        move(East)
        move(North)

    init_pos_x = get_pos_x()
    init_pos_y = get_pos_y()

    while True:
        while get_pos_x() != init_pos_x or get_pos_y() != init_pos_y:
            if init_pos_x > get_pos_x():
                move(East)
            elif init_pos_x < get_pos_x():
                move(West)

            if init_pos_y > get_pos_y():
                move(North)
            elif init_pos_y < get_pos_y():
                move(South)

        plant(Entities.Bush)
        use_item(Items.Weird_Substance, substance)

        search(init_pos_x - 2, init_pos_y - 2)

        if num_items(Items.Power) < 1000:
            break


def main():
    clear()

    drones = []

    for i in range(6):
        for j in range(6):
            if i != 0 or j != 0:
                drones.append(spawn_drone(solve_maze))

            for _ in range(5):
                move(East)

        for _ in range(5):
            move(North)
        move(East)
        move(East)

    move(North)
    move(North)

    solve_maze()

    for drone in drones:
        if drone:
            wait_for(drone)


main()
