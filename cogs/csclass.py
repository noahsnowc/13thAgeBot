""" class CharacterSheet:
    def __init__(self):
        csdata = [
        self.author_name : "",
        self.character_name : "",
        self.cs_class : "",
        self.race : "",
        self.level : 0,
        self.strength : 0,
        self.constitution : 0,
        self.dexterity : 0,
        self. wisdom : 0,
        self.charisma : 0,
        self.ac : 0,
        self.pd : 0,
        self.md : 0,
        self.hp_max : 0,
        self.hp_current : 0,
        self.recoveries_current : 0,
        self.recoveries_max : 0,
        self.out : "",
        self.racial_power : "",
        self.powers : [],
        self.spells : [],
        self.icon_relationships : [],
        self.backgrounds : [],
        self.talents : [],
        self.class_features : [],
        self.feats : [],
        self.equipment : [],
        self.gold : [],
        self.magic_items : [],
        ]


    def get_info(self, info_tuple):
        for data in info_tuple:
            return self.csdata[data]

    def set_info(self, info_tuple):
        for data in info_tuple:
            self.csdata[data] = info_tuple[data]

    def roll_stat


cs_object = CharacterSheet() """ 
"""May or may not need the above"""
