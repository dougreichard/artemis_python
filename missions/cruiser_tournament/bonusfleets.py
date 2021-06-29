from tonnage import SpawnState, TonnageObject, TonnageSkaraan


class Trigger:
    def __init__(self, name, pickup_type, x, z):
        self.name = name
        self.type = pickup_type
        self.x = x
        self.z = z
        self.state = SpawnState.NotSpawned

    def spawn(self, sim):
        #TODO: Make Anomaly
        self.id = sim.make_new_passive("behav_asteroid, ", "Asteroid 1") 
        obj = sim.get_space_object(self.id)
        sim.reposition_space_object(obj, self.x, 0,self.z)
        self.state = SpawnState.Spawned
        #TODO: object.pickupType
        #TODO: Set name

    def tick(self, sim):
        if self.state == SpawnState.Spawned:
            if not sim.space_object_exists(self.id):
                self.state = SpawnState.Destroyed


class Fleet:
    def __init__(self, name, number, collect, triggers, enemies):
        self.name = name
        self.number = number
        self.collect = collect
        self.triggers = triggers
        self.enemies = enemies

        self.state = SpawnState.NotSpawned

    def start(self, sim):
        for anom in self.triggers:
            anom.spawn(sim)
        # set fleet number
        for enemy in self.enemies:
            enemy.fleet_number = self.number

    def tick(self, sim):
        # if fleet not spawned, check for spawn
        if self.state == SpawnState.NotSpawned:
            count = 0
            for trigger in self.triggers:
                trigger.tick(sim)
                # count the destoried triggers
                if trigger.state == SpawnState.Destroyed:
                    count+= 1
            if count == len(self.triggers):
                for enemy in self.enemies:
                    enemy.spawn(sim)
                self.state = SpawnState.Spawned
                print(f'Bonus fleet spawned {self.name}')
                """
                TODO:
                <incoming_comms_text from = "Enemy Fleet" >
                Congratulations, Artemis. You collected all of the ${collect}. We are sending a bonus fleet for you to fight.
                </incoming_comms_text>
                """
                    
        elif self.state == SpawnState.Spawned:
            count = 0
            for enemy in self.enemies:
                enemy.tick(sim)
                # count the destoried triggers
                if enemy.state == SpawnState.Destroyed:
                    count+= 1
            if count == len(self.enemies):
                self.state = SpawnState.Destroyed


class BonusFleets:
    fleets = [
        Fleet("Bonus_0", 90, "High Density Power Cells",
              [
                  Trigger("01", 0, 32511.0, 65063.0),
                  Trigger("02", 0, 30469.0, 46936.0),
                  Trigger("03", 0, 36341.0, 28936.0),
                  Trigger("04", 0, 29064.0, 21659.0),
                  Trigger("05", 0, 50766.0, 91617.0),
                  Trigger("06", 0, 53958.0, 83702.0),
                  Trigger("07", 0, 58681.0, 77574.0),
                  Trigger("08", 0, 56256.0, 56255.0),
              ],
              [
                  TonnageSkaraan("B01", 26000, 0,    32000, 200, "Skaraan", "Executor",     "large",
                                abilities ={'ability_captain': "Warp", 'ability_clear': "HET,LowVis,Stealth"}),
                  TonnageObject("B02", 26140, -200, 31800, 200,
                                "Torgoth", "Behemoth",     "large"),
                  TonnageObject("B03", 26960, -200, 33200, 200,
                                "Kralien", "Dreadnaught",  "large"),
                  TonnageObject("B04", 26540, 200,  32300, 200,
                                "Kralien", "Battleship",    "medium"),
                  TonnageObject("B05", 26640, 200,  34300, 200,
                                "Kralien", "Cruiser",      "small"),
                  TonnageObject("B06", 26740, -200, 34400, 200,
                                "Kralien", "Cruiser",      "small"),
                  TonnageObject("B07", 26040, 200,  31700, 200,
                                "Arvonian", "Carrier",     "Carrier"),
                  TonnageObject("B08", 26540, -200, 31250, 200,
                                "Kralien", "Battleship",   "medium"),
              ]),
        Fleet("Bonus_1", 91, "Cetrocite Crystals",
              [Trigger("11", 1, 67362.0, 65574.0),
               Trigger("12", 1, 65192.0, 57276.0),
               Trigger("13", 1, 62383.0, 48340.0),
               Trigger("14", 1, 67362.0, 41829.0),
               Trigger("15", 1, 68894.0, 29957.0),
               Trigger("16", 1, 70426.0, 24212.0),
               Trigger("17", 1, 7042.0, 14212.0),
               ],
              [
                  TonnageSkaraan("B11", 66000, 0,   31000, 200, "Skaraan", "Executor", "large", 
                        abilities ={'ability_captain': "Warp", 'ability_clear': "Cloak,Teleport,HET,AnitiMine,shlddrain,shldvamp,LowVis,Stealth"}),
                  TonnageObject("B12", 66140, -200, 30800, 200,
                                "Torgoth", "Behemoth", "large"),
                  TonnageObject("B13", 66960, -200, 32200, 200,
                                "Kralien", "Dreadnought", "large"),
                  TonnageObject("B14", 66540, 200, 31300, 200,
                                "Kralien", "Battleship", "medium"),
                  TonnageObject("B15", 66640, 200, 33300, 200,
                                "Kralien", "Cruiser", "small"),
                  TonnageObject("B16", 66740, 200, 33400, 200,
                                "Kralien", "Cruiser", "small"),
                  TonnageObject("B17", 66040, 200, 30700, 200,
                                "Arvonian", "Carrier", "Carrier"),
                  TonnageObject("B18", 66540, -200, 30250, 200,
                                "Kralien", "Battleship", "medium"),
              ]),
        Fleet("Bonus_2", 92, "Cetrocite Crystals",
              [Trigger("21", 2, 88426.0, 88212.0),
               Trigger("22", 2, 10426.0, 84212.0),
               Trigger("23", 2, 87426.0, 7212.0),
               Trigger("24", 2, 48326.0, 42128.0),
               Trigger("25", 2, 50461.0, 25295.0),
               Trigger("26", 2, 84026.0, 28126.0),
               ],
              [
                  TonnageSkaraan("B21", 75000, 0,   31000, 200, "Skaraan", "Executor", "large", 
                        abilities ={'ability_captain': "Warp", 'ability_clear': "Cloak,Teleport,HET,AnitiMine,shlddrain,shldvamp,LowVis,Stealth"}),
                  TonnageObject("B22", 75140, -200, 30800, 200,
                                "Torgoth", "Behemoth", "large"),
                  TonnageObject("B23", 74960, -200, 32200, 200,
                                "Kralien", "Dreadnought", "large"),
                  TonnageObject("B24", 75240, 200, 31300, 200,
                                "Kralien", "Battleship", "medium"),
                  TonnageObject("B25", 75540, 200, 33333, 200,
                                "Kralien", "Cruiser", "small"),
                  TonnageObject("B26", 75040, -200, 33300, 200,
                                "Kralien", "Cruiser", "small"),
                  TonnageObject("B27", 75240, 200, 30600, 200,
                                "Arvonian", "Carrier", "Carrier"),
              ]),
        Fleet("Bonus_3", 93, "Lateral Arrays",
              [Trigger("31", 3, 90465.0, 84212.0),
               Trigger("32", 3, 86526.0, 7212.0),
               Trigger("33", 3, 68326.0, 42128.0),
               Trigger("34", 3, 92431.0, 52229.0),
               Trigger("35", 3, 9461.0, 25292.0),
               ],
              [
                  TonnageSkaraan("B31", 44000, 0,   30000, 200, "Skaraan", "Enforcer", "medium", 
                        abilities = {'ability_captain': "Cloak", 'ability_clear': "Warp,Teleport,HET,AnitiMine,shlddrain,shldvamp,LowVis,Stealth"}),
                  TonnageObject("B32", 44140, -200, 29800, 200,
                                "Torgoth", "Leviathan", "medium"),
                  TonnageObject("B33", 43960, -200, 31200, 200,
                                "Kralien", "Dreadnought", "large"),
                  TonnageObject("B34", 44133, 200, 30300, 200,
                                "Kralien", "Battleship", "medium"),
                  TonnageObject("B35", 44444, 200, 32300, 200,
                                "Kralien", "Cruiser", "small"),
                  TonnageObject("B36", 43540, 200, 32430, 200,
                                "Kralien", "Cruiser", "small"),
                  TonnageObject("B37", 44240, -200, 29600, 200,
                                "Arvonian", "Carrier", "Carrier"),
              ]),
        Fleet("Bonus_4", 94, "Tauron Focusers",
              [Trigger("41", 4, 10260.0, 84212.0),
               Trigger("42", 4, 88967.0, 7942.0),
               Trigger("43", 4, 78429.0, 79128.0),
               Trigger("44", 4, 44461.0, 42829.0),

               ],
              [
                  TonnageSkaraan("B41", 65000, 0,   31000, 200, "Skaraan", "Enforcer", "medium",
                        abilities = {'ability_captain': "Cloak",
                                 'ability_clear': "Warp,Teleport,HET,AnitiMine,AntiTorp,shlddrain,shldvamp,LowVis,Stealth"}),
                  TonnageObject("B42", 65140, -200, 30800, 200,
                                "Torgoth", "Leviathan", "medium"),
                  TonnageObject("B43", 64960, -200, 32200, 200,
                                "Kralien", "Dreadnought", "large"),
                  TonnageObject("B44", 65440, 200, 31300, 200,
                                "Kralien", "Battleship", "medium"),
                  TonnageObject("B45", 65540, -200, 33000, 200,
                                "Kralien", "Cruiser", "small"),
                  TonnageObject("B46", 65340, 200, 33300, 200,
                                "Kralien", "Cruiser", "small"),
                  TonnageObject("B47", 65340, 200, 30600, 200,
                                "Arvonian", "Carrier", "Carrier"),
              ]),
        Fleet("Bonus_5", 95, "Infusion P-Coils",
              [Trigger("51", 5, 68265.0, 80210.0),
               Trigger("52", 5, 10426.0, 89228.0),
               Trigger("53", 5, 77426.0, 7212.0)
               ],

              [
                  TonnageSkaraan("B51", 65000, 0,   31000, 200, "Skaraan", "Enforcer", "medium", 
                      abilities = {'ability_captain': "Cloak", 'ability_clear': "Warp,Teleport,HET,AnitiMine,AntiTorp,shlddrain,shldvamp,LowVis,Stealth"}),
                  TonnageObject("B52", 65140, -200, 30800, 200,
                                "Torgoth", "Leviathan", "medium"),
                  TonnageObject("B53", 64960, -200, 32200, 200,
                                "Kralien", "Dreadnought", "large"),
                  TonnageObject("B54", 65540, 200, 31300, 200,
                                "Kralien", "Battleship", "medium"),
                  TonnageObject("B55", 65440, -200, 33000, 200,
                                "Kralien", "Cruiser", "small"),
                  TonnageObject("B56", 65340, 200, 33300, 200,
                                "Kralien", "Cruiser", "small"),
                  TonnageObject("B57", 65340, 200, 30600, 200,
                                "Arvonian", "Light Carrier", "large"),
              ]),
        Fleet("Bonus_6", 96, "Carapaction Coils",
              [Trigger("61", 6, 48271.0, 33120.0),
               Trigger("62", 6, 80612.0, 72893.0),
               ],
              [
                  TonnageSkaraan("B61", 75000, 0,   41000, 200, "Skaraan", "Enforcer", "medium", 
                      abilities = {'ability_captain': "Teleport", 'ability_clear': "Cloak,Warp,Tractor,Drones,HET,AnitiMine,AntiTorp,shlddrain,shldvamp,LowVis,Stealth"}),
                  TonnageObject("B62", 75140, -200, 40800, 200,
                                "Torgoth", "Leviathan", "medium"),
                  TonnageObject("B63", 74960, -200, 42200, 200,
                                "Kralien", "Dreadnought", "large"),
                  TonnageObject("B64", 75540, 200, 43100, 200,
                                "Kralien", "Battleship", "medium"),
                  TonnageObject("B65", 75440, 200, 43700, 200,
                                "Kralien", "Cruiser", "small"),
                  TonnageObject("B66", 75340, 200, 43300, 200,
                                "Kralien", "Cruiser", "small")
              ]),
        Fleet("Bonus_7", 97, "Secret Code Case",
              [Trigger("71", 7, 50461.0, 2954.0)],
              [
                  TonnageSkaraan("B71", 5000, 0, 41000, 200, "Skaraan", "Executor", "large",
                            abilities = {"ability_captain": "AniTorp", "ability_clear": "Teleport,shlddrain,LowVis,Stealth"}),
                  TonnageObject("B72", 5140, -200, 40800, 200,
                                "Torgoth", "Leviathan", "medium"),
                  TonnageObject("B73", 4960, -200, 42200, 200,
                                "Kralien", "Dreadnought", "large"),
                  TonnageObject("B74", 5540, 200, 43300, 200,
                                "Kralien", "Battleship", "medium"),
                  TonnageObject("B75", 5440, 200, 43500, 200,
                                "Kralien", "Cruiser", "small"),
                  TonnageObject("B76", 5340, 200, 42300, 200,
                                "Kralien", "Cruiser", "small"),
              ])]

    def start(self, sim):
        for fleet in self.fleets:
            fleet.start(sim)

    def tick(self, sim):
        for fleet in self.fleets:
            fleet.tick(sim)
        # NOTE: If state of fleet is destroyed it could get removed
