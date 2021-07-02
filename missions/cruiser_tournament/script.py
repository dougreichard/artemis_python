# import GAME
# import Difficulty
# import Mayday
# import Stations
# import Cargo
# import Destroyers

from periods import Periods
from bonusfleets import BonusFleets
from stations import Stations

import sbs


from tonnage import SpawnState, TonnageObject, TonnageTorgoth, TonnageSkaraan, TonnageHunter
"""
  A TSN Cruiser has 48 minutes to vanquish as many enemies as possible.^^For a full crew of 6 in Artemis 2.7.1.^^Your Comms Officer should take notes or print out the Communications Cheat Sheet in the mission folder.
"""
class Mission:
    enemies = [
        # KRALIANS
        TonnageObject("K00", 40300.0, 0.0, 52300.0, 45,
                      "Kralien", "Cruiser", "small", fleet_number=68),
        TonnageObject("K01", 40300.0, 0.0, 52000.0, 45,
                      "Kralien", "Cruiser", "small", fleet_number=68),
        TonnageObject("K02", 40000.0, 0.0, 52000.0, 45,
                      "Kralien", "Cruiser", "small", fleet_number=68),
        TonnageObject("K04", 60000.0, 0.0, 47000.0, 180, "Kralien",
                      "Battleship", "medium", fleet_number=69),
        TonnageObject("K05", 60700.0, 0.0, 47000.0, 180, "Kralien",
                      "Battleship", "medium", fleet_number=69),
        TonnageObject("K06", 60300.0, 0.0, 47000.0, 180, "Kralien",
                      "Battleship", "medium", fleet_number=69),
        TonnageObject("K07", 70000.0, 0.0, 42000.0, 180, "Kralien",
                      "Dreadnought", "large", fleet_number=67),
        TonnageObject("K08", 69700.0, 0.0, 42000.0, 180, "Kralien",
                      "Dreadnought", "large", fleet_number=67),
        TonnageObject("K09", 70300.0, 0.0, 42000.0, 180, "Kralien",
                      "Dreadnought", "large", fleet_number=67),
        TonnageObject("K10", 60300.0, 0.0, 2300.0, 45,
                      "Kralien", "Cruiser", "small", fleet_number=57),
        TonnageObject("K11", 60300.0, 0.0, 2000.0, 45,
                      "Kralien", "Cruiser", "small", fleet_number=57),
        TonnageObject("K12", 60000.0, 0.0, 2000.0, 45,
                      "Kralien", "Cruiser", "small", fleet_number=57),
        TonnageObject("K14", 60000.0, 0.0, 17000.0, 180, "Kralien",
                      "Battleship", "medium", fleet_number=58),
        TonnageObject("K15", 59700.0, 0.0, 17000.0, 180, "Kralien",
                      "Battleship", "medium", fleet_number=58),
        TonnageObject("K16", 60300.0, 0.0, 17000.0, 180, "Kralien",
                      "Battleship", "medium", fleet_number=58),
        TonnageObject("K17", 60000.0, 0.0, 12000.0, 180, "Kralien",
                      "Dreadnought", "large", fleet_number=59),
        TonnageObject("K18", 59700.0, 0.0, 12000.0, 180, "Kralien",
                      "Dreadnought", "large", fleet_number=59),
        TonnageObject("K19", 60300.0, 0.0, 12000.0, 180, "Kralien",
                      "Dreadnought", "large", fleet_number=59),
        # SKARRAN
        TonnageSkaraan("K61", 50500.0, 0.0, 41500.0, 260.0, "Skaraan", "Defiler", "small", fleet_number=22,
                      abilities={'ability_captain': "Warp", 'ability_clear': "Cloak,Drones,AnitiMine,shlddrain,shldvamp,LowVis,Stealth"}),
        # PIRATES
       TonnageObject("Lusty Wrench", 10.0, 10.0, 10.0, 45, "Pirate",
                    "Strongbow", "", fleet_number=1),
        # NOTE: Original had different points for these 40,20 vs 20,10
        TonnageObject("Nimbus", 99990.0, -10.0, 10.0, 45, "Pirate",
                      "Strongbow", "", fleet_number=2),
        # Torgoth
        TonnageTorgoth("Behemoth 1", 22222.0, 500.0, 22200.0, 45.0, "Torgoth",
                       "Behemoth", "large", fleet_number=5, ship=0.0, captain=1.0),
        TonnageTorgoth("Goliath 1", 22000.0, 0.0, 23000.0, 45.0, "Torgoth",
                       "Goliath", "small", fleet_number=5, ship=1.0, captain=-1.0),
        TonnageTorgoth("Goliath 2", 22433.0, 500.0, 21800.0, 45.0, "Torgoth",
                       "Goliath", "small", fleet_number=5, ship=-1.0, captain=-1.0),
        TonnageTorgoth("Leviathan 1", 22000.0, 0.0, 23000.0, 45.0, "Torgoth",
                       "Leviathan", "medium", fleet_number=5, ship=0.0, captain=0.0),
        TonnageTorgoth("Leviathan 2", 21000.0, 0.0, 22000.0, 45.0, "Torgoth",
                       "Leviathan", "medium", fleet_number=5, ship=-1.0, captain=-1.0),
    ]

    # Maybe these should be in periods
    # so they are not hooked in yet
    bonus_fleets = BonusFleets()
    periods = Periods()
    stations = Stations()

    def start_map(self, sim):
        # <set_object_property property="nebulaIsOpaque" value="0"/>
        # <set_object_property property="sensorSettingspec" value="0"/>
        # <create count="35" type="asteroids" startAngle="100" endAngle="300" startX="50000.0" startY="0.0" startZ="25000.0" radius="22000" randomRange="1200" randomSeed="3"/>
        # <create count="35" type="asteroids" startAngle="20" endAngle="110" startX="70000.0" startY="0.0" startZ="40000.0" radius="23000" randomRange="1000" randomSeed="4"/>
        # <create count="45" type="asteroids" startAngle="200" endAngle="300" startX="30000.0" startY="0.0" startZ="65000.0" radius="33000" randomRange="5000" randomSeed="2"/>
        # <create count="35" type="nebulas" startAngle="200" endAngle="300" startX="30000.0" startY="0.0" startZ="65000.0" radius="33000" randomRange="5000" randomSeed="2"/>
        # <create count="25" type="nebulas" startAngle="100" endAngle="300" startX="50000.0" startY="0.0" startZ="25000.0" radius="22000" randomRange="3200" randomSeed="3"/>
        # <create count="25" type="nebulas" startAngle="20" endAngle="110" startX="70000.0" startY="0.0" startZ="40000.0" radius="23000" randomRange="3000" randomSeed="4"/>
        # <!-- The Start Block also sets the skybox, which will be the main screen background throughout the mission -->
        # <set_skybox_index index="27"/>
        pass

    def start_player(self, sim):
        """
          Players start in bottom right of of the 100,000 x 100,000 sector with one shuttle 'Pilgrim' aboard
        """
        
        # playerID will be a NUMBER, a unique value for every space object that you create.
        self.playerID = sim.make_new_player("behav_playership", "Battle Cruiser");
        player = sim.get_space_object(self.playerID)
        sim.reposition_space_object(player, 50000,0,50000)

        # <set_player_carried_type player_slot="0" bay_slot="0" name="Dagger" raceKeys="TSN player" hullKeys="TSN Shuttle"/>
        # <create type="player" player_slot="0" x="39055.0" y="0.0" z="85951.0" angle="295" name="Artemis" raceKeys="TSN player" hullKeys="Light Cruiser" warp="yes" jump="no"/>
        # <set_object_property property="energy" value="1100" player_slot="0"/>
        # <set_object_property property="countEMP" value="4" player_slot="0"/>
        # <set_object_property property="countMine" value="6" player_slot="0"/>
        # <set_object_property property="countNuke" value="2" player_slot="0"/>
        # <set_object_property property="countHoming" value="8" player_slot="0"/>
        # <set_object_property property="countPshock" value="2" player_slot="0"/>

    def start(self, sim):
        self.start_map(sim)
        self.start_player(sim)
        #self.bonus_fleets.start(sim)
        for enemy in self.enemies:
            enemy.spawn(sim)
        self.jump_to = 0
        self.jump = 0
        self.stations.spawn(sim)
        # self.periods.start(sim)
        """
        The Start Block also presents players with the mission title

        <big_message title = "CRUISER TOURNAMENT" subtitle1 = "BY MIKE SUBSTELNY" subtitle2 = "a Challenge Tournament"/>
  
        Finally, the start block sets timers and variables to start the game
        """

    def tick(self, sim):
        # self.bonus_fleets.tick(sim)
        # self.periods.tick(sim)
        # if the player still exists
        if sim.space_object_exists(self.playerID):
            player = sim.get_space_object(self.playerID)
            for enemy in self.enemies:
                enemy.tick(sim)
                if sim.space_object_exists(enemy.id):
                    npc_ship = sim.get_space_object(enemy.id)
                    blob = npc_ship.data_set
                    # make the npc's target be the position of the player
                    blob.set("target_pos_x", player.pos.x,0)
                    blob.set("target_pos_y", player.pos.y,0)
                    blob.set("target_pos_z", player.pos.z,0)
                    blob.set("target_id", player.unique_ID,0)

        #things = self.stations.stations
        #self.do_jump(things = self.enemies)

    def do_jump(self, sim, things):
        # every ten second jump near something
        self.jump += 2
        
        if self.jump >2:
            thing = things[self.jump_to]
            if thing.state == SpawnState.Spawned: 
                thing_id = thing.id
                thing_obj = sim.get_space_object(thing_id)
                if thing_obj is not None:
                    player = sim.get_space_object(self.playerID)
                    x = thing_obj.pos.x
                    y = thing_obj.pos.y
                    z = thing_obj.pos.z
                    print(f'POS: {thing_obj.pos.x},{thing_obj.pos.y},{thing_obj.pos.z}')
                    #sim.reposition_space_object(player, thing_obj.pos.x+600,thing_obj.pos.y+20,thing_obj.pos.z+600)
                    sim.reposition_space_object(player, x+600,y+20,z+600)
            self.jump = 0
            self.jump_to = (self.jump_to+1) % len(things)
            
            print(f"next jump {self.jump_to} {things[self.jump_to].name}")


mission = Mission()


def HandleScriptStart(sim):
    global mission
    mission.start(sim)


def HandleScriptTick(sim):
    global mission
    mission.tick(sim)
