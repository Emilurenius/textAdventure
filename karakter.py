class character():
    def __init__(self, name, health, AC, intelligence, dexterity, strength):
        self.name = name
        self.health = 20 + health
        self.AC = 12 + AC
        self.intelligence = 10 + intelligence
        self.dexterity = 10 + dexterity
        self.strength = 10 + strength
orc = character("orc", 4, 2, -5, -4, 5)
elf = character("elf", -4, -2, 6, 4, -2)
human = character("human", 0, 0, 0, 0, 0)
troll = character("troll", 2, -2, 2, 6, 2)




