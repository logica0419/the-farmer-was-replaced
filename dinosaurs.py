from __builtins__ import (
    East,
    Hats,
    North,
    South,
    West,
    can_move,
    change_hat,
    clear,
    get_pos_y,
    get_world_size,
    measure,
    move,
    spawn_drone,
)

size = get_world_size()
half_size = size // 2
size_minus_1 = size - 1
size_minus_2 = size - 2
half_size_square = (size * size) // 2


def finalize():
    change_hat(Hats.Straw_Hat)
    spawn_drone(main)


def dinosaur_move(dir, treasure_y, count):
    m = measure()
    if m:
        treasure_y = m[1]
        count += 1

    if can_move(dir):
        move(dir)
    else:
        finalize()
        count = -1

    return treasure_y, count


def main():
    clear()
    change_hat(Hats.Dinosaur_Hat)

    treasure_y = size, size
    count = 0

    treasure_y, count = dinosaur_move(East, treasure_y, count)
    if treasure_y > 1:
        treasure_y, count = dinosaur_move(North, treasure_y, count)
        treasure_y, count = dinosaur_move(North, treasure_y, count)

    while count > -1:
        for _ in range(half_size):
            while (
                count < half_size_square
                and treasure_y - 1 > get_pos_y()
                and can_move(West)
            ):
                treasure_y, count = dinosaur_move(North, treasure_y, count)
                treasure_y, count = dinosaur_move(North, treasure_y, count)

            for _ in range(size_minus_2):
                treasure_y, count = dinosaur_move(East, treasure_y, count)
            treasure_y, count = dinosaur_move(North, treasure_y, count)

            for _ in range(size_minus_2):
                treasure_y, count = dinosaur_move(West, treasure_y, count)

            if get_pos_y() == size_minus_1:
                break

            if (
                count < half_size_square
                and treasure_y <= get_pos_y()
                and get_pos_y() - treasure_y > count // size
                and can_move(West)
            ):
                break

            treasure_y, count = dinosaur_move(North, treasure_y, count)

        treasure_y, count = dinosaur_move(West, treasure_y, count)
        treasure_y, count = dinosaur_move(South, treasure_y, count)

        while get_pos_y() > 0:
            if (
                count < half_size_square
                and treasure_y >= get_pos_y()
                and can_move(East)
            ):
                break
            if get_pos_y() != size_minus_1:
                treasure_y, count = dinosaur_move(South, treasure_y, count)
            treasure_y, count = dinosaur_move(South, treasure_y, count)

        treasure_y, count = dinosaur_move(East, treasure_y, count)


main()
