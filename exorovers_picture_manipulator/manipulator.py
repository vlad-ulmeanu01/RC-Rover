from PIL import Image
def MIN (a, b) :
    if (a < b) :
        return a
    else :
        return b
 
def MAX (a, b) :
    return a + b - MIN (a, b)
 
def processpic (k) :
    path = "p" + str (k) + ".jpg"
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

dimx = 160
dimy = 120

thold = 37 # 37 px / 2 grade celsius diferenta
pc_tmp = 0.3 # cat de semnificativa e temp masurata?
tmp = 25
spcx = 27
spcy = 282
ims = Image.open ("spectrum.png")
ims = ims.convert ("RGB")
global spc
spc = ims.load ()
 
processpic (426)
