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
size_minus_2 = 30
half_size = 16
twice_size = 64

max_drone = 32
max_drone_minus_1 = 31


def sort_cactus_line(finalize_func, direction, reverse):
    i = 0
    returning_len = 1

    while True:
        if measure() > measure(direction) and swap(direction) and i > 0:
            if i < half_size or not spawn_drone(
                sort_cactus_slave(i, finalize_func, reverse)
            ):
                move(reverse)
                returning_len += 1
                i -= 1
                continue

        if returning_len == 1:
            i += 1
            if i == size_minus_1:
                return
            move(direction)
            continue

        tmp_i = i
        i += returning_len
        if i == size_minus_1:
            return

        if returning_len < half_size:
            for _ in range(returning_len):
                move(direction)
        else:
            for _ in range(tmp_i + 2):
                move(reverse)
            for _ in range(size_minus_2 - returning_len - tmp_i):
                if measure() > measure(direction):
                    swap(direction)
                move(reverse)

        returning_len = 1


def sort_cactus_slave(i, finalize_func, reverse):
    def sort_func():
        for _ in range(i):
            if measure() < measure(reverse) and swap(reverse):
                move(reverse)
            else:
                break

        if num_drones() == 1:
            finalize_func()

    return sort_func


def farm_cactus_row_leader():
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

    if get_pos_y() == 0:
        farm_cactus_column_leader()


def farm_cactus_column_leader():
    threshold = 16

    while threshold > 0:
        for _ in range(threshold):
            while num_drones() > max_drone_minus_1 - (threshold // 2):
                pass

            drone = None
            while not drone:
                drone = spawn_drone(farm_cactus_column)
            move(East)

        threshold //= 2

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
