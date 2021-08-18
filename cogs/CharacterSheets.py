"""Module containing support command for the main bot."""
from os import stat
import sqlite3
from discord.ext import commands


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
  magic_items BLOB,
  active boolean DEFAULT FALSE
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

    def get_cs_value(self, author_name, arg):
        query = 'SELECT '+arg+' FROM charactersheet WHERE author_name=? and active=TRUE'
        self.cursor.execute(query, (author_name,)) 
        cs_values = self.cursor.fetchall()
        return cs_values
    
    def set_cs_value(self, author_name, character_name, *args):
        for arg in args:
            string_arg = str(arg)
            query = 'UPDATE '+string_arg+' FROM charactersheet WHERE author_name=? AND character_names=?'
        self.cursor.executeall(query, (author_name, character_name))
        return "Value(s) added"

    def activate_sheet(self, author_name, character_name):
        self.cursor.execute('Select character_name from charactersheet')
        if (any(character_name in i for i in self.cursor.fetchall())):
            self.cursor.execute('UPDATE charactersheet SET active= True where character_name=? and author_name=?',(character_name,author_name))
            return '{} has been set to active.'.format(character_name)
        else:
            return 'Character Sheet not found.'
    #==========================================

charactersheet_db = DatabaseIO()


##############################################################################
#Database Commands
##############################################################################

## Refactor these to use ACTIVATED character rather than supply character name
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
        if not args:
            await ctx.send("Send me a name. I NEED A NAME. LET ME DELETE.")
        else:
            await ctx.send(charactersheet_db.delete_character(ctx.message.author.id, args))

    @cs.group(case_insensitive=True, help="Various stat related commands")
    async def stats(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Additional arguments required, "
                           f"see **{ctx.prefix}help cs** for available options.")

    @cs.command(case_insensitive=True, help="")
    async def statnames(self,ctx):
        await ctx.send(charactersheet_db.list_stat_names())

    @stats.command(case_insensitive=True, help="Sets the supplied stats to the provided value.")
    async def set(self, ctx, args):
        def check(args):
                return args.author == ctx.author and args.channel == ctx.channel
        for arg in args:
            await ctx.send("What would you like to set {} to?".format(arg))
            response = await ctx.await_for('response', check=check)
            print(response)
            #await charactersheet_db.set_cs_value(ctx.message.author.id,"Bob",)

    #stat command update
    @stats.command(case_insensitive=True, help="Gets the supplied stats for the provided value")
    async def get(self, ctx, args):
        for arg in args:
            csdata = [tupleA[0] for tupleA in charactersheet_db.get_cs_value(ctx.message.author.id, arg)]
            response = "{}: {}".format(arg,csdata[0])
            await ctx.send(response)
    
    @cs.command(case_insensitive=True, help="Activates a Character sheet for use.")
    async def activate(self, ctx, namearg):
        await ctx.send(charactersheet_db.activate_sheet(ctx.message.author.id, namearg))
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