# Initialization

import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Variables and stuff

Gravity = 0.2
floorY = 570
damping = 0.96


LinkedPoint = []
LinkingPoint = []
elasticity = []
targetLength = []
Fixed = []
OldX = []
OldY = []
X = []
Y = []

# Move And Draw Points

def AddPoint(x, y, VelX, VelY, Fix):
    OldX.append(x - VelX)
    OldY.append(y - VelY)
    Fixed.append(Fix)
    X.append(x)
    Y.append(y)

def AddLink(p1, p2, e, length):
    LinkedPoint.append(p1)
    LinkingPoint.append(p2)
    elasticity.append(e)
    targetLength.append(length)

def applyLinkForce(x1, y1, x2, y2, L, k, f1, f2):
    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx*dx + dy*dy)
    c = (distance - L)*k/(2*distance)
    newX1, newY1, newX2, newY2 = x1, y1, x2, y2
    if(f1==0):
        newX1 += dx*c
        newY1 += dy*c
    if(f2==0):
        newX2 -= dx*c
        newY2 -= dy*c
    return(newX1, newY1, newX2, newY2)

def Apply_Gravity_To_Point(pointNo):
    VelocityX = X[pointNo] - OldX[pointNo]
    VelocityY = Y[pointNo] - OldY[pointNo] + Gravity

    OldX[pointNo] = X[pointNo]
    OldY[pointNo] = Y[pointNo]

    X[pointNo] += VelocityX
    Y[pointNo] += VelocityY
    
def Apply_Floor(pointNo):
    if(Y[pointNo]>(floorY + 5)):
        Y[pointNo] = floorY + 5
    if(X[pointNo]>(750 + 5)):
        X[pointNo] = 750 + 5
    if(X[pointNo]<(25 + 5)):
        X[pointNo] = 25 + 5
        
def collide(x1, y1, x2, y2, r1, r2, distance, fix):
    distance = math.sqrt(distance)
    dx = x1 - x2
    dy = y1 - y2
    if(distance==0):
        cos = 1
        sin = 1
    else:
        cos = dx/distance
        sin = dy/distance
    depth = -(distance-(r1+r2))
    newX1 = (depth*cos)/2 + x1
    newY1 = (depth*sin)/2 + y1
    newX2, newY2 = x2, y2
    if(fix==0):
        newX2 += (-depth*cos)/2
        newY2 += (-depth*sin)/2
    return(newX1, newY1, newX2, newY2)
    
def dampVelocity(pointNo, Damping):
    XVel = X[pointNo] - OldX[pointNo]
    YVel = Y[pointNo] - OldY[pointNo]
    OldX[pointNo] = X[pointNo] - XVel * Damping
    OldY[pointNo] = Y[pointNo] - YVel * Damping
        
def collidePoints(pointNo):
    pointX = X[pointNo]
    pointY = Y[pointNo]
    r1 = 5
    for point in range(len(X)):
        if(point != pointNo):
            point2X = X[point]
            point2Y = Y[point]
            r2 = 5

            dx = pointX - point2X
            dy = pointY - point2Y
            distance = (dx*dx + dy*dy)
            if(distance<((r1+r2)*(r1+r2))):
                 X[pointNo], Y[pointNo], X[point], Y[point] = collide(pointX, pointY, point2X, point2Y, r1, r2, distance, Fixed[point])
                 dampVelocity(pointNo, damping)
                 dampVelocity(point, damping)

def Move_Points():
    #Gravity and collisions
    for i in range(len(X)):
        if(Fixed[i]==0):
            Apply_Gravity_To_Point(i)
            collidePoints(i)
        Apply_Floor(i)
    #links/connections
    for i in range(len(LinkedPoint)):
        p1 = LinkedPoint[i]
        p2 = LinkingPoint[i]
        X[p1], Y[p1], X[p2], Y[p2] = applyLinkForce(X[p1], Y[p1], X[p2], Y[p2], targetLength[i], elasticity[i], Fixed[p1], Fixed[p2])
        pygame.draw.line(
            screen,
            (255,255,255),
            (int(X[p1]), int(Y[p1])),
            (int(X[p2]), int(Y[p2]))
        )

def Draw_Points():
    for i in range(len(X)):
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(X[i]), int(Y[i])),
            5
        )

# Shapes -

def Triangle(x, y, size):
    startPoint = len(X)
    AddPoint(x, y, 0, -5, 0)
    AddPoint(x, y, 0, -5, 0)
    AddPoint(x, y, 2, -5, 0)
    AddLink(startPoint, startPoint+1, 0.6, size)
    AddLink(startPoint+2, startPoint+1, 0.6, size)
    AddLink(startPoint+2, startPoint, 0.6, size)

def Square(x, y, size):
    startPoint = len(X)
    AddPoint(x, y, 0, 0, 0)
    AddPoint(x+size, y, 0, 0, 0)
    AddPoint(x+size, y+size, 0, 0, 0)
    AddPoint(x, y+size, 0, 0, 0)
    AddLink(startPoint, startPoint+1, 0.6, size)
    AddLink(startPoint+2, startPoint+1, 0.6, size)
    AddLink(startPoint+3, startPoint, 0.6, size)
    AddLink(startPoint+3, startPoint+2, 0.6, size)
    AddLink(startPoint, startPoint+2, 0.6, size*math.sqrt(2))
    AddLink(startPoint+1, startPoint+3, 0.6, size*math.sqrt(2))
    
# Add the points

Square(200, 100, 75)
Triangle(100, 100, 75)
for i in range(36):
    AddPoint(100+i*8, 100, 0, 0, 0)

# Making the window -

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill((0, 0, 0))

    Move_Points()
    Draw_Points()

    pygame.display.update()
    clock.tick(60)