# Paper Minecraft Remake
# Copyright (c)2022 cjplays Development
# All Rights Reserved

#- Setup -#

# Imports
import pygame
import pygame.freetype
import time 
import random

# Pygame Setup
pygame.init()
clock = pygame.time.Clock()
FPS = 60

# Fonts Setup
invenFont = pygame.freetype.Font("Archivo-Regular.ttf")
invenFont.size = 50
invenFont.fgcolor = [171, 171, 171]
invenTileFont = pygame.freetype.Font("Archivo-Regular.ttf")
invenTileFont.size = 30
invenTileFont.fgcolor = [111,111,111]
steveFont = pygame.freetype.Font("Archivo-Regular.ttf")
steveFont.size = 100
steveFont.fgcolor = [36,36,36]
steveFont2 = pygame.freetype.Font("Archivo-Regular.ttf")
steveFont2.size = 30
steveFont2.fgcolor = [36,36,36]
withSteveRect = pygame.Rect(100,452,175,175)
withoutSteveRect = pygame.Rect(1705,452,175,175)
withSteve = pygame.image.load("Boulder.png")
withoutSteve = pygame.image.load("BoulderBack.png")
# Dictionary Setup [contains grids for the building space and inventory]
tilerects = {}
tilecolors = {}
invenrects = {}
invenoutlines = {}
invenblocks = {}


# Default building block is air
mode = "air"

# Steve setup
stevemove = "n"
steveX = 0
steveY = 555
steve = pygame.image.load("Boulder.png")
steveH, steveW = steve.get_size()

# Steve's bounding box
steveCollision = pygame.Rect(steveX,steveY,steveH,steveW)

# Variable used to fix a bug with selection cursor
currentsquare = False

# Inventory is closed by default
inventory = False

# Defines colors for blocks. "mouse" is the color of the cursor when hovering over the block
colors = {"air":[0, 213, 255],"dirt":[130, 69, 0],"grass":[0, 224, 67],
          "stone":[115, 115, 115],"mouseair":[0,203,255],"mousedirt":[120,59,0],
          "mousegrass":[0,214,57],"mousestone":[105,105,105],"inventory":[222,222,222],
         "mouseinventory":[212,212,212],"sand":[255, 235, 189],"mousesand":[245,225,189],"red concrete":[171, 2, 2],"mousered concrete":[161,0,0],
         "orange concrete":[255,165,0],"mouseorange concrete":[245,155,0],"yellow concrete":[235, 214, 5],"mouseyellow concrete":[225,204,0],
         "lime concrete":[86, 207, 10],"mouselime concrete":[76,197,0], "green concrete":[0, 112, 26], "mousegreen concrete": [0,102,16],"light blue concrete":[22, 204, 224],
         "mouselight blue concrete":[12, 194, 214],"cyan concrete":[14, 156, 144],"mousecyan concrete":[4,146,134],"blue concrete":[0, 43, 107],"mouseblue concrete":[0,33,97],
         "purple concrete":[126, 0, 199], "mousepurple concrete":[116, 0, 189],"black concrete":[10,10,10],"mouseblack concrete":[0,0,0],"white concrete":[255,255,255],
         "mousewhite concrete":[245,245,245],"magenta concrete":[196, 0, 199],"mousemagenta concrete":[186,0,189],"brown concrete":[105, 64, 8],"mousebrown concrete":[95,54,0],"pink concrete":[255, 120, 246],
         "mousepink concrete":[245,110,236],"light gray concrete":[140, 140, 140],"mouselight gray concrete":[130,130,130],"gray concrete":[94, 94, 94],"mousegray concrete":[84,84,84], "water":[15, 127, 255],"mousewater":[0,117,245],
         "ice":[15, 250, 246],"mouseice":[5,240,236],"end stone":[240, 255, 143],"mouseend stone":[230,245,133],"obsidian":[34, 0, 36],"mouseobsidian":[24,0,26],"diamond block":[43, 194, 224],"mousediamond block":[33,184,214],"gold block":[240, 217, 48],
         "mousegold block":[230,207,38]}

# More pygame setup
w = pygame.display.set_mode([1920,1080])

# Allows the user to play with/without steve
choice = False
w.fill([173,173,173])

steveFont.render_to(w,[450,0],"CHOOSE GAMEMODE")
pygame.draw.ellipse(w,[36,36,36],withSteveRect,4)
pygame.draw.ellipse(w,[36,36,36],withoutSteveRect,4)
w.blit(withSteve, [100,452])
w.blit(withoutSteve, [1705,452])
steveFont2.render_to(w,[75,652],"Steve Enabled")
steveFont2.render_to(w,[1690,652],"Steve Disabled")
running = True
while not choice:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            choice = False
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mX,mY = pygame.mouse.get_pos()
            if withSteveRect.collidepoint(mX,mY):
                choice = True
                steveon = True
            if withoutSteveRect.collidepoint(mX,mY):
                choice = True
                steveon = False
                
# Creates default landstape and defines Rects for the basic grid of blocks
for i in range(1,17):
    for j in range(1,10):
        if 1 <= j <= 6:
            tilecolors[str(i) + " " + str(j)] = "air"
        elif j == 7:
            tilecolors[str(i) + " " + str(j)] = "grass"
        elif j == 8:
            tilecolors[str(i) + " " + str(j)] = "dirt"
        else:
            tilecolors[str(i) + " " + str(j)] = "stone"
        tilerects[str(i) + " " + str(j)] = pygame.Rect(i * 120 - 120, j * 120 - 120, 120, 120)
        pygame.draw.rect(w,colors[tilecolors[str(i) + " " + str(j)]],tilerects[str(i) + " " + str(j)])

# Defines rects for inventory tiles
for i in range(1,17):
    for j in range(1,9):
        invenoutlines[str(i) + " " + str(j)] = pygame.Rect(i * 120 - 120,(j * 120 - 120) + 120,119,119)
        invenrects[str(i) + " " + str(j)] = pygame.Rect((i * 120 - 120) + 4, ((j * 120 - 120) + 120) + 4, 111,111)

# Fills in inventory tiles with blocks
invenblocks["1 1"] = "air"
invenblocks["2 1"] = "dirt"
invenblocks["3 1"] = "stone"
invenblocks["4 1"] = "grass"
invenblocks["5 1"] = "sand"
invenblocks["6 1"] = "water"
invenblocks["7 1"] = "ice"
invenblocks["8 1"] = "end stone"
invenblocks["9 1"] = "obsidian"
invenblocks["10 1"] = "diamond block"
invenblocks["11 1"] = "gold block"
invenblocks["1 8"] = "red concrete"
invenblocks["2 8"] = "orange concrete"
invenblocks["3 8"] = "yellow concrete"
invenblocks["4 8"] = "lime concrete"
invenblocks["5 8"] = "green concrete"
invenblocks["6 8"] = "light blue concrete"
invenblocks["7 8"] = "cyan concrete"
invenblocks["8 8"] = "blue concrete"
invenblocks["9 8"] = "purple concrete"
invenblocks["10 8"] = "black concrete"
invenblocks["11 8"] = "white concrete"
invenblocks["12 8"] = "magenta concrete"
invenblocks["13 8"] = "brown concrete"
invenblocks["14 8"] = "pink concrete"
invenblocks["15 8"] = "light gray concrete"
invenblocks["16 8"] = "gray concrete"

# Creates empty tiles for non-defined inventory spaces
for i in range(1,17):
    for j in range(1,9):
        if (str(i) + " " + str(j)) not in invenblocks:
            invenblocks[str(i) + " " + str(j)] = "inventory"

pygame.display.flip()

# Redraws landscape after closing inventory
def redraw():
    for i in tilerects:
        pygame.draw.rect(w,colors[tilecolors[i]],tilerects[i])
        pygame.display.flip()
        if steveon:
            w.blit(steve,[steveX,steveY])
            
# Draws steve
if steveon:
    w.blit(steve,[steveX,steveY])
    
# Main loop


while running:
    
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            
            # Gets mouse position for cursor
            mX, mY = pygame.mouse.get_pos()
            
            if not inventory:
                # Makes sure steve is not drawn over
                steveMouseCollision = pygame.Rect(steveX - 60, steveY - 60, steveH + 180, steveW + 180)
                
                
                for i in tilerects:
                    if tilerects[i].collidepoint(mX,mY) and currentsquare != i and (not steveMouseCollision.collidepoint(mX,mY) or not steveon):
                        # Erases old cursor
                        try:
                            pygame.draw.rect(w,colors[tilecolors[currentsquare]],tilerects[currentsquare])
                        except:
                            pygame.draw.rect(w,colors[tilecolors[i]],tilerects[i])
                        
                        # Sets up cursor to be erased when it is moved
                        currentsquare = i
                        
                        # Draws new cursor
                        pygame.draw.rect(w,colors["mouse" + tilecolors[i]],tilerects[i])
                        pygame.display.flip()
                        
            
            if inventory:
                
                # Same code as before for inventory
                
                for i in invenrects:
                    if invenrects[i].collidepoint(mX,mY) and currentsquare != i:
                        temp = colors["mouse" + invenblocks[i]]
                        
                        # Makes text readable on darker blocks
                        
                        if temp[0] + temp[1] + temp[2] <= 345:
                            invenTileFont.fgcolor = [255,255,255]
                        else:
                            invenTileFont.fgcolor = [111,111,111]
                            
                        # Erases old cursor
                        try:
                            pygame.draw.rect(w,colors[invenblocks[currentsquare]],invenrects[currentsquare])
                        except:
                            pygame.draw.rect(w,colors[invenblocks[i]],invenrects[i])
                            
                        # Sets up cursor to be erased when it is moved
                        
                        currentsquare = i
                        
                        # Draws new cursor
                        pygame.draw.rect(w,colors["mouse" + invenblocks[i]], invenrects[i])
                        
                        # Draws text for blocks
                        if invenblocks[i] != "inventory":
                            
                            # Super complicated method for text wrapping in pygame
                            
                            # Tsapp: add one number to your code
                            # pygame:
                            temptext = invenblocks[i].capitalize()
                            if len(temptext) < 7:
                                invenTileFont.render_to(w,[invenrects[i].x + 1,invenrects[i].y + 1],invenblocks[i].capitalize())
                            else:
                                temptext2 = {}
                                temptext3 = len(temptext) // 6
                                temptext4 = len(temptext) % 6
                                for j in range(1,temptext3 + 1):
                                    #print(i)
                                    temptext2[j] = temptext[(j * 6 - 6):j * 6]
                                if temptext4 > 0:
                                    temptext2[temptext3 + 1] = temptext[len(temptext) - temptext4:]
                                for j in temptext2:
                                    temptext2[j] = temptext2[j].lstrip(" ")
                                    #print(temptext2)
                                    invenTileFont.render_to(w,[invenrects[i].x + 1,invenrects[i].y + (j * 30) - 30],temptext2[j])
                                    
                        pygame.display.flip()
                        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if not inventory:
                # Places block
                tilecolors[currentsquare] = mode
                pygame.draw.rect(w,colors[tilecolors[currentsquare]],tilerects[currentsquare])
            if inventory:
                # Selects block in inventory
                mX,mY = pygame.mouse.get_pos()
                for i in invenrects:
                    if i in invenblocks and invenrects[i].collidepoint(mX,mY) and invenblocks[i] != "inventory":
                        #print(invenblocks[i])
                        mode = invenblocks[i]
                        
            pygame.display.flip()
            
        if event.type == pygame.KEYDOWN:
            
            # Moves steve if enabled
            if steveon:
                if event.key == pygame.K_LEFT:
                    stevemove = "l"
                if event.key == pygame.K_RIGHT:
                    stevemove = "r"
                
            if event.key == pygame.K_SPACE:
                
                # Opens inventory
                if not inventory:
                    inventory = True
                    w.fill(colors["inventory"])
                    
                    # Draws outlines
                    for i in invenoutlines:
                        pygame.draw.rect(w,colors["mouseinventory"],invenoutlines[i],4)
                        pygame.display.flip()
                    # Draws blocks
                    for i in invenrects:
                        if i in invenblocks:
                            pygame.draw.rect(w,colors[invenblocks[i]],invenrects[i])
                            pygame.display.flip()
                    # Writes "inventory" on the screen
                    invenFont.render_to(w, [50,50],"Inventory")
                    pygame.display.flip()
                    continue
                
                # Closes inventory
                if inventory:
                    inventory = False
                    redraw()
                    
        # Stops moving steve
        if event.type == pygame.KEYUP:
            if steveon:
                if event.key == pygame.K_LEFT:
                    stevemove = "n"
                    
                if event.key == pygame.K_RIGHT:
                    stevemove = "n"
                    
    # Moves steve                
    if stevemove != "n" and not inventory and steveon:
        
        # Makes sure steve is not walking inside blocks
        steveH, steveW = steve.get_size()
        steveCollision = pygame.Rect(steveX,steveY,steveH,steveW)
        if stevemove == "l":
            for i in tilerects:
                if tilecolors[i] != "air":
                    if tilerects[i].colliderect(steveCollision):
                        stevemove = "n"
                        continue
                        
            # Erases old steve
            pygame.draw.rect(w,colors["air"],steveCollision)
            steveX -= 5
            
            # Draws new steve
            w.blit(steve,[steveX,steveY])
            
            # Same code as above for moving right
        if stevemove == "r":
            for i in tilerects:
                if tilecolors[i] != "air":
                    if tilerects[i].colliderect(steveCollision):
                        stevemove = "n"
                        continue
                        
            # Erases old steve
            pygame.draw.rect(w,colors["air"],steveCollision)
            steveX += 5
            
            # Draws new steve
            w.blit(steve,[steveX,steveY])
    
    pygame.display.flip()
    clock.tick(FPS)
                
                
