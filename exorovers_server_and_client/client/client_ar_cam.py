from struct import pack
from PIL import Image
import socket
from picamera import PiCamera
from time import sleep

def sendimg ( s, name ) :
    bfsz = 2048
    im = Image.open ( name )
    im = im.convert ( "RGB" )
    data = im.load ()
    string = ""

    cl, ln = im.size

    for x in range ( 0, cl ) :
        for y in range ( 0, ln ) :
            r, g, b = data[ x, y ]
            string += str ( r ) + '!' + str ( g ) + '!' + str ( b ) + '!'

    lg = pack ( '>Q', len ( string ) )
    s.send ( lg )
    string = str.encode ( string )
    s.send ( string )

    message = s.recv ( bfsz )
    
camera = PiCamera ()
camera.resolution = ( 160, 120 )

host = "192.168.1.109"
port = 5560

s = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
s.connect ( ( host, port ) )

cyc = 0
while 1 :
    name = "pic" + str ( cyc ) + ".png"
    camera.capture ( name )
    sendimg ( s, name )
    print ( "ended cycle", cyc )
    cyc += 1

im.close ()
s.close ()
