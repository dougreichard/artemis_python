from tonnage import TonnageObject, TonnageSkaraan, TonnageTorgoth
from whales import Whales


class Period:
    def __init__(self, enemies):
        self.enemies = enemies


class Periods:
    periods = [
        Period([
            TonnageObject("Black Comet", 99990.0, -10.0, 10.0, 0,
                          "Pirate", "Strongbow", "", -1),
            TonnageObject("D12", 16500, -350, 41100, 270, "Arvonian",
                          "Light Carrier", "carrier", 32),
            TonnageObject("R13", 13000, 450, 40500, 245,
                          "Torgoth", "Goliath", "small", 33),
            TonnageSkaraan("N14", 51000, -80, 31100, 200, "Skaraan", "Defiler", "small", 34, abilities={
                'ability_captain': "AntiTorp", 'ability_clear': "Cloak,Tractor,Teleport,Drones,AnitiMine,shlddrain,shldvamp,LowVis,Stealth"})
        ]),
        Period([
            TonnageObject("D16", 16500, -500, 41000, 270,
                          "Arvonian", "Carrier", "carrier", 36),
            TonnageObject("R17", 13000, 500, 40500, 245,
                          "Torgoth", "Leviathan", "medium", 37),
            TonnageSkaraan("N18", 51000, 0, 31000, 200, "Skaraan", "Enforcer", "medium", 38, abilities={
                'ability_captain': "AntiTorp", 'ability_clear': "Teleport,AnitiMine,shlddrain,shldvamp,LowVis,Stealth"}),
        ]),
        Period([
            TonnageObject("D20", 16500, -500, 71000, 270,
                          "Arvonian", "Carrier", "carrier", 40),
            TonnageObject("R21", 13000, 500, 30500, 245,
                          "Torgoth", "Behemoth", "large", 41),
            TonnageObject("R22", 13500, -500, 30000, 245,
                          "Torgoth", "Leviathan", "medium", 41),
            TonnageSkaraan("N22", 51000, 0, 21000, 200, "Skaraan", "Executor", "large", 42, abilities={
                'ability_captain': "AntiTorp", 'ability_clear': "AnitiMine,shlddrain,LowVis,Stealth"}),
        ]),
        Period([
            TonnageObject("D25", 86500, -500, 31000, 270,
                          "Arvonian", "Carrier", "carrier", 43),
            TonnageObject("D26", 86700, 500, 31900, 270,
                          "Arvonian", "Carrier", "carrier", 43),
            TonnageObject("R27", 13000, 500, 40500, 245,
                          "Torgoth", "Behemoth", "large", 44),
            TonnageObject("R28", 12600, -500, 40600, 245,
                          "Torgoth", "Behemoth", "large", 44),
            TonnageSkaraan("N29", 51000, 0, 31000, 200, "Skaraan", "Executor", "large", 46, abilities={
                'ability_captain': "AntiTorp", 'ability_clear': "AnitiMine,shlddrain,LowVis,Stealth"}),
            TonnageSkaraan("N30", 51400, -200, 30800, 200, "Skaraan", "Executor", "large", 46,
                           abilities={'ability_captain': "AntiTorp", 'ability_clear': "shlddrain,LowVis,Stealth"}),

        ]),
        Period([
            TonnageObject("Skywayman", 99990.0, -100.0, 10.0, 0,
                          "Pirate", "Strongbow", " ", -1),
            TonnageObject("D33", 16500, -500, 41000, 270,
                          "Arvonian", "Carrier", "carrier", 50),
            TonnageObject("D34", 16700, 500, 41900, 270,
                          "Arvonian", "Carrier", "carrier", 50),
            TonnageObject("R35", 88000, 500, 40500, 245,
                          "Torgoth", "Behemoth", "large", 52),
            TonnageObject("R36", 88600, -500, 40600, 245,
                          "Torgoth", "Behemoth", "large", 52),
            TonnageSkaraan("N37", 51000, 0, 61000, 200, "Skaraan", "Executor", "large", 54, abilities={
                'ability_captain': "AntiTorp", 'ability_clear': "shlddrain,LowVis,Stealth"}),
            TonnageSkaraan("N38", 51400, -200, 60800, 200, "Skaraan", "Executor", "large", 54,
                           abilities={'ability_captain': "AntiTorp", 'ability_clear': "shlddrain,LowVis,Stealth"}),
        ])
    ]
    whales = Whales()

    def start(self, sim):
        # eight minutes timer
        self.timer_end = 480
        self.elapsed = 0
        self.period = 0
        self.whales.start(sim)
    
    def period_spawn(self, sim):
        if self.period < len(self.periods):
            for enemy in self.periods[self.period]:
                enemy.spawn(sim)

    def next_period(self,sim):
        # Check for end of period
        if self.elapsed > self.timer_end:
            bonus = self.whales.bonus(sim)
            TonnageObject.tonnage += bonus
            #TODO:  <big_message title="End of First Period" subtitle1="Now spawning more enemies." subtitle2="Whale Bonus = |Bonus|"/>
            # <log text="End of ${name}. Whale Bonus = |Bonus|"/>
            # <log text="Score = |Tonnage| kt  |Minutes| minutes remaining."/>
            
    def start_end_game(self, sim):
        # <big_message title="END OF FINAL PERIOD" subtitle1="Congratulations" subtitle2="Whale Bonus = |Bonus|"/>
        # <set_timer name="endint_timer" seconds="8"/>
        # <log text="End of Sixth Period. Whale Bonus = |Bonus|"/>
        # <log text="Final Score = |Tonnage| kilotons."/>
        # <play_sound_now filename="Fanfare.wav"/>
        pass

    def end_game(self,sim):
        pass

    def tick(self, sim):
        # TODO: Check the timer logic
        # now assumes tick every 2 seconds
        self.elapsed += 2
        if self.elapsed > self.timer_end:
            if self.period < len(self.periods):
                self.next_period(sim)
            elif self.period == len(self.periods):
                self.start_end_game(sim)
                self.timer_end = 8
                self.period = -1
            elif self.period == -1:
                # Game is over
                self.end_game(sim)
                return
            self.elapsed = 0
            self.period += 1




