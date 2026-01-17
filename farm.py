from __builtins__ import (
    East,
    Entities,
    Items,
    North,
    South,
    West,
    can_harvest,
    clear,
    get_entity_type,
    get_pos_x,
    get_pos_y,
    get_world_size,
    harvest,
    has_finished,
    max_drones,
    measure,
    move,
    num_items,
    plant,
    range,
    spawn_drone,
    swap,
    till,
    use_item,
    wait_for,
)

size = get_world_size()
cactus_area_hight = 0
pumpkin_area_height = 0
sunflower_area_height = size * 3 // 4
carrot_area_height = size * 15 // 16

total_drones = max_drones()

size_minus_1 = size - 1
cactus_area_hight_minus_1 = cactus_area_hight - 1
pumpkin_area_height_plus_1 = pumpkin_area_height - cactus_area_hight + 1
pumpkin_area_height_minus_1 = pumpkin_area_height - cactus_area_hight - 1


def till_line():
    for _ in range(size):
        harvest()
        till()
        move(East)


def farm_cactus_line(direction):
    y = get_pos_y()

    sorted = True

    for _ in range(size):
        if get_entity_type() != Entities.Cactus:
            plant(Entities.Cactus)
            sorted = False

        here_measure = measure()
        south_measure = measure(South)
        west_measure = measure(West)

        if here_measure or here_measure == 0:
            if y != 0 and south_measure and here_measure < south_measure:
                swap(South)
                sorted = False
            if get_pos_x() != 0 and west_measure and here_measure < west_measure:
                swap(West)
                sorted = False
            move(direction)

    return sorted


def farm_cactus_sub():
    farm_cactus_line(East)


def farm_cactus():
    drone = None
    sorted = farm_cactus_line(West)

    while not sorted:
        if not drone or has_finished(drone):
            drone = spawn_drone(farm_cactus_sub)
        sorted = farm_cactus_line(West)

    if drone:
        wait_for(drone)


def farm_cactus_leader():
    move(West)

    while True:
        drones = []

        for _ in range(cactus_area_hight_minus_1):
            move(South)
            drones.append(spawn_drone(farm_cactus))

        for _ in range(cactus_area_hight_minus_1):
            move(North)

        farm_cactus()

        for drone in drones:
            if drone:
                wait_for(drone)

        harvest()


def farm_pumpkin():
    def grow(entity_type):
        if not can_harvest():
            if (
                entity_type
                and entity_type != Entities.Dead_Pumpkin
                and num_items(Items.Fertilizer) > 3
            ):
                use_item(Items.Fertilizer)
            else:
                while (
                    entity_type
                    and entity_type != Entities.Dead_Pumpkin
                    and not can_harvest()
                ):
                    use_item(Items.Water)
                    entity_type = get_entity_type()

    for _ in range(size):
        grow(get_entity_type())
        harvest()
        if get_pos_x() % pumpkin_area_height_plus_1 <= pumpkin_area_height_minus_1:
            plant(Entities.Pumpkin)
        else:
            plant(Entities.Sunflower)
        move(East)

    for _ in range(3):
        for _ in range(size):
            entity_type = get_entity_type()
            grow(entity_type)
            if not entity_type or entity_type == Entities.Dead_Pumpkin:
                plant(Entities.Pumpkin)
            if entity_type == Entities.Sunflower:
                harvest()
                plant(Entities.Sunflower)
            move(East)


def farm_pumpkin_leader():
    while True:
        drones = []

        for _ in range(pumpkin_area_height_minus_1):
            move(South)
            spawned = False
            while not spawned:
                drone = spawn_drone(farm_pumpkin)
                if drone:
                    drones.append(drone)
                    spawned = True

        for _ in range(pumpkin_area_height_minus_1):
            move(North)

        farm_pumpkin()

        for drone in drones:
            if drone:
                wait_for(drone)


def return_farm_func(y):
    def farm_common():
        if not can_harvest():
            if num_items(Items.Fertilizer) > 3:
                use_item(Items.Fertilizer)
            else:
                while not can_harvest():
                    use_item(Items.Water)
        harvest()

    def farm_sunflower():
        farm_common()
        plant(Entities.Sunflower)

    def farm_carrot():
        farm_common()
        plant(Entities.Carrot)

    def farm_other_1():
        farm_common()
        move(East)
        farm_common()
        plant(Entities.Tree)

    def farm_other_2():
        farm_common()
        plant(Entities.Tree)
        move(East)
        farm_common()

    if y < sunflower_area_height:
        return farm_sunflower
    elif y < carrot_area_height:
        return farm_carrot
    elif y % 2 == 1:
        return farm_other_1
    else:
        return farm_other_2


def farm():
    y = get_pos_y()

    if y < cactus_area_hight:
        till_line()
        if y == cactus_area_hight - 1:
            return farm_cactus_leader()
        else:
            return

    if y < pumpkin_area_height:
        till_line()
        if y == pumpkin_area_height - 1:
            return farm_pumpkin_leader()
        else:
            return

    if y < carrot_area_height:
        till_line()
        for _ in range(size):
            plant(Entities.Bush)
            move(East)

    farm_func = return_farm_func(y)

    while True:
        farm_func()
        move(East)
        if num_items(Items.Power) > 50000:
            break


def main():
    clear()

    for _ in range(total_drones - 1):
        spawn_drone(farm)
        move(North)
    farm()


main()
