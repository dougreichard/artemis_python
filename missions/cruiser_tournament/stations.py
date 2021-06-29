import sbs
from tonnage import TonnageObject, SpawnState

class Station:
    def __init__(self, name, station_type, x,z, bonus, 
        minutes, produce, need, want1, want2,nuke=0, homing=0, emp=0, mine=0, pshock = 0          

    ):
        self.name = name
        self.station_type = station_type
        self.x = x
        self.z = z
        self.bonus = bonus
        self.minutes= minutes
        self.produce= produce
        self.need = need
        self.want1 = want1
        self.want2 = want2
        self.nuke = nuke
        self.homing = homing
        self.emp = emp
        self.mine = mine
        self.pshock = pshock

        # Temp all are Starbase
        self.station_type = 'Starbase'

        self.state = SpawnState.NotSpawned

        
    def tick(self, sim):
        if self.state == SpawnState.Spawned:
            if not sim.space_object_exists(self.id):
                self.state = SpawnState.Destroyed
                TonnageObject.tonnage -= 90
                print(f'Total tonnage now: {TonnageObject.tonnage}')
                # <big_message title="${race} ${hull} ${name} destroyed" OR SURRENDER
                #       subtitle1="${_.int(weight) <0?'Penalty ':''}${weight} kilotons" subtitle2=""/>
                # <log text="${race} ${hull} ${name} destroyed"/>

                # <set_object_property property="topSpeed" value="0.2" name="${name}"/>
                # <big_message title="${race} ${hull} surrendered" subtitle1="${weight} kilotons" subtitle2="+${surrender} kt surrender bonus"/>
                # <log text="${race} ${hull} ${name} Surrendered"/>

  
    def spawn(self, sim):
        self.id = sim.make_new_active('behav_station', self.station_type)
        obj = sim.get_space_object(self.id)
        sim.reposition_space_object(obj, self.x,0,self.z)
        print(f"Spawned {self.id}:{self.name} at:{obj.pos.x},:{obj.pos.y},:{obj.pos.z}")
        self.state = SpawnState.Spawned
        #TODO: 
        #TODO: Do all the other stuff
    #     <clear_player_station_carried name="${name}"/>
    #   <set_player_station_carried name="${name}" singleSeatName="Pilgrim" raceKeys="TSN player" hullKeys="singleseat shuttle"/>
    #   <create type="station" x="${x}" y="0.0" z="${z}" angle="0" name="${name}" raceKeys="Terran friendly" hullKeys="${type} Base"/>
    #   <set_object_property property="missileStoresNuke" value="${nuke}" name="${name}"/>
    #   <set_object_property property="missileStoresHoming" value="${homing}" name="${name}"/>
    #   <set_object_property property="missileStoresEMP" value="${EMP}" name="${name}"/>
    #   <set_object_property property="missileStoresMine" value="${mine}" name="${name}"/>
    #   <set_object_property property="missileStoresPshock" value="${Pshock}" name="${name}"/>
        

class Stations:
    stations = [
        Station("DS1", "Science", 69500, 69000, "Vigoranium"
        , 47, "Xiridium", "Platinum", "Salistra", "Augite"
        , 0, 7, 0, 1, 2),
        Station("DS2", "Civilian", 44000, 71000, "High Density Power Cells"
        , 46, "Salistra", "Xiridium", "Platinum", "Augite"
        , 1, 10, 0, 1, 2), 
        Station("DS3", "Science", 76000, 95000, "Carapaction Coils"
        , 45, "Augite", "Salistra", "Xiridium", "Platinum"
        , 0, 27, 0, 1, 2),
        Station("DS4", "Civilian", 33600, 92500, "Tauron Focusers"
        , 44, "Platinum", "Augite", "Xiridium", "Salistra"
        , 0, 27, 0, 1, 2)
    ]

    def spawn(self, sim):
        for station in self.stations:
            station.spawn(sim)
        #<set_comms_button text="Request Cargo Report" sideValue="2" player_slot="0"/>
  
        #   <!-- Hints from Bases -->
        #   <repeat _range="stations">
        #     <event name="${name} Hint">
        #       <if_variable name="${name}_hint" comparator="EQUALS" value="0"/>
        #       <if_docked name="${name}"/>
        #       <incoming_comms_text from="${name}" type="STATION">
        #   Bonus available! If you collect all ${bonus} Nodules a bonus enemy fleet will attack. You can score extra tonnage by destroying it.
        #       </incoming_comms_text>
        #       <set_variable name="${name}_hint" value="1"/>
        #     </event>
        
        #     <event name="Instructions from ${name}">
        #       <if_variable name="Minutes" comparator="EQUALS" value="${minutes}"/>
        #       <if_variable name="Message" comparator="EQUALS" value="${_index}"/>
        #       <incoming_comms_text from="${name}" type="STATION">
        #     Our base can produces ${produce}. We need ${need} to make Nukes. If you send us ${want1} or ${want2} we can make EMP torpedoes.
        #       </incoming_comms_text>
        #       <set_variable name="Message" value="${_index+1}"/>
        #     </event>
            
        #   </repeat>

        #   <event name="Instructions from Scorekeeper">
        #     <if_comms_button text="Request Cargo Report"/>
        #     <repeat _range="stations">
        #       <incoming_comms_text from="Scorekeeper" type="ALERT">
        #       ${name} makes ${produce} and prefers ${need}
        #       </incoming_comms_text>
        #     </repeat>
        #     <incoming_comms_text from="Scorekeeper" type="ALERT">
        #       Any base will accept any cargo it doesn't produce.
        #     </incoming_comms_text>
        #   </event>
        # </mission_data>