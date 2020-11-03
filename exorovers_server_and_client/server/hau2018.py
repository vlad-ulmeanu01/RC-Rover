from time import *
import datetime
import pygame
from pygame.locals import *
import random
import socket

host = ''
port = 5560
bfsz = 1024

def MIN ( a, b ):
  if a < b:
    return a
  else :
    return b

def MAX ( a, b ):
  return a + b - MIN ( a, b )

def setup () :
  s = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
  print ( "socket created" )
  try :
    s.bind ( ( host, port ) )
  except socket.error as msg :
    print ( msg )
  print ( "socket bind" )

  return s

pygame.init()
window = pygame.display.set_mode ( ( 832, 480 ) )

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

bg1 = pygame.image.load( "bg_menu.png" ).convert()
bg2 = pygame.image.load( "bg_hao2018.png" ).convert()
img_hmd = pygame.image.load ( "show_hmd.png" ).convert()
img_tmp = pygame.image.load ( "show_tmp.png" ).convert()
img_prs = pygame.image.load ( "show_prs.png" ).convert()
img_mvt = pygame.image.load ( "show_mvt.png" ).convert()
img_ind = pygame.image.load ( "show_ind.png" ).convert()
slash = pygame.image.load ( "show_slash.png" ).convert()
img_y_p = pygame.image.load ( "show_yes.png" ).convert()
img_y_n = pygame.image.load ( "show_yes_n.png" ).convert()
img_n_p = pygame.image.load ( "show_no.png" ).convert()
img_n_n = pygame.image.load ( "show_no_n.png" ).convert()

cx = 650
cy_nh3 = 40
cy_co2 = 135
cy_dst = 240

#               hmd          tmp        prs        mvt   ind
col_norm = [ dark_green, orange_red, light_blue, mauve,  yellow         ]
col_trig = [ lawn_green, firebrick,  blue,       indigo, dark_goldenrod ]
trig_vec  = [ 40, 30, 1050, 0.2, 45 ]

img_print = [0] * 10

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

def printnum ( n, x, y ) :
  n = int ( n )
  nc = nr_cifre ( n )

  p10 = 10 ** ( nc - 1 )
    
  for i in range ( 0, nc ) :
    window.blit ( img_print[ int ( n / p10 ) % 10 ], ( x + i * 44, y ) )
    p10 /= 10

def main () :
  load_dgt ()
  
  LN = 480
  CL = 640
  CLP = 832
  SQ = 4

  skt = setup ()
  skt.listen ( 1 )
  conn, addr = skt.accept ()
  
  window = pygame.display.set_mode ( ( CLP, LN ) )
  pygame.draw.rect ( window, white, Rect ( ( 0, 0 ), ( CLP, LN ) ) )

  nrch = 5 # alegeri pt umiditate / temperatura / presiune / vibratii / inductie magnetica
  yn = [1] * nrch

  data_graph_l = [ [ 0 for x in range ( nrch ) ] for y in range ( LN ) ]
  data_graph = [ [ 0 for x in range ( nrch ) ] for y in range ( LN * 15 ) ]
  
  print ( yn[0], yn[1], yn[2], yn[3], yn[4] )
  
  clock = pygame.time.Clock ()
  
  """ printing loop """
  pygame.draw.rect ( window, white, Rect ( ( 0, 0 ), ( CLP, LN ) ) ) 
  
  i = 0
  j = 0
  k = 0
  flag = 0
  cyc = 0
  newdata = 0
  tstart = tloop = time ()
  #filename = str (datetime.datetime.now()) + "data.csv"
  filename = "data/" + str (int(tstart)) + "data.csv"
  with open (filename, "a") as fout:
    fout.write ( "HMD,TMP,PRS,MVT,IND,NH3,CO2,DST\n" )
  
  while flag == 0 :
    for event in pygame.event.get () :
      if event.type == QUIT :
        pygame.quit ()
      elif event.type == KEYDOWN :
        if event.key == K_ESCAPE :
          flag = 1
        elif event.key == K_q :
          yn[0] = 1 - yn[0]
        elif event.key == K_w :
          yn[1] = 1 - yn[1]
        elif event.key == K_e :
          yn[2] = 1 - yn[2]
        elif event.key == K_r :
          yn[3] = 1 - yn[3]
        elif event.key == K_t :
          yn[4] = 1 - yn[4]

    window.blit ( bg2, ( 0, 0 ) )

    if tloop - tstart >= 0.9 :
      data = conn.recv ( bfsz )
      tstart = tloop
      if data :
        data = data.decode ( "utf-8" )
        hmd, tmp, prs, mvt, ind, nh3, co2, dst, *rest = data.split ( '!' )
        hmd = float (hmd)
        tmp = float (tmp)
        prs = float (prs)
        ind = float (ind)
        ind = MIN ( ind, 100.0 )
        mvt = float (mvt)
        mvt = MIN ( mvt, 1.0 )
        nh3 = float (nh3)
        co2 = float (co2)
        dst = float (dst)

        with open (filename, "a") as fout:
          fout.write ( str(hmd) + "," + str(tmp) + "," + str(prs) + "," + str(mvt) + "," + str(ind) + "," + str(nh3) + "," + str(co2) + "," + str(dst) + "\n" ) 

        hmd = int(hmd)
        tmp = int(tmp)
        prs = int(prs)
        ind = int(ind)
        nh3 = int(nh3)
        co2 = int(co2)
        dst = int(dst)

        printnum ( nh3, cx, cy_nh3 )
        printnum ( co2, cx, cy_co2 )
        printnum ( dst, cx, cy_dst )
        newdata = nrch
        print ( "received :", hmd, tmp, prs, mvt, ind, nh3, co2, dst )
        
    # mut datele
    for k in range ( 0, nrch ) :
      if yn[k] == 1 :
        for j in range ( 1, CL // SQ ) :
          # fac alb fostul patrat
          pygame.draw.rect ( window, white, Rect ( ( ( j - 1 ) * SQ, data_graph_l[j-1][k] ), ( SQ, SQ ) ) )
          # mut poz
          data_graph_l[j-1][k] = data_graph_l[j][k]
          # colorez noua pozitie si tin cont de trigger
          if data_graph[j-1][k] >= trig_vec[k] :
            pygame.draw.rect ( window, col_trig[k], Rect ( ( ( j - 1 ) * SQ, data_graph_l[j-1][k] ), ( SQ, SQ ) ) )
          else :
            pygame.draw.rect ( window, col_norm[k], Rect ( ( ( j - 1 ) * SQ, data_graph_l[j-1][k] ), ( SQ, SQ ) ) )

        # calculez pt. ciclul curent
        if newdata > 0 : # sau ping de la receiver
          newdata -= 1
          if k == 0 :
            tp_val = hmd
            data_graph_l[CL//SQ-1][k] = int ( LN - tp_val * SQ )
          elif k == 1 :
            tp_val = tmp
            data_graph_l[CL//SQ-1][k] = int ( LN - tp_val * SQ )
          elif k == 2 :
            tp_val = prs
            data_graph_l[CL//SQ-1][k] = int ( LN - ( tp_val - 950 ) * SQ )
          elif k == 3 :
            tp_val = int ( mvt * 100 )
            data_graph_l[CL//SQ-1][k] = int ( LN - int ( tp_val ) * SQ )
          elif k == 4 :
            tp_val = ind
            data_graph_l[CL//SQ-1][k] = int ( LN - tp_val * SQ )

          data_graph[int(cyc/nrch)][k] = tp_val
          cyc += 1
        else : # daca nu, copiaza
          data_graph_l[CL//SQ-1][k] = data_graph_l[CL//SQ-2][k]
          data_graph[CL//SQ-1][k] = data_graph[CL//SQ-2][k]
          cyc += nrch

        # desenez ultima coloana
        if data_graph[int(cyc/nrch)][k] >= trig_vec[k] :
          pygame.draw.rect ( window, col_trig[k], Rect ( ( ( j - 1 ) * SQ, data_graph_l[CL//SQ-1][k] ), ( SQ, SQ ) ) )
        else :
          pygame.draw.rect ( window, col_norm[k], Rect ( ( ( j - 1 ) * SQ, data_graph_l[CL//SQ-1][k] ), ( SQ, SQ ) ) )

        # trag liniile pentru mvt
        if k == 3 and yn[3] == 1 :
          for j in range ( 1, CL // SQ ) :
            if data_graph[j][k] >= trig_vec[k] :
              draw_color = indigo
            else :
              draw_color = mauve
            pygame.draw.line ( window, draw_color, ( ( j - 1 ) * SQ, data_graph_l[j-1][k] ), ( j * SQ, data_graph_l[j][k] ), 2 )
    
    tloop = time ()
    sleep ( 0.09 )  
    pygame.display.update ()
    clock.tick( 20 )

  pygame.quit ()
  return;

main ()
