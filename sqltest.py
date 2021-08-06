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

create_new_sheet("Test author_name","Test Boy", cursor)
cursor.execute('Select * from charactersheet')
print(cursor.fetchall())

