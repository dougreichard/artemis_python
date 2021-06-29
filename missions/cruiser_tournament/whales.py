
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
class Whales:
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
    
    def start(self, sim):
        for whale in self.whales:
            whale.spawn(sim)

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
    
