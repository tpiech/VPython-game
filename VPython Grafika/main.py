from vpython import *
import math
import time
from pynput import keyboard


###################################################################################################################################

def choose_variant():
    v = int(input("insert level do you want to play 1 - 3"))
    global Can
    global Shelves
    if v == 1:
        Can.append(Pin(15,0,-40,5))
        Can.append(Pin(15,0,-20,5))
        Can.append(Pin(15,0,0,5))
        Can.append(Pin(15,0,20,5))
        Can.append(Pin(15,0,40,5))
    elif v == 2:
        Can.append(Pin(45,30,-40,5))
        Shelves.append(box( pos = vector(45,30,-40),height = 0.01,length = 10,width = 10))
        Can.append(Pin(30,20,-20,5))
        Shelves.append(box( pos = vector(30,0,-40),height = 0.01,length = 10, width = 10))
        Can.append(Pin(15,0,0,5))
        Shelves.append(box( pos = vector(15,0,0),height = 0.01,length = 10, width = 10))
        Can.append(Pin(30,20,20,5))
        Shelves.append(box( pos = vector(30,20,20),height = 0.01,length = 10, width = 10))
        Can.append(Pin(45,30,40,5))
        Shelves.append(box( pos = vector(45,30,40),height = 0.01,length = 10, width = 10))
    elif v == 3:
        Can.append(Pin(-45,30,-40))
        Shelves.append(box( pos = vector(-45,30,-40),height = 0.01,length = 10, width = 10))
        Can.append(Pin(-30,20,-20,5))
        Shelves.append(box( pos = vector(-30,20,-20),height = 0.01,length = 10, width = 10))
        Can.append(Pin(15,0,0,5))
        Shelves.append(box( pos = vector(15,0,0),height = 0.01,length = 10, width = 10))
        Can.append(Pin(30,20,20,5))
        Shelves.append(box( pos = vector(30,20,20),height = 0.01,length = 10, width = 10))
        Can.append(Pin(45,30,40,5))
        Shelves.append(box( pos = vector(45,30,40),height = 0.01,length = 10, width = 10))
    else:
        print("No such level exists")


###################################################################################################################################




###################################################################################################################################
scene = canvas(title='Shoot the ball', width = 720, height = 600)
lamp = local_light(pos=vector(5,10,0),
                      color=color.yellow)
scene.autoscale = False
#ustwaienia sceny
###################################################################################################################################




###################################################################################################################################
def move_loop(Bowl):
    Bowl.cnd = not(Bowl.cnd)
def changeZleft(Bowl):
    Bowl.bowl.vel.z -=0.1
def changeZright(Bowl):
    Bowl.bowl.vel.z +=0.1
def changeYup(Bowl):
    Bowl.bowl.vel.y +=0.1
def changeYdown(Bowl):
    Bowl.bowl.vel.y -=0.1
def resetSpeeds(Bowl):
    Bowl.bowl.vel = vector(1,1,0)
def changeXforward(Bowl):
    Bowl.bowl.vel.x +=0.1
def changeXbackward(Bowl):
    Bowl.bowl.vel.x -=0.1
def resetBallPos(Bowl):
    Bowl.bowl.pos = Bowl.startingPos
    Bowl.IsAtStartingPosition = True

#sterowanie kulki i celownika
###################################################################################################################################





###################################################################################################################################
def on_press(key):
    global aim
    if key == keyboard.Key.space and Ball.IsAtStartingPosition == True:
        move_loop(Ball)
        global count_of_shots 
        count_of_shots += 1
    if key == keyboard.Key.left:
        changeZleft(Ball)
        aim.pos.z -= 0.2
    if key == keyboard.Key.right:
        changeZright(Ball)
        aim.pos.z += 0.2       
    if key == keyboard.Key.up:
        changeYup(Ball)
        aim.pos.y += 0.2
    if key == keyboard.Key.down:
        changeYdown(Ball)
        aim.pos.y -= 0.2
    if key == keyboard.KeyCode.from_char('r'):
        aim.pos = vector(3,4,0)
        resetSpeeds(Ball)
    if key == keyboard.KeyCode.from_char('w'):
        changeXforward(Ball)
        aim.pos.x += 0.2
    if key == keyboard.KeyCode.from_char('s'):
        changeXbackward(Ball)
        aim.pos.x -= 0.2
    if key == keyboard.KeyCode.from_char('t'):
        aim.pos = Ball.bowl.pos+vector(3,2,0)
        resetBallPos(Ball)
def on_release(key):
    return 0

###################################################################################################################################


class Bowl: 
    def __init__(self, x, y, z, rad):
        self.bowl = sphere(pos = vector(x,y,z), radius = rad, color = color.red  , make_trail=True, texture = textures.wood_old)
        self.startingPos = vector(x,y,z)
        self.bowl.vel = vector(1,1,0)
        self.cnd = False
        self.IsAtStartingPosition = True
class Pin:
    def __init__(self, x, y, z, rad):
        self.pin = cylinder(pos=vector(x,y,z), axis=vector(0,1,0), radius=rad, length = rad*4, make_trail=True, texture = textures.metal)
        self.centre = vector(x,(self.pin.length+y)/2,z)
        self.stable = True
        self.higher_or_lower = 0
    def invisible(self):
        self.pin.visible = False

###################################################################################################################################

#########################################################################################################################################################
Ball = Bowl(0,2,0,2)
#kulka do strzelania
aim = sphere(pos = Ball.bowl.pos+vector(3,2,0), radius = 0.3, color = color.red)
# celownik
VisibleCans = [True, True, True, True, True]
Can = []
#tablica na "cele"
Shelves = []
#labica na "podstawki pod cele"
dt = 0.1
#krok czasowy
count_of_shots = 0
#licznik strzalow
my_floor = box(pos = vector(0,0,0), height = 0.01, width = 100, length = 100)
#Podloga
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
#wykrywacz przyciskow

#########################################################################################################################################################

listener.start()
choose_variant()



while True:
    scene.caption="X speed = {} Y speed = {} Z speed = {} Arrow keys to change Y and Z, W and S to change X, R to reset speeds, T to reset ball position, space to shoot".format(Ball.bowl.vel.x, Ball.bowl.vel.y, Ball.bowl.vel.z)
    rate(100)
    t = 0
    while Ball.cnd == True:
        rate(100)
        t += dt
        S = label(pos=vector(0,-10,0),text='Number of shots: {}'.format(count_of_shots), xoffset=20, yoffset=50, space=30, height=16, border=4,font='sans')
        for i in range(0,len(Can)):
            if Can[i].stable == False and Can[i].pin.axis.y > 0:
                Can[i].pin.rotate(angle=math.pi*0.05, axis = vector(Can[i].pin.pos.z-Ball.startingPos.z,0,Can[i].higher_or_lower), origin=Can[i].centre)
                if Can[i].pin.pos.y > 0:
                    Can[i].pin.pos.y = Can[i].pin.pos.y - (t*t*0.2)
            elif  Can[i].pin.axis.y <= 0:
                Can[i].invisible()
                VisibleCans[i] = False
            if True not in VisibleCans:
                L = label(pos=vector(0,0,0),text='CONGRATULATIONS! YOU WON!', xoffset=20, yoffset=50, space=30, height=16, border=4,font='sans')
        for i in range(0,len(Can)):
            if Ball.bowl.pos.y > 1:
                Ball.IsAtStartingPosition = False 
                Ball.bowl.pos.x += Ball.bowl.vel.x * t
                Ball.bowl.pos.z += Ball.bowl.vel.z * t
                Ball.bowl.pos.y = Ball.bowl.pos.y - (t*t*0.2) + Ball.bowl.vel.y * t
                if( abs(Ball.bowl.pos.x - Can[i].pin.pos.x) <= (Ball.bowl.radius+Can[i].pin.radius) and Ball.bowl.pos.y-Ball.bowl.radius <= (Can[i].pin.pos.y+Can[i].pin.length) and ( Ball.bowl.pos.z-Ball.bowl.radius < Can[i].pin.pos.z+Can[i].pin.radius and Ball.bowl.pos.z+Ball.bowl.radius > Can[i].pin.pos.z-Can[i].pin.radius )  ):
                    Can[i].stable = False
                    if Ball.bowl.pos.y < (Can[i].pin.pos.y+Can[i].pin.length)/2:
                        Can[i].higher_or_lower = 1
                    elif Ball.bowl.pos.y > (Can[i].pin.pos.y+Can[i].pin.length)/2:
                        Can[i].higher_or_lower = -1
                    else:
                        Can[i].higher_or_lower = 0
            else:
                Ball.cnd = False
                

