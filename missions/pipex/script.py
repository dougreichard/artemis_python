import messaging 
import sbs


class Player:
    def spawn(self, sim):
        self.id = sim.make_new_player("behav_playership", "Battle Cruiser");
        player = sim.get_space_object(self.id)
        sim.reposition_space_object(player, 0.0,0,0.0)
    def tick(self, sim):
        pass

class Enemy:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def spawn(self, sim):
        self.id = sim.make_new_player("behav_npcship", "Behemoth");
        enemy = sim.get_space_object(self.id)
        sim.reposition_space_object(enemy, self.x,self.y,self.z)

    def tick(self, sim):
        pass

class Mission:
    def spawn(self, sim):
        self.player = Player()
        self.player.spawn(sim)
        self.enemies = []

    def spawn_enemy(self, sim):
        enemy = Enemy(len(self.enemies)*500,0,2000)
        enemy.spawn(sim)
        self.enemies.append(enemy)
        return enemy
    def remove_enemy(self, id):
        sbs.delete_object(id)


    def tick(self, sim):
        for enemy in self.enemies:
            enemy.tick(sim)

mission = Mission()
   


########################################################################################################
def  HandleScriptStart(sim):
    messaging.HandleScriptStart(sim)
    mission.spawn(sim)

def  HandleScriptTick(sim):
    messaging.HandleScriptTick(sim, mission)
    mission.tick(sim)

    
# This is just a test for running in python NOT artemis
if __name__ == '__main__':
    HandleScriptStart(None)



