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

def get_value(cursor, author_name, arg) :
        print(author_name)
        print(arg)
        query = 'SELECT '+arg+' from charactersheet WHERE active = true AND author_name=?'
        cursor.execute(query,(author_name,))
        print(cursor.fetchall())

def update_character(cursor, character_name, *args):
        for arg in args:
                print("What would you like to update "+arg+" to?")
                input1 = input()
                cursor.execute('UPDATE charactersheet SET class = ? where character_name=?',(input1, character_name))
        db.commit()
        print("Updated Database")
        

cursor.execute('Select class from charactersheet where character_name=?', ("Bob",))
print(cursor.fetchall())
#print(cursor.fetchall())
#get_value(cursor, "Bob", 'class', 'race')]
get_value(cursor, "Bob", 'class')
cursor.execute('Select * from charactersheet')
print(cursor.fetchall())

#THis all seems so fucked, willl look again in morning
