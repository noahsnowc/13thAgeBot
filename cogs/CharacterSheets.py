"""Module containing support command for the main bot."""
import sqlite3
from discord.ext import commands

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

class DatabaseIO:
    """Class definition to contain all interactions with the SQLite3 database."""

    def __init__(self):
        self.bot_db = sqlite3.connect('data/discordbot.sql', isolation_level=None,
                                      detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.cursor = self.bot_db.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS charactersheet (
  character_name TEXT UNIQUE PRIMARY KEY,
  author_name TEXT,
  class TEXT,
  race TEXT,
  pclevel FLOAT,
  strength FLOAT,
  constitution FLOAT,
  dexterity FLOAT,
  wisdom FLOAT,
  charisma FLOAT,
  ac FLOAT,
  pd FLOAT,
  md FLOAT,
  hp_max FLOAT,
  hp_current FLOAT,
  recoveries_max FLOAT,
  recoveries_current FLOAT,
  oneut TEXT,
  racial_power BLOB,
  powers BLOB,
  spells BLOB,
  icon_relationships BLOB,
  backgrounds BLOB,
  talents BLOB,
  class_features BLOB,
  feats BLOB,
  equipment BLOB,
  gold BLOB,
  magic_items BLOB
)
''')
    
    def list_stat_names(self):
        table_info = self.cursor.execute("PRAGMA table_info(charactersheet)")
        only_columns = []
        print(table_info)
        for columns in self.cursor.fetchall():
            only_columns.append(columns[1])
        return only_columns

    def list_all_stat_values(self):
        self.cursor.execute("SELECT * FROM charactersheet")
        data = self.cursor.fetchall()
        print(data)
        return data 

    ##Need to switch this to character
    def list_all_author_stat_values(self, author_name):
        print(author_name)
        self.cursor.execute("SELECT * FROM charactersheet WHERE author_name=?", (author_name,))
        data = self.cursor.fetchall()
        print(data)
        return data

    def create_new_sheet(self, author_name, character_name):
        print(author_name)
        print(character_name)
        print("running Character Creation")
        self.cursor.execute('''INSERT INTO charactersheet(character_name,author_name) 
                                VALUES(?,?)
                                ''',(character_name,author_name))

        message = "Character Sheet created for " + character_name
        print(message)
        return message 

    def delete_character(self,author_name, character_name):
        self.cursor.execute('''DELETE FROM charactersheet 
                               WHERE character_name=? AND author_name=?''',
                            (character_name,author_name))
        message = character_name+" Deleted"
        return message

    def get_cs_value(self, author_name, character_name, *args):
        self.cursor.executeall('''SELECT ? FROM charactersheet 
                        WHERE author_name=? and character_name=?''', (args,author_name,character_name))
        cs_values = self.cursor.fetchall()
        return cs_values
    
    def set_cs_value(self, *args):
        self.cursor.execute()
        return "Value(s) addede"

charactersheet_db = DatabaseIO()
        
class Charactersheet_Commands(commands.Cog, name="Character Sheet Commands"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(case_insensitive=True, help="Character Sheet helper")
    async def cs(self, ctx):
        """Base init command group."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Additional arguments required, "
                           f"see **{ctx.prefix}help cs** for available options.")

    @cs.command(case_insensitive=True, help="creates a new character sheet for the current user")
    async def create_sheet(self, ctx, args):
            await ctx.send(charactersheet_db.create_new_sheet(ctx.message.author.id, args))
    
    @cs.command(case_insensitive=True, help="")
    async def delete_sheet(self, ctx, args):
        if args:
            await ctx.send("Send me a name. I NEED A NAME. LET ME DELETE.")
        else:
            await ctx.send(charactersheet_db.delete_character(ctx.message.author.id, args))

    #==========================================
    # Database/SQL Testing Below this point
    #==========================================       
    
   # @cs.command(case_insensitive=True, help="Players Ignore - - - List all current info headers of character")
    async def headers(self, ctx):
        await ctx.send(charactersheet_db.list_stat_names())
    
    @cs.command(case_insensitive=True, help="Players Ignore - - - ")
    async def all_stats(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(charactersheet_db.list_all_author_stat_values(ctx.message.author.id))
    @cs.command(case_insensitive=True, help="Players Ignore - - - ")
    async def db(self, ctx):
        await ctx.send(charactersheet_db.list_all_stat_values())
        
def setup(bot):
    """Discord module required setup for Cog loading."""
    bot.add_cog(Charactersheet_Commands(bot))