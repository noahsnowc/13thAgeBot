import sqlite3
db = sqlite3.connect("./data/discordbot.sql")
cursor = db.cursor()

def create_new_sheet(author_name, character_name, cursor):
        print(author_name)
        print(character_name)
        print("running Character Creation")
        cursor.execute('''INSERT INTO charactersheet(character_name,author_name) 
                                VALUES(?,?)
                                ''',[character_name, author_name])

        cursor.execute('Select * from charactersheet where character_name=?',[character_name])
        print("Database Updated")
        print(cursor.fetchall())

def get_value(cursor, character_name, *args) :
        print(character_name)
        print(args)
        for arg in args:
                cursor.execute('SELECT ? from charactersheet where character_name=?',(arg, character_name))
        print(cursor.fetchall())

def update_character(cursor, character_name, *args):
        for arg in args:
                print("What would you like to update "+arg+" to?")
                input1 = input()
                cursor.execute('UPDATE charactersheet SET class = ? where character_name=?',(input1, character_name))
        db.commit()
        print("Updated Database")
        

cursor.execute('Select race from charactersheet where character_name=?', ("Bob",))
print(cursor.fetchall())
#print(cursor.fetchall())
#get_value(cursor, "Bob", 'class', 'race')
#update_character(cursor, "Bob", 'class', 'race')
#get_value(cursor, "Bob", 'class', 'race')

THis all seems so fucked, willl look again in morning
