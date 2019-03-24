import sqlite3
import sys

def initialize(connection):
    c = connection.cursor()
    createColorsTable(c)
    connection.commit()

def createColorsTable(c):
    c.execute('''CREATE TABLE [colors] (
	    [id] integer primary key autoincrement,
    	red int,
	    green int,
	    blue int,
	    created real default current_timestamp,
        last_used real default current_timestamp
    )''')
    c.execute('''CREATE UNIQUE INDEX `colors_unique_rgb` ON `colors` (
	`red`,
	`green`,
	`blue`
    )''')

def updateColor(connection, red, green, blue):
    c = connection.cursor()
    try:
        c.execute('''INSERT INTO [colors] (red,green,blue) VALUES (?,?,?)''', (red,green,blue))
    except sqlite3.IntegrityError: 
        c.execute('''UPDATE [colors] SET last_used = current_timestamp WHERE red = ? AND green = ? AND blue = ?''', (red,green,blue))
                
    connection.commit()

def getUsedColors(connection):
    c = connection.cursor()
    c.execute('''SELECT red, green, blue FROM [colors] ORDER BY last_used DESC''')
    results = []
    for row in c:
        results.append([row[0],row[1],row[2]])

    return results

def getLastUsedColor(connection):
    c = connection.cursor()
    c.execute('SELECT red, green, blue FROM [colors] ORDER BY last_used DESC LIMIT 1')
    result = None
    for row in c:
        result = { 
            "red" : row[0],
            "green" : row[1],
            "blue" : row[2]
        }

    return result