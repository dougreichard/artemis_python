from tonnage import TonnageHunter
from PyAddons.formations.vec import Vec3

class Whale:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

    def spawn(self, sim):
        #TODO: Whales are needed
        # self.id = sim.add_active("whale", "whale") #pod? ??
        self.id = sim.make_new_passive("behav_asteroid, ", "Asteroid 1")
        obj = sim.get_space_object(self.id)
        sim.reposition_space_object(obj, self.x, 0,self.z)
        

    def exists(self, sim):
        sim.space_object_exists(self.id)

"""
Manage all the whales
"""
class WhaleHunt:
    whales = [
        Whale("Ed",40000,-500,91000),
        Whale("Al",40000,500,4000),
        Whale("Jo",60000,-500,4000),
        Whale("An",60000,500,91000),
        Whale("Ki",95000,-500,25000),
        Whale("Lu",5000,500,25000),
        Whale("Pi",5000,-500,40000),
        Whale("Te",95000,500,40000),
    ]
    hunters = [  
        TonnageHunter("Hunter[1]", 58300,57,78300, 70),
        TonnageHunter("Hunter[2]", 59300,57,23500, 80),
        TonnageHunter("Hunter[3]", 38200,-57,43500, 90),
        TonnageHunter("Hunter[4]", 58200,-245,43500, 100),
    ]
    huntable_distance = 2000
    
    def start(self, sim):
        for whale in self.whales:
            whale.spawn(sim)
        for hunter in self.hunters:
            hunter.spawn(sim)

    def tick(self, sim):
        # hunters hunt whales
        # using beacons?
        for hunter in self.hunters:
             if sim.space_object_exists(hunter.id):
                    hunter_obj = sim.get_space_object(hunter.id)
                    self.chase_closest_whale(sim, hunter_obj)
                    
    def chase_closest_whale(self, sim, hunter):
        hunter_pos = Vec3(hunter.pos.x, hunter.pos.y, hunter.pos.z)
        for whale in self.whales:
            if whale.exists(sim):
                whale_obj = sim.get_space_object(whale.id)
                whale_pos = Vec3(whale_obj.pos.x, whale_obj.pos.y, whale_obj.pos.z)
                diff = hunter_pos - whale_pos
                if diff.length() < self.huntable_distance:
                    blob = hunter.data_set
                    # make the npc's target be the position of the player
                    blob.set("target_pos_x", whale_pos.x,0)
                    blob.set("target_pos_y", whale_pos.y,0)
                    blob.set("target_pos_z", whale_pos.z,0)
                    blob.set("target_id", whale_obj.unique_ID,0)
    """
    this will actually be called by another system (periods)
    at the period end it calculates the bonus
    from how many whales are still active
    
    So this is no longer called every tick
    """
    def bonus(self, sim):
        bonus = 0
        for whale in self.whales:
            if whale.exists(sim):
                bonus += 1
        return bonus
    
