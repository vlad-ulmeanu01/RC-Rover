import socket
from time import *
from sense_hat import SenseHat

sense = SenseHat ()

def get_ind () :
    bval = bx = by = bz = 0
    b = 0

    bval = sense.get_compass_raw ()
    bx = bval["x"]
    by = bval["y"]
    bz = bval["z"]
    b = ( bx * bx + by * by + bz * bz ) ** 0.5

    return int ( b * 100 ) / 100

z1 = z2 = 0

def get_mvt () :
    global z1, z2

    ot = sense.get_accelerometer_raw ()
    z2 = ot["z"]
    dif = z2 - z1
    z1 = z2

    if dif < 0 :
        dif = 0

    return int ( dif * 100 ) / 100

def addzero ( sg ) :
    sz = len ( sg )
    ct = 0
    for i in range ( 1, sz ) :
        if sg[i-1] == '!' and sg[i] == '.' :
            ct += 1

    if ct == 0 :
        return sg
    else :
        rep = [ 0 for i in range ( 0, sz + ct ) ]
        j = 0
        for i in range ( 1, sz ) :
            if sq[i-1] == '!' and sq[i] == '.' :
                rep[j] = '0'
                j += 1
            rep[j] = sq[i]
            j += 1

        return rep
    
host = "192.168.100.8"
port = 5560
bfsz = 1024

s = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
s.connect ( ( host, port ) )

print ( "connected to remote" )
tstart = tloop = time ()
mxmvt = 0

flag = 0
while flag == 0 :
    mvt = get_mvt ()
    if mvt > mxmvt :
        mxmvt = mvt
        
    if tloop - tstart >= 0.5 :  
        tstart = tloop

        hmd = int ( sense.get_humidity () * 100 ) / 100
        tmp = int ( sense.get_temperature () * 100 ) / 100
        prs = int ( sense.get_pressure () * 100 ) / 100
        ind = get_ind ()
        message = str ( hmd ) + '!' + str ( tmp ) + '!' + str ( prs ) + '!' + str ( mxmvt ) + '!' + str ( ind ) + '!'

        s.send ( str.encode ( message ) )
        print ( "packet sent :", message )
        mxmvt = 0
        
    tloop = time ()

s.close ()
