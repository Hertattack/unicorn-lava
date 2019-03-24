#!/usr/bin/python3
import os
import sys
import sqlite3
from json import dumps

try:
    import unicornhathd as unicorn
    print("unicorn hat hd detected")
except ImportError:
    from unicorn_hat_sim import unicornhathd as unicorn

from bottle import route, run, template, static_file, request, response

DB_VERSION="1"

import db

options = {
    "port" : 8080,
    "wwwroot" : None,
    "host" : '0.0.0.0'
}

def getAbsolutePath(relativePath):
    return os.path.realpath(os.path.join(os.path.dirname(__file__),relativePath))

def initialize(options):
    options["wwwroot"] = getAbsolutePath("../wwwroot")
    options["port"] = int(sys.argv[1])  if len(sys.argv) == 2  else options["port"]
    
    options["databaseFile"] = getAbsolutePath('../lava-%s.db3' % (DB_VERSION))
    print("Using database: %s" % options["databaseFile"])

    if(os.path.isfile(options["databaseFile"]) == False):
        options["connection"] = sqlite3.connect(options["databaseFile"])
        print("Initializing New Database")
        db.initialize(options["connection"])
    else:
        options["connection"] = sqlite3.connect(options["databaseFile"])


def start(options):
    print("Server running on port: %d" % (options["port"]))
    lastColor = db.getLastUsedColor(options["connection"])
    if(lastColor != None):
        setHatColor(lastColor["red"], lastColor["green"], lastColor["blue"])
    run(host=options["host"], port=options["port"])

currentRed = '0'
currentBlue = '0'
currentGreen = '0'

def setHatColor(r, g, b):
    for x in range(0, 16):
        for y in range(0, 16):
            unicorn.set_pixel(x, y, r, g, b)
    
    unicorn.show()

@route('/js/<filename>')
def static_js(filename):
    return static_file(filename, root=os.path.join(options["wwwroot"],'js'))

@route('/css/<filename>')
def static_css(filename):
    return static_file(filename, root=os.path.join(options["wwwroot"],'css'))

@route('/index.html')
@route('/')
def index():
    return static_file('index.html', root=options["wwwroot"])

@route('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root=options["wwwroot"])

@route('/api/getUsedColors')
def getPreviousColors():
    colors = db.getUsedColors(options["connection"])
    response.status = 200
    response.content_type = 'application/json'
    return dumps(colors)

@route('/api/deleteColor', method="DELETE")
def deleteColor():
    currentRed = request.query.red or currentRed
    currentGreen = request.query.green or currentGreen
    currentBlue = request.query.blue or currentBlue

    intRed = int(currentRed)
    intGreen = int(currentGreen)
    intBlue = int(currentBlue)

    db.deleteUsedColor(options["connection"], intRed, intGreen, intBlue)

    response.status = 200

@route('/api/setColor')
def setColor():
    currentRed = request.query.red or currentRed
    currentGreen = request.query.green or currentGreen
    currentBlue = request.query.blue or currentBlue

    intRed = int(currentRed)
    intGreen = int(currentGreen)
    intBlue = int(currentBlue)

    if(intRed <= 255 and intGreen <= 255 and intBlue <= 255 and intRed >= 0 and intGreen >= 0 and intBlue >= 0):
        db.updateColor(options["connection"],intRed,intGreen,intBlue)
        setHatColor(intRed, intGreen, intBlue)
        response.status = 200
    else:
        response.status = 400
        
    return

@route('/api/getCurrentColor')
def getColor():
    return {
        "red" : currentRed,
        "green" : currentGreen,
        "blue" : currentBlue
    }

initialize(options)
start(options)