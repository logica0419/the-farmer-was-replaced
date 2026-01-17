from __builtins__ import (
    East,
    Entities,
    North,
    South,
    West,
    get_pos_y,
    harvest,
    measure,
    move,
    num_drones,
    plant,
    range,
    spawn_drone,
    swap,
    till,
)

size = 32
size_minus_1 = 31
half_size = 16
one_fourth_size_minus_1 = 7

max_drone = 32
threshold = 10


def sort_cactus_line(finalize_func, direction, inverse):
    i = 1
    n = -size
    inverted = 0

    while True:
        n += 1

        if measure() < measure(inverse) and swap(inverse) and i > 1:
            move(inverse)
            if n < size:
                inverted += 1
                i -= 1
                continue

            if spawn_drone(sort_cactus_slave(i - 1, finalize_func, inverse)):
                move(direction)
            else:
                inverted += 1
                i -= 1
                continue

        inverted_plus_1 = inverted + 1
        i += inverted_plus_1
        if i >= size:
            return

        if inverted >= half_size:
            for _ in range(size - inverted_plus_1):
                move(inverse)
        else:
            for _ in range(inverted_plus_1):
                move(direction)
        inverted = 0


def sort_cactus_slave(i, finalize_func, inverse):
    def sort_func():
        for _ in range(i):
            if measure() < measure(inverse) and swap(inverse):
                move(inverse)
            else:
                break

        if num_drones() == 1:
            finalize_func()

    return sort_func


def farm_cactus_row_leader():
    move(East)

    for _ in range(size_minus_1):
        spawn_drone(farm_cactus_row)
        move(North)

    farm_cactus_row()


def farm_cactus_row():
    for _ in range(32):
        till()
        plant(Entities.Cactus)
        move(East)

    sort_cactus_line(harvest, East, West)

    if get_pos_y() == 1:
        farm_cactus_column_leader()


def farm_cactus_column_leader():
    for _ in range(max_drone - 1 - threshold):
        while num_drones() > max_drone - threshold:
            pass

        drone = None
        while not drone:
            drone = spawn_drone(farm_cactus_column)
        move(East)

    while num_drones() > max_drone - threshold:
        pass

    for _ in range(threshold):
        drone = None
        while not drone:
            drone = spawn_drone(farm_cactus_column)
        move(East)

    farm_cactus_column()


def farm_cactus_column():
    while num_drones() < max_drone:
        pass

    sort_cactus_line(harvest, North, South)

    if num_drones() == 1:
        harvest()


def run():
    farm_cactus_row_leader()


run()
