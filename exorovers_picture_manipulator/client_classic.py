import socket
import serial
from time import *
from sense_hat import SenseHat
import pygame
from pygame.locals import *
from PIL import Image
from picamera import PiCamera

sense = SenseHat ()
camera = PiCamera ()
pygame.init()

def MIN (a, b) :
    if (a < b) :
        return a
    else :
        return b

def MAX (a, b) :
    return a + b - MIN (a, b)

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

def ar_iscf ( ch ) :
    return ch >= '0' and ch <= '9'

i = 0
def ar_getnum ( s, i ) :
    sz = len ( s )

    while i < sz and ar_iscf ( s[i] ) == False :
        i += 1

    nr = 0
    while i < sz and ar_iscf ( s[i] ) == True :
        nr = nr * 10 + int ( s[i] )
        i += 1

    p10 = 1
    if i < sz and s[i] == '.' :
        i += 1
        while i < sz and ar_iscf ( s[i] ) == True :
            nr = nr * 10 + int ( s[i] )
            p10 *= 10
            i += 1

    if p10 == 1 :
        return ( nr, i )
    else :
        return ( float ( nr / p10 ), i )

def ar_getdata ( ser ) :
    i = 0
    read_serial = ser.readline ()
    s = ser.readline ()
    s = s.decode ( "utf-8" )

    nh4, i = ar_getnum ( s, i )
    co2, i = ar_getnum ( s, i )
    dist, i = ar_getnum ( s, i )
    print ( nh4, co2, dist )

    return ( nh4, co2, dist )

def processpic (k) :
    path = "photos/p" + str (k) + ".jpg"
    im = Image.open (path)
    im = im.convert ("RGB")
    pix = im.load ()

    for i in range ( 0, dimx ) :
        for j in range ( 0, dimy ) :
            r, g, b = pix[i,j]
            avg = 2/3 * r/255 + 1/6 * g/255 + 1/6 * b/255
            x = 5
            y = int ( (40-tmp) * thold/2 )
            y = MIN (MAX (y, 0), spcy-1)
            y = y * pc_tmp + int ((1-avg) * spcy) * (1- pc_tmp)
            if avg > 0.5 :
                y = MAX (y - thold * (avg - 0.5) * 2, 0)
            else :
                y = MIN (y + thold * (0.5 - avg) * 2, spcy-1)
            pix[i,j] = spc[x,y]

    path = "mod" + path
    im.save (path)
    im.close ()
    
host = "192.168.43.170" # host router shutup (********) si Redmi (*********)
port = 5560
bfsz = 1024

s = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
s.connect ( ( host, port ) )

ser = serial.Serial ( '/dev/ttyUSB0', 9600 )

print ( "connected to remote" )
tstart = tloop = time ()
mxmvt = 0

pics_taken = 0
dimx = 160
dimy = 120
camera.resolution = (dimx, dimy)
camera.rotation = 180
camera.start_preview ()

spcx = 27
spcy = 282
ims = Image.open ("spectrum.png")
ims = ims.convert ("RGB")
spc = ims.load ()

thold = 37 # 37 px / 2 grade celsius diferenta
pc_tmp = 0.5 # cat de semnificativa e temp masurata?
# temp min = 0 grade (spcy), temp max = 40 grade (0)

flag = 0
while flag == 0 :
    mvt = get_mvt ()
    if mvt > mxmvt :
        mxmvt = mvt
        
    if tloop - tstart >= 1 :  
        tstart = tloop

        hmd = int ( sense.get_humidity () * 100 ) / 100
        tmp = int ( sense.get_temperature () * 100 ) / 100
        prs = int ( sense.get_pressure () * 100 ) / 100
        ind = get_ind ()
        nh4, co2, dst = ar_getdata ( ser )
        message = str ( hmd ) + '!' + str ( tmp ) + '!' + str ( prs ) + '!' + str ( mxmvt ) + '!' + str ( ind ) + '!' + str ( nh4 ) + '!' + str ( co2 ) + '!' + str ( dst ) + '!'
        
        s.send ( str.encode ( message ) )
        print ( "packet sent :", message )
        mxmvt = 0
        # ir
        path = "photos/p" + str (pics_taken) + ".jpg"
        camera.capture (path, use_video_port = True)
        processpic (pics_taken)
        pics_taken += 1
        
    tloop = time ()
    for event in pygame.event.get () : # joystick
      if event.type == KEYDOWN :
        if event.key == K_RETURN :
          flag = 1

s.close ()
camera.stop_preview ()

