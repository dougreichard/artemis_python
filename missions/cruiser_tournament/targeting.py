from tonnage import SpawnState
from PyAddons.formations.vec import Vec3

def assign_closest(sim, chaser,  *args):
    # Has not spawned
    if not hasattr(chaser, 'id'):
        return False
    chaser_id = getattr(chaser, 'id')
    ship = sim.get_space_object(chaser_id)
    if ship is None:
        return False
    from_pos = Vec3(ship.pos.x, ship.pos.y, ship.pos.z)
    last_dist = float('inf')
    for targets in args:
        to_pos  = None
        to_id = None
        # iterate each set of targets until one is found
        # args should be in priority order
        for target in targets:
            test_id = getattr(target, 'id')
            test = sim.get_space_object(test_id)
            if test is not None:
                test_pos = Vec3(test.pos.x, test.pos.y, test.pos.z)
                dist = (from_pos - test_pos).length()
                if dist < last_dist:
                    to_pos = test_pos
                    last_dist = dist
                    to_id = test_id

        if to_pos is not None:
            blob = ship.data_set

            blob.set("target_pos_x", to_pos.x,0)
            blob.set("target_pos_y", to_pos.y,0)
            blob.set("target_pos_z", to_pos.z,0)
            blob.set("target_id", to_id,0)
            # print(f'{chaser_id} is attacking {to_id}')
            return True

    return False

def assign_targets(sim, chasers, *args):
    for chaser in chasers:
        to_pos = assign_closest(sim, chaser, args)
        if not to_pos :
            print('could not find target')



