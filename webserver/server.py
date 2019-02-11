#!/usr/bin/python3
import os
import sys

try:
    import unicornhathd as unicorn
    print("unicorn hat hd detected")
except ImportError:
    from unicorn_hat_sim import unicornhathd as unicorn

from bottle import route, run, template, static_file, request, response

wwwroot = os.path.realpath(os.path.join(os.path.dirname(__file__),"../wwwroot"))

port = int(sys.argv[1])  if len(sys.argv) == 2  else 8080

print("Server running on port: %d" % (port))

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
    return static_file(filename, root=os.path.join(wwwroot,'js'))

@route('/css/<filename>')
def static_css(filename):
    return static_file(filename, root=os.path.join(wwwroot,'css'))

@route('/index.html')
@route('/')
def index():
    return static_file('index.html', root=wwwroot)

@route('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root=wwwroot)

@route('/api/setColor')
def setColor():
    currentRed = request.query.red or currentRed
    currentGreen = request.query.green or currentGreen
    currentBlue = request.query.blue or currentBlue

    setHatColor(int(currentRed), int(currentGreen),int(currentBlue))

    response.status = 200

    return

@route('/api/getCurrentColor')
def getColor():
    return {
        red : currentRed,
        green : currentGreen,
        blue : currentBlue
    }

run(host='0.0.0.0', port=port)