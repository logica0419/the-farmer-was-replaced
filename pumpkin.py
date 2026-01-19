from __builtins__ import (
    East,
    Entities,
    Items,
    North,
    can_harvest,
    get_entity_type,
    get_pos_x,
    get_water,
    harvest,
    move,
    num_drones,
    num_items,
    plant,
    range,
    spawn_drone,
    till,
    use_item,
)

size = 32
size_minus_1 = 31
half_size = 16

max_drone = 32
max_drone_minus_1 = 31


def eliminate_dead_pumpkin():
    pos = get_pos_x()
    not_harvestable = []

    for i in range(size):
        if not can_harvest():
            while True:
                plant(Entities.Pumpkin)
                if not num_items(Items.Fertilizer) or can_harvest():
                    break
                use_item(Items.Fertilizer)

            if not can_harvest():
                plant(Entities.Pumpkin)
                while get_water() < 0.75 and use_item(Items.Water):
                    continue

                if not can_harvest():
                    not_harvestable.append((i + pos) % size)

        move(East)

    while len(not_harvestable):
        for nh in not_harvestable:
            diff = nh - pos
            if diff < 0:
                for _ in range(size + diff):
                    move(East)
            else:
                for _ in range(diff):
                    move(East)
            pos = nh

            if can_harvest() or spawn_drone(eliminate_dead_pumpkin_slave):
                not_harvestable.remove(nh)
            else:
                while True:
                    plant(Entities.Pumpkin)
                    if not num_items(Items.Fertilizer) or can_harvest():
                        break
                    use_item(Items.Fertilizer)

                if not can_harvest():
                    plant(Entities.Pumpkin)
                    while get_water() < 0.75 and use_item(Items.Water):
                        continue

                    if can_harvest():
                        not_harvestable.remove(nh)
                    elif get_entity_type() == Entities.Dead_Pumpkin:
                        plant(Entities.Pumpkin)

    if num_drones() == 1:
        harvest()
        if num_items(Items.Pumpkin) >= 200000000:
            return
        run()


def eliminate_dead_pumpkin_slave():
    while True:
        plant(Entities.Pumpkin)
        if not num_items(Items.Fertilizer) or can_harvest():
            break
        use_item(Items.Fertilizer)

    while not can_harvest():
        plant(Entities.Pumpkin)

        while get_water() < 0.75 and use_item(Items.Water):
            continue

    if num_drones() == 1:
        harvest()
        if num_items(Items.Pumpkin) >= 200000000:
            return
        run()


def farm_pumpkin():
    for _ in range(32):
        plant(Entities.Pumpkin)
        move(East)

    eliminate_dead_pumpkin()


def run():
    for _ in range(size_minus_1):
        spawn_drone(farm_pumpkin)
        move(North)

    farm_pumpkin()


def farm_pumpkin_init():
    for _ in range(32):
        till()
        plant(Entities.Pumpkin)
        move(East)

    eliminate_dead_pumpkin()


def run_init():
    for _ in range(size_minus_1):
        spawn_drone(farm_pumpkin_init)
        move(North)

    farm_pumpkin_init()


run_init()
