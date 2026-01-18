from __builtins__ import (
    East,
    Entities,
    Items,
    North,
    South,
    West,
    abs,
    can_move,
    get_entity_type,
    get_pos_x,
    get_pos_y,
    harvest,
    len,
    measure,
    move,
    plant,
    use_item,
)

size = 8
substance = 256

north_movabilities = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
east_movabilities = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
south_movabilities = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]
west_movabilities = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

# ------------------------------------------ init_search ------------------------------------------


def init_search(reset_limit):
    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)
        reset_limit -= 1

    visited = {(0, 0)}

    if can_move(North):
        north_movabilities[0][0] = 1

        new_pos_x = 0
        new_pos_y = 1
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(North)
        reset_limit = init_search_north(visited, new_pos_x, new_pos_y, reset_limit)
        move(South)

    if can_move(East):
        east_movabilities[0][0] = 1

        new_pos_x = 1
        new_pos_y = 0
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(East)
        reset_limit = init_search_east(visited, new_pos_x, new_pos_y, reset_limit)
        move(West)

    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)
        reset_limit -= 1

    return reset_limit


def init_search_north(visited, current_x, current_y, reset_limit):
    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)
        reset_limit -= 1

    if can_move(North):
        north_movabilities[current_x][current_y] = 1

        new_pos_x = current_x
        new_pos_y = current_y + 1
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(North)
        reset_limit = init_search_north(visited, new_pos_x, new_pos_y, reset_limit)
        move(South)

    if can_move(East):
        east_movabilities[current_x][current_y] = 1

        new_pos_x = current_x + 1
        new_pos_y = current_y
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(East)
        reset_limit = init_search_east(visited, new_pos_x, new_pos_y, reset_limit)
        move(West)

    south_movabilities[current_x][current_y] = 1

    if can_move(West):
        west_movabilities[current_x][current_y] = 1

        new_pos_x = current_x - 1
        new_pos_y = current_y
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(West)
        reset_limit = init_search_west(visited, new_pos_x, new_pos_y, reset_limit)
        move(East)

    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)
        reset_limit -= 1

    return reset_limit


def init_search_east(visited, current_x, current_y, reset_limit):
    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)
        reset_limit -= 1

    if can_move(North):
        north_movabilities[current_x][current_y] = 1

        new_pos_x = current_x
        new_pos_y = current_y + 1
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(North)
        reset_limit = init_search_north(visited, new_pos_x, new_pos_y, reset_limit)
        move(South)

    if can_move(East):
        east_movabilities[current_x][current_y] = 1

        new_pos_x = current_x + 1
        new_pos_y = current_y
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(East)
        reset_limit = init_search_east(visited, new_pos_x, new_pos_y, reset_limit)
        move(West)

    if can_move(South):
        south_movabilities[current_x][current_y] = 1

        new_pos_x = current_x
        new_pos_y = current_y - 1
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(South)
        reset_limit = init_search_south(visited, new_pos_x, new_pos_y, reset_limit)
        move(North)

    west_movabilities[current_x][current_y] = 1

    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)
        reset_limit -= 1

    return reset_limit


def init_search_south(visited, current_x, current_y, reset_limit):
    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)
        reset_limit -= 1

    north_movabilities[current_x][current_y] = 1

    if can_move(East):
        east_movabilities[current_x][current_y] = 1

        new_pos_x = current_x + 1
        new_pos_y = current_y
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(East)
        reset_limit = init_search_east(visited, new_pos_x, new_pos_y, reset_limit)
        move(West)

    if can_move(South):
        south_movabilities[current_x][current_y] = 1

        new_pos_x = current_x
        new_pos_y = current_y - 1
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(South)
        reset_limit = init_search_south(visited, new_pos_x, new_pos_y, reset_limit)
        move(North)

    if can_move(West):
        west_movabilities[current_x][current_y] = 1

        new_pos_x = current_x - 1
        new_pos_y = current_y
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(West)
        reset_limit = init_search_west(visited, new_pos_x, new_pos_y, reset_limit)
        move(East)

    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)
        reset_limit -= 1

    return reset_limit


def init_search_west(visited, current_x, current_y, reset_limit):
    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)
        reset_limit -= 1

    if can_move(North):
        north_movabilities[current_x][current_y] = 1

        new_pos_x = current_x
        new_pos_y = current_y + 1
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(North)
        reset_limit = init_search_north(visited, new_pos_x, new_pos_y, reset_limit)
        move(South)

    east_movabilities[current_x][current_y] = 1

    if can_move(South):
        south_movabilities[current_x][current_y] = 1

        new_pos_x = current_x
        new_pos_y = current_y - 1
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(South)
        reset_limit = init_search_south(visited, new_pos_x, new_pos_y, reset_limit)
        move(North)

    if can_move(West):
        west_movabilities[current_x][current_y] = 1

        new_pos_x = current_x - 1
        new_pos_y = current_y
        new_pos = (new_pos_x, new_pos_y)
        if new_pos in visited:
            return reset_limit
        visited.add(new_pos)

        move(West)
        reset_limit = init_search_west(visited, new_pos_x, new_pos_y, reset_limit)
        move(East)

    if get_entity_type() == Entities.Treasure:
        use_item(Items.Weird_Substance, substance)
        reset_limit -= 1

    return reset_limit


# ------------------------------------------------------------------------------------


def update_cell(current_x, current_y):
    if can_move(North):
        north_movabilities[current_x][current_y] = 1
    if can_move(East):
        east_movabilities[current_x][current_y] = 1
    if can_move(South):
        south_movabilities[current_x][current_y] = 1
    if can_move(West):
        west_movabilities[current_x][current_y] = 1


# def bfs(current_x, current_y, treasure):
#     current = (current_x, current_y)
#     if current == treasure:
#         return []

#     visited = {current}
#     routes = [[]]
#     current_cost = 0
#     current_queue = [(current_x, current_y, 0, None)]
#     priority_queues = {}

#     while True:
#         while len(current_queue) == 0:
#             current_cost += 1
#             if current_cost in priority_queues:
#                 current_queue = priority_queues[current_cost]

#         pos_x, pos_y, route_num, came_from = current_queue.pop(0)
#         tmp_route = routes[route_num][:]
#         tmp_cost = current_cost + 1

#         north_movability = 0
#         east_movability = 0
#         south_movability = 0
#         west_movability = 0
#         movability = 0
#         while True:
#             if came_from == North:
#                 north_movability = 0
#                 east_movability = east_movabilities[pos_x][pos_y]
#                 south_movability = south_movabilities[pos_x][pos_y]
#                 west_movability = west_movabilities[pos_x][pos_y]
#             elif came_from == East:
#                 north_movability = north_movabilities[pos_x][pos_y]
#                 east_movability = 0
#                 south_movability = south_movabilities[pos_x][pos_y]
#                 west_movability = west_movabilities[pos_x][pos_y]
#             elif came_from == South:
#                 north_movability = north_movabilities[pos_x][pos_y]
#                 east_movability = east_movabilities[pos_x][pos_y]
#                 south_movability = 0
#                 west_movability = west_movabilities[pos_x][pos_y]
#             elif came_from == West:
#                 north_movability = north_movabilities[pos_x][pos_y]
#                 east_movability = east_movabilities[pos_x][pos_y]
#                 south_movability = south_movabilities[pos_x][pos_y]
#                 west_movability = 0
#             else:
#                 north_movability = north_movabilities[pos_x][pos_y]
#                 east_movability = east_movabilities[pos_x][pos_y]
#                 south_movability = south_movabilities[pos_x][pos_y]
#                 west_movability = west_movabilities[pos_x][pos_y]

#             movability = (
#                 north_movability + east_movability + south_movability + west_movability
#             )
#             if movability != 1:
#                 break

#             if north_movability:
#                 tmp_route.append(North)
#                 pos_y += 1
#                 came_from = South
#             elif east_movability:
#                 tmp_route.append(East)
#                 pos_x += 1
#                 came_from = West
#             elif south_movability:
#                 tmp_route.append(South)
#                 pos_y -= 1
#                 came_from = North
#             else:
#                 tmp_route.append(West)
#                 pos_x -= 1
#                 came_from = East

#             tmp_cost += 1

#             new_pos = (pos_x, pos_y)
#             if new_pos == treasure:
#                 return tmp_route
#             if new_pos in visited:
#                 movability = 0
#                 break
#             visited.add(new_pos)

#         if movability == 0:
#             continue

#         if tmp_cost not in priority_queues:
#             priority_queues[tmp_cost] = []

#         if north_movability:
#             new_pos_y = pos_y + 1
#             new_pos = (pos_x, new_pos_y)

#             if new_pos == treasure:
#                 tmp_route.append(North)
#                 return tmp_route

#             if new_pos not in visited:
#                 visited.add(new_pos)

#                 new_route_num = len(routes)
#                 new_route = tmp_route[:]
#                 new_route.append(North)
#                 routes.append(new_route)

#                 priority_queues[tmp_cost].append(
#                     (pos_x, new_pos_y, new_route_num, South)
#                 )

#         if east_movability:
#             new_pos_x = pos_x + 1
#             new_pos = (new_pos_x, pos_y)

#             if new_pos == treasure:
#                 tmp_route.append(East)
#                 return tmp_route

#             if new_pos not in visited:
#                 visited.add(new_pos)

#                 new_route_num = len(routes)
#                 new_route = tmp_route[:]
#                 new_route.append(East)
#                 routes.append(new_route)

#                 priority_queues[tmp_cost].append(
#                     (new_pos_x, pos_y, new_route_num, West)
#                 )

#         if south_movability:
#             new_pos_y = pos_y - 1
#             new_pos = (pos_x, new_pos_y)

#             if new_pos == treasure:
#                 tmp_route.append(South)
#                 return tmp_route

#             if new_pos not in visited:
#                 visited.add(new_pos)

#                 new_route_num = len(routes)
#                 new_route = tmp_route[:]
#                 new_route.append(South)
#                 routes.append(new_route)

#                 priority_queues[tmp_cost].append(
#                     (pos_x, new_pos_y, new_route_num, North)
#                 )

#         if west_movability:
#             new_pos_x = pos_x - 1
#             new_pos = (new_pos_x, pos_y)

#             if new_pos == treasure:
#                 tmp_route.append(West)
#                 return tmp_route

#             if new_pos not in visited:
#                 visited.add(new_pos)

#                 new_route_num = len(routes)
#                 new_route = tmp_route[:]
#                 new_route.append(West)
#                 routes.append(new_route)

#                 priority_queues[tmp_cost].append(
#                     (new_pos_x, pos_y, new_route_num, East)
#                 )


def dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(current_x, current_y, treasure):
    current = (current_x, current_y)
    if current == treasure:
        return []

    treasure_x, treasure_y = treasure

    visited = {current}
    routes = [[]]
    current_cost = dist(current_x, current_y, treasure_x, treasure_y)
    priority_queues = {current_cost: [(current_x, current_y, 0, None, 0)]}

    while True:
        if len(priority_queues[current_cost]) == 0:
            current_cost += 1
            while current_cost not in priority_queues:
                current_cost += 1

        pos_x, pos_y, route_num, came_from, base_cost = priority_queues[
            current_cost
        ].pop(0)
        tmp_route = routes[route_num]
        tmp_cost = base_cost + 1

        north_movability = 0
        east_movability = 0
        south_movability = 0
        west_movability = 0
        movability = 0
        while True:
            if came_from == North:
                north_movability = 0
                east_movability = east_movabilities[pos_x][pos_y]
                south_movability = south_movabilities[pos_x][pos_y]
                west_movability = west_movabilities[pos_x][pos_y]
            elif came_from == East:
                north_movability = north_movabilities[pos_x][pos_y]
                east_movability = 0
                south_movability = south_movabilities[pos_x][pos_y]
                west_movability = west_movabilities[pos_x][pos_y]
            elif came_from == South:
                north_movability = north_movabilities[pos_x][pos_y]
                east_movability = east_movabilities[pos_x][pos_y]
                south_movability = 0
                west_movability = west_movabilities[pos_x][pos_y]
            elif came_from == West:
                north_movability = north_movabilities[pos_x][pos_y]
                east_movability = east_movabilities[pos_x][pos_y]
                south_movability = south_movabilities[pos_x][pos_y]
                west_movability = 0
            else:
                north_movability = north_movabilities[pos_x][pos_y]
                east_movability = east_movabilities[pos_x][pos_y]
                south_movability = south_movabilities[pos_x][pos_y]
                west_movability = west_movabilities[pos_x][pos_y]

            movability = (
                north_movability + east_movability + south_movability + west_movability
            )
            if movability != 1:
                break

            if north_movability:
                tmp_route.append(North)
                pos_y += 1
                came_from = South
            elif east_movability:
                tmp_route.append(East)
                pos_x += 1
                came_from = West
            elif south_movability:
                tmp_route.append(South)
                pos_y -= 1
                came_from = North
            else:
                tmp_route.append(West)
                pos_x -= 1
                came_from = East

            tmp_cost += 1

            new_pos = (pos_x, pos_y)
            if new_pos == treasure:
                return tmp_route
            if new_pos in visited:
                movability = 0
                break
            visited.add(new_pos)

        if movability == 0:
            continue

        if north_movability:
            new_pos_y = pos_y + 1
            new_pos = (pos_x, new_pos_y)

            if new_pos == treasure:
                tmp_route.append(North)
                return tmp_route

            if new_pos not in visited:
                visited.add(new_pos)

                new_route_num = len(routes)
                new_route = tmp_route[:]
                new_route.append(North)
                routes.append(new_route)

                new_cost = tmp_cost + dist(pos_x, new_pos_y, treasure_x, treasure_y)
                if new_cost not in priority_queues:
                    priority_queues[new_cost] = [
                        (pos_x, new_pos_y, new_route_num, South, tmp_cost)
                    ]
                else:
                    priority_queues[new_cost].append(
                        (pos_x, new_pos_y, new_route_num, South, tmp_cost)
                    )

        if east_movability:
            new_pos_x = pos_x + 1
            new_pos = (new_pos_x, pos_y)

            if new_pos == treasure:
                tmp_route.append(East)
                return tmp_route

            if new_pos not in visited:
                visited.add(new_pos)

                new_route_num = len(routes)
                new_route = tmp_route[:]
                new_route.append(East)
                routes.append(new_route)

                new_cost = tmp_cost + dist(new_pos_x, pos_y, treasure_x, treasure_y)
                if new_cost not in priority_queues:
                    priority_queues[new_cost] = [
                        (new_pos_x, pos_y, new_route_num, West, tmp_cost)
                    ]
                else:
                    priority_queues[new_cost].append(
                        (new_pos_x, pos_y, new_route_num, West, tmp_cost)
                    )

        if south_movability:
            new_pos_y = pos_y - 1
            new_pos = (pos_x, new_pos_y)

            if new_pos == treasure:
                tmp_route.append(South)
                return tmp_route

            if new_pos not in visited:
                visited.add(new_pos)

                new_route_num = len(routes)
                new_route = tmp_route[:]
                new_route.append(South)
                routes.append(new_route)

                new_cost = tmp_cost + dist(pos_x, new_pos_y, treasure_x, treasure_y)
                if new_cost not in priority_queues:
                    priority_queues[new_cost] = [
                        (pos_x, new_pos_y, new_route_num, North, tmp_cost)
                    ]
                else:
                    priority_queues[new_cost].append(
                        (pos_x, new_pos_y, new_route_num, North, tmp_cost)
                    )

        if west_movability:
            new_pos_x = pos_x - 1
            new_pos = (new_pos_x, pos_y)

            if new_pos == treasure:
                tmp_route.append(West)
                return tmp_route

            if new_pos not in visited:
                visited.add(new_pos)

                new_route_num = len(routes)
                new_route = tmp_route
                new_route.append(West)
                routes.append(new_route)

                new_cost = tmp_cost + dist(new_pos_x, pos_y, treasure_x, treasure_y)
                if new_cost not in priority_queues:
                    priority_queues[new_cost] = [
                        (new_pos_x, pos_y, new_route_num, East, tmp_cost)
                    ]
                else:
                    priority_queues[new_cost].append(
                        (new_pos_x, pos_y, new_route_num, East, tmp_cost)
                    )


with_update_num = 245
without_update_num = 55


def search():
    current_x = 0
    current_y = 0
    limit = init_search(with_update_num)

    for _ in range(limit):
        route = a_star(current_x, current_y, measure())
        for dir in route:
            move(dir)
            current_x = get_pos_x()
            current_y = get_pos_y()
            update_cell(current_x, current_y)

        use_item(Items.Weird_Substance, substance)

    for _ in range(without_update_num):
        route = a_star(current_x, current_y, measure())
        for dir in route:
            move(dir)

        use_item(Items.Weird_Substance, substance)
        current_x = get_pos_x()
        current_y = get_pos_y()

    route = a_star(current_x, current_y, measure())
    for dir in route:
        move(dir)
    harvest()


def run():
    plant(Entities.Bush)
    use_item(Items.Weird_Substance, substance)

    search()


run()
