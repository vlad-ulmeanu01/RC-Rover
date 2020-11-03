from struct import unpack
import socket
import pygame
from pygame.locals import *
from PIL import Image
from random import randint
from time import *

pygame.init()

white = ( 255, 255, 255 )
red = ( 255, 0, 0 )
black = ( 0, 0, 0 )
dark_green = ( 0, 100, 0 )
dark_goldenrod = ( 184, 134, 11 )
yellow = ( 255, 255, 0 )
lawn_green = ( 124, 252, 0 )
hot_pink = ( 255, 105, 180 )
orange_red = ( 255, 69, 0 )
firebrick = ( 178, 34, 34 )
blue = ( 0, 0, 255 )
light_blue = ( 135, 206, 250 )
mauve = ( 194, 100, 255 )
indigo = ( 75, 0, 130 )
orange = ( 255, 165, 0 )

img_print = [0] * 10

host = ''
port = 5560

def ph_iscf ( ch ) :
    return ch >= '0' and ch <= '9'

def ph_getnum ( clg, ind, string ) :
    nr = 0
    while ind < clg and ph_iscf ( string[ind] ) == False :
        ind += 1
    while ind < clg and ph_iscf ( string[ind] ) == True :
        nr = nr * 10 + int ( string[ind] )
        ind += 1

    return ( nr, ind )

def ph_setup () :
    s = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    print ( "socket created" )
    try :
        s.bind ( ( host, port ) )
    except socket.error as msg :
        print ( msg )
    print ( "socket bind" )

    return s

def ph_getimg ( s, conn, name ) :
    bfsz = 2048
    
    enc = conn.recv ( 8 )
    (lg,) = unpack ( '>Q', enc )
    string = ""
    clg = lg

    i = 0
    while lg > 0 :
        _m = min ( bfsz, lg )
        get = conn.recv ( _m )
        get = get.decode ( "utf-8" )
        string += get
        i += 1
        lg -= _m
        sleep ( 0.01 )

    print ( clg, len ( string ) )
    
    im = Image.open ( "sample.png" )
    im = im.convert ( "RGB" )
    data = im.load ()

    cl, ln = im.size
    crash = 0
    ind = 0
    for x in range ( 0, cl ) :
        if crash == 1 :
            break
        for y in range ( 0, ln ) :
            try :
                r, ind = ph_getnum ( clg, ind, string )
                g, ind = ph_getnum ( clg, ind, string )
                b, ind = ph_getnum ( clg, ind, string )
                data[ x, y ] = ( r, g, b )
            except :
                print ( "crash", x, y, ind )
                crash = 1
                break

    print ( crash )
    message = str.encode ( "1" )
    conn.send ( message )
    
    im.save ( name )
    im.close ()

s = ph_setup ()
s.listen ( 1 )
conn, addr = s.accept ()

def load_dgt () :
    i = 0
    for i in range ( 0, 10 ) :
        img_print[i] = pygame.image.load ( str ( i ) + ".png" ).convert()

def nr_cifre ( n ) :
    nc = 0
    while n > 0 :
        nc += 1
        n = int ( n / 10 )
    return nc

def print_num ( n, x, y ) :
    n = int ( n )
    nc = nr_cifre ( n )

    p10 = 10 ** ( nc - 1 )
    
    for i in range ( 0, nc ) :
        window.blit ( img_print[ int ( n / p10 ) % 10 ], ( x + i * 44, y ) )
        p10 /= 10
  
cx = 650
cy_nh4 = 50
cy_co2 = 145
cy_dst = 240
cy_img = 335

window = pygame.display.set_mode ( ( 832, 480 ) )

load_dgt ()
bg = pygame.image.load( "bg_hao2018.png" ).convert()
window.blit ( bg, ( 0, 0 ) )

cyc = 0
while 1 :
    # get img
    name = "pic" + str ( cyc ) + ".png"
    ph_getimg ( s, conn, name )
    print ( "got cycle", cyc )
    
    # valori arduino
    nh4 = randint ( 1, 1024 ) % 1024
    co2 = randint ( 1, 1024 ) % 1024
    dst = randint ( 1, 1024 ) % 1024

    print_num ( nh4, cx, cy_nh4 )
    print_num ( co2, cx, cy_co2 )
    print_num ( dst, cx, cy_dst )

    im = pygame.image.load ( "pic" + str ( cyc ) + ".png" ).convert()

    window.blit ( im, ( cx, cy_img ) )
    
    pygame.display.flip ()
    sleep ( 1 )
    cyc += 1

conn.close ()
s.close ()
