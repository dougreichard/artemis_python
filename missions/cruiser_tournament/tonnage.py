from enum import Enum

class SpawnState(Enum):
        NotSpawned = 1
        Spawned = 2
        Destroyed = 3

"""
This is a base class for handling enemies and counting the tonnage
Enemy Ships in this game when destoryed or surrender score points
"""
class TonnageObject:
    ''' Total Score based on Tonnage - This is a class/static value'''
    tonnage = 0
    """
    This is a lookup table to score Tonnage
    TODO: maybe this should be logic now
    """
    POINTS= {
        "Enemy": {
            "Hunter": { "weight":40, "surrender":20 }
        },
        "Arvonian": {
            "Carrier": { "weight":45, "surrender":23 },
            "Light Carrier": { "weight":25, "surrender":13 },
        },
        "Kralien": {
            "Cruiser": { "weight":9, "surrender":5 },
            "Dreadnought": { "weight":25, "surrender":13 },
            "Battleship": { "weight":17, "surrender":9 },
        },
        "Torgoth": {
            "Goliath": { "weight":80, "surrender":40 },
            "Behemoth": { "weight":150, "surrender":75 },
            "Leviathan": { "weight":90, "surrender":45 },
        },
        "Pirate": {
            "Strongbow": { "weight":20, "surrender":10 },
        },
        "Terran": {
            "Destroyer": { "weight":-30, "surrender":-30 },
        },
        "Fiendly": {
            "Freighter": { "weight":-50, "surrender":-50 },
            "Base": { "weight":-90, "surrender":-90 },
        },
        "Skaraan": {
            "Defiler": { "weight":40, "surrender":20 },
            "Executor": { "weight":75, "surrender":35 },
            "Enforcer": { "weight":50, "surrender":25 },
        },
    }


    def __init__(self, name, x,y,z,angle, race,hull, size, fleet_number=-1):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.race = race
        self.hull = hull
        self.size = size
        self.fleet_number = fleet_number
        # these are temporary Since these are not in the ship data now
        if hull == 'Cruiser':
            self.hull = 'Battleship'
        if hull == 'Strongbow':
            self.hull = 'Battleship'
        # Dreadnought is mispelled in ship data
        if hull == 'Dreadnought':
            self.hull = 'Dreadnaught'
        if hull == 'Defiler':
            self.hull = 'Hunter'
        self.state = SpawnState.NotSpawned

    # add tonnage points when destroyed
    def score_points(self, sim, surrender):
        if self.race in TonnageObject.POINTS:
            race = TonnageObject.POINTS[self.race]
            if self.hull in race:
                if surrender: 
                    TonnageObject.tonnage += race[self.hull]['surrender']
                else:
                    TonnageObject.tonnage += race[self.hull]['weight']
                print(f'Total tonnage now: {TonnageObject.tonnage}')
                # <big_message title="${race} ${hull} ${name} destroyed" OR SURRENDER
                #       subtitle1="${_.int(weight) <0?'Penalty ':''}${weight} kilotons" subtitle2=""/>
                # <log text="${race} ${hull} ${name} destroyed"/>

                # <set_object_property property="topSpeed" value="0.2" name="${name}"/>
                # <big_message title="${race} ${hull} surrendered" subtitle1="${weight} kilotons" subtitle2="+${surrender} kt surrender bonus"/>
                # <log text="${race} ${hull} ${name} Surrendered"/>

    def tick(self, sim):
        self.update_state(sim)

    def update_state(self, sim):
        if self.state == SpawnState.Spawned:
            if not sim.space_object_exists(self.id):
                self.state = SpawnState.Destroyed
                self.score_points(sim, False)
            # esif IF SURRENDERED
            # <if_object_property property="hasSurrendered" name="${name}" comparator="EQUALS" value="1"/>


    def spawn(self, sim):
        self.id = sim.make_new_active('behav_npcship', self.hull)
        obj = sim.get_space_object(self.id)
        sim.reposition_space_object(obj, self.x,self.y,self.z)
        print(f"Spawned {self.id}:{self.name} at:{obj.pos.x},:{obj.pos.y},:{obj.pos.z}")
        self.state = SpawnState.Spawned
        #TODO: set the name
        #TODO: set the angle
        #TODO: what to do with size
        #TODO captain and ship
       

"""
Skaraan ships have extra ability settings
"""
class TonnageSkaraan(TonnageObject):
    def __init__(self, name, x,y,z,angle, race,hull, size, fleet_number=-1, abilities=None,):
        super().__init__(name,x,y,z,angle,race,hull,size, fleet_number)
        self.abilities = abilities


    def spawn(self, sim):
        ret =  super().spawn(sim)
        obj = sim.get_space_object(self.id)
        ## TODO: Handle abilities
        """
            <set_special name="${name}" clear="${ability_clear.match(/warp/i)?'yes':''}" ability="Warp"/>
            <set_special name="${name}" clear="${ability_clear.match(/tractor/i)?'yes':''}" ability="Tractor"/>
            <set_special name="${name}" clear="${ability_clear.match(/teleport/i)?'yes':''}" ability="Teleport"/>
            <set_special name="${name}" clear="${ability_clear.match(/drones/i)?'yes':''}" ability="Drones"/>
            <set_special name="${name}" clear="${ability_clear.match(/het/i)?'yes':''}" ability="HET"/>
            <set_special name="${name}" clear="${ability_clear.match(/antimine/i)?'yes':''}"  ability="AntiMine"/>
            <set_special name="${name}" clear="${ability_clear.match(/antimine/i)?'yes':''}" ability="AntiTorp"/>
            <set_special name="${name}" clear="${ability_clear.match(/shlddrain/i)?'yes':''}" ability="ShldDrain"/>
            <set_special name="${name}" clear="${ability_clear.match(/shldvamp/i)?'yes':''}" ability="ShldVamp"/>
            <set_special name="${name}" clear="${ability_clear.match(/lowvis/i)?'yes':''}" ability="LowVis"/>
            <set_special name="${name}" clear="${ability_clear.match(/stealth/i)?'yes':''}" ability="Stealth"/>
            <set_special name="${name}" ship="-1" captain="5" ability="${ability_captain}"/>
        """

        return ret



""" 
Torgoth ships set the the ship and captain
"""
class TonnageTorgoth(TonnageObject):
    def __init__(self, name, x,y,z,angle, race,hull, size, fleet_number=-1, ship=-99, captain=-99):
        super().__init__(name,x,y,z,angle,race,hull,size, fleet_number)
        self.ship = ship
        self.captain = captain

    def spawn(self, sim):
        ret =  super().spawn(sim)
        obj = sim.get_space_object(self.id)
        ## SET Ship and captain
        return ret


# class PrimeState(Enum):
#         PrePrime = 1
#         Primed = 2

"""
Hunters are torgoth, but don't set ship, captain
and have extra behavior for beacons
"""
class TonnageHunter(TonnageObject):
    def __init__(self, name, x,y,z, timer):
        super().__init__(name,x,y,z,45,"Torgoth","Goliath","", fleet_number=-1)
        self.timer = timer
        self.timer_elapsed = 0
        self.beacon_id = 0
        #self.prime_state = PrimeState.PrePrime

    # Not sure what Prime means
    # and it seems to be done immediately
    # Which I thought it was something done later
    def prime(self,sim, obj):
        #  <set_object_property name="${name}" property="shieldMaxStateFront" value="20"/>
        #  <set_object_property name="${name}" property="shieldMaxStateBack" value="20"/>
        #  <set_object_property name="${name}" property="topSpeed" value="${0.35+_index*0.01}"/>
        pass

    # Hunters are worth less tonnage
    def score_points(self, sim, surrender):
        if surrender: 
            TonnageObject.tonnage += 20
        else:
            TonnageObject.tonnage += 40

    def redeploy_beacon(self, sim):
        self.timer_elapsed += sim.elapased #TODO: What is the elapsed time
        if self.timer_elapsed > self.timer:
            # Can't this just be moved?
            if self.beacon_id != 0:
                sim.destroy_space_object(self.beacon_id)
            self.beacon_id = sim.add_passive('anomaly', 'anomaly')
            # <create type="Anomaly" name="B${_index}" pickupType="8" beaconMonsterType="1" beaconEffect="0" x="3511.0" y="-321.0" z="6063.0"/>
            # <set_relative_position name2="B${_index}" name1="${name}" angle="0" distance="1000"/>
            
            self.timer_elapsed = 0

    def spawn(self, sim):
        ret =  super().spawn(sim)
        obj = sim.get_space_object(self.id)
        #  <set_ship_text name="${name}" race="Torgoth" class="Whale Hunter" desc="Licensed Professional Hunter of Whales"/>
        #  <add_ai name ="${name}" type ="CHASE_WHALE" value1="20000"/>
        #  <add_ai name ="${name}" type ="CHASE_ANGER" value1="20000"/>
        #  <set_special name="${name}" clear="yes" ability="Drones"/>
        #  <set_timer name="${name}_timer" seconds="${timer}"/>
        return ret

    def tick(self, sim):
        super().tick(sim)
        # self.redeploy_beacon(sim)