from sense_hat import SenseHat
from time import *

sense = SenseHat()

bval = bx = by = bz =0
b = 0

while 1 > 0 :
    bval = sense.get_compass_raw ()
    ( bx, by, bz ) = bval
    b = ( bx * bx + by * by + bz * bz ) ** 0.5
    print ( b )
    sleep ( 0.2 )    
