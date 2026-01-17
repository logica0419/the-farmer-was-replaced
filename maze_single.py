from __builtins__ import (
    East,
    Entities,
    Items,
    North,
    South,
    West,
    can_move,
    get_entity_type,
    get_pos_x,
    get_pos_y,
    harvest,
    measure,
    move,
    plant,
    use_item,
)

north = 2
east = 3
south = 5
west = 7

directions = [
    (north, North, South, 0, 1),
    (east, East, West, 1, 0),
    (south, South, North, 0, -1),
    (west, West, East, -1, 0),
]

size = 8
substance = 256


def init_search(maze, visited, current, came_from, reset_limit):
    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)
        reset_limit -= 1

    current_x, current_y = current[0], current[1]

    for dir in directions:
        if not can_move(dir[1]):
            continue

        maze[current_x][current_y] *= dir[0]

        if dir[1] == came_from:
            continue

        new_pos = (current_x + dir[3], current_y + dir[4])
        if new_pos in visited:
            continue
        visited.add(new_pos)

        move(dir[1])
        reset_limit = init_search(maze, visited, new_pos, dir[2], reset_limit)
        move(dir[2])

    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)
        reset_limit -= 1

    return reset_limit


def update_cell(maze, current_x, current_y):
    ref = 1
    for dir in directions:
        if can_move(dir[1]):
            ref *= dir[0]
    maze[current_x][current_y] = ref


def bfs(maze, current_x, current_y, treasure):
    current = (current_x, current_y)
    if current == treasure:
        return []

    treasure_visited = {treasure: 0}
    treasure_routes = [[]]
    treasure_queue = [(treasure, 0, None)]

    current_visited = {current: 0}
    current_routes = [[]]
    current_queue = [(current, 0, None)]

    while True:
        pos, route_num, came_from = treasure_queue.pop(0)
        pos_x, pos_y = pos[0], pos[1]
        cell = maze[pos_x][pos_y]
        route = treasure_routes[route_num]

        for dir in directions:
            if dir[1] == came_from or cell % dir[0] != 0:
                continue

            new_pos = (pos_x + dir[3], pos[1] + dir[4])
            if new_pos in treasure_visited:
                continue

            new_route_num = len(treasure_routes)
            treasure_routes.append(route[:])
            treasure_routes[new_route_num].append(dir[2])

            treasure_visited[new_pos] = new_route_num

            treasure_queue.append((new_pos, new_route_num, dir[2]))

        # ------------------------------------------------------

        pos, route_num, came_from = current_queue.pop(0)
        pos_x, pos_y = pos[0], pos[1]
        cell = maze[pos_x][pos_y]
        route = current_routes[route_num]

        for dir in directions:
            if dir[1] == came_from or cell % dir[0] != 0:
                continue

            new_pos = (pos_x + dir[3], pos[1] + dir[4])
            if new_pos in current_visited:
                continue

            if new_pos in treasure_visited:
                route.append(dir[1])
                treasure_route = treasure_routes[treasure_visited[new_pos]]
                for _ in range(len(treasure_route)):
                    route.append(treasure_route.pop())
                return route

            new_route_num = len(current_routes)

            current_routes.append(route[:])
            current_routes[new_route_num].append(dir[1])

            current_visited[new_pos] = new_route_num

            current_queue.append((new_pos, new_route_num, dir[2]))


def a_star(maze, current_x, current_y, treasure):
    current = (current_x, current_y)
    treasure_x, treasure_y = treasure[0], treasure[1]

    cost = abs(treasure_x - current_x) + abs(treasure_y - current_y)

    treasure_visited = {treasure: 0}
    treasure_routes = [[]]
    treasure_queue = [(treasure, 0, None, 0, cost)]

    current_visited = {current: 0}
    current_routes = [[]]
    current_queue = [(current, 0, None, 0, cost)]

    while True:
        pos, route_num, came_from, cost, _ = treasure_queue.pop(0)
        pos_x, pos_y = pos[0], pos[1]
        cell = maze[pos_x][pos_y]
        route = treasure_routes[route_num]

        for dir in directions:
            if dir[1] == came_from or cell % dir[0] != 0:
                continue

            new_pos_x = pos_x + dir[3]
            new_pos_y = pos_y + dir[4]
            new_pos = (new_pos_x, new_pos_y)
            if new_pos in treasure_visited:
                continue

            new_cost = cost + 1
            new_total_cost = (
                new_cost + abs(current_x - new_pos_x) + abs(current_y - new_pos_y)
            )

            new_route_num = len(treasure_routes)
            treasure_routes.append(route[:])
            treasure_routes[new_route_num].append(dir[2])

            treasure_visited[new_pos] = new_route_num

            inserted = False
            for i in range(len(treasure_queue)):
                if treasure_queue[i][4] >= new_total_cost:
                    treasure_queue.insert(
                        i, (new_pos, new_route_num, dir[2], new_cost, new_total_cost)
                    )
                    inserted = True
                    break
            if not inserted:
                treasure_queue.append(
                    (new_pos, new_route_num, dir[2], new_cost, new_total_cost)
                )

        # ------------------------------------------------------

        pos, route_num, came_from, cost, _ = current_queue.pop(0)
        pos_x, pos_y = pos[0], pos[1]
        cell = maze[pos_x][pos_y]
        route = current_routes[route_num]

        for dir in directions:
            if dir[1] == came_from or cell % dir[0] != 0:
                continue

            new_pos_x = pos_x + dir[3]
            new_pos_y = pos_y + dir[4]
            new_pos = (new_pos_x, new_pos_y)
            if new_pos in current_visited:
                continue

            if new_pos in treasure_visited:
                route = route
                route.append(dir[1])
                treasure_route = treasure_routes[treasure_visited[new_pos]]
                for _ in range(len(treasure_route)):
                    route.append(treasure_route.pop())
                return route

            new_cost = cost + 1
            new_total_cost = (
                new_cost + abs(treasure_x - new_pos_x) + abs(treasure_y - new_pos_y)
            )

            new_route_num = len(current_routes)

            current_routes.append(route[:])
            current_routes[new_route_num].append(dir[1])

            current_visited[new_pos] = new_route_num

            inserted = False
            for i in range(len(current_queue)):
                if current_queue[i][4] >= new_total_cost:
                    current_queue.insert(
                        i, (new_pos, new_route_num, dir[2], new_cost, new_total_cost)
                    )
                    inserted = True
                    break
            if not inserted:
                current_queue.append(
                    (new_pos, new_route_num, dir[2], new_cost, new_total_cost)
                )


def search():
    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]

    current_x, current_y = 0, 0
    reset_limit = init_search(
        maze, {(current_x, current_y)}, (current_x, current_y), None, 140
    )

    for _ in range(160):
        route = bfs(
            maze,
            current_x,
            current_y,
            measure(),
        )
        for dir in route:
            move(dir)
            current_x, current_y = get_pos_x(), get_pos_y()
            update_cell(maze, current_x, current_y)

        use_item(Items.Weird_Substance, substance)

    for _ in range(reset_limit):
        route = a_star(
            maze,
            current_x,
            current_y,
            measure(),
        )
        for dir in route:
            move(dir)
            current_x, current_y = get_pos_x(), get_pos_y()
            update_cell(maze, current_x, current_y)

        use_item(Items.Weird_Substance, substance)

    route = a_star(
        maze,
        current_x,
        current_y,
        measure(),
    )
    for dir in route:
        move(dir)
    harvest()


def run():
    plant(Entities.Bush)
    use_item(Items.Weird_Substance, substance)

    search()


run()
