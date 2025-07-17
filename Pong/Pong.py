import pygame
import math
import random

pygame.init()

TOGGLE_CLICKSTART = pygame.USEREVENT + 1
THROW_BALL = pygame.USEREVENT + 2

WIDTH = 1920
HEIGHT = 1080

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync = 1)
clock = pygame.time.Clock()
running = True

pygame.mouse.set_visible(0)
pygame.display.set_caption("Pong")
pygame.display.toggle_fullscreen()

gameStarted = False
settingsOpen = False
mode = "Two-player"
clickStartVisible = True
freePlayVisible = False
drawBall = True
drawPaddles = False
paddleSpeedMode = "Fast"
paddleSpeed = 10
ballRotationMode = "Dynamic"
ballSpeedMode = "Slow"
moveBall = True
gameEnded = False
debug = False
playSound = False

# ---CZCIONKI---
atari = pygame.font.Font("atari.otf", 60) # czcionka atari
freesansbold = pygame.font.Font("freesansbold.ttf", 30) # czcionka freesansbold

# ---DZWIEKI---
wallSound = pygame.mixer.Sound("wall.wav")
outSound = pygame.mixer.Sound("out.wav")
paddleSound = pygame.mixer.Sound("paddle.wav")

# statystyki
pointsLeft = 0
pointsRight = 0

# elementy gry
ball = pygame.Rect(954, 534, 12, 12)
goalLeft = pygame.Rect(470, 0, 10, 1080)
goalRight = pygame.Rect(1440, 0, 10, 1080)
wallTop = pygame.Rect(480, 0, 960, 10)
wallBottom = pygame.Rect(480, 1070, 960, 10)
paddleLeft = pygame.Rect(540, 515, 10, 50)
paddleRight = pygame.Rect(1370, 515, 10, 50)

# cechy ball
ballSpeed = 5

whichAngleStart = random.randint(0, 1)
if whichAngleStart == 0:
    ballAngle = 135

elif whichAngleStart == 1:
    ballAngle = 45

ballAngleRad = math.radians(ballAngle)

ballVelX = math.cos(ballAngleRad) * ballSpeed
ballVelY = -math.sin(ballAngleRad) * ballSpeed

whichPlayer = 0

# przerywana kreska na srodku
dashLenght = 15
gap = 15
x = WIDTH / 2 - 1

# startowanie gry
def startGame():
    global gameStarted, drawBall, drawPaddles, pointsLeft, pointsRight, moveBall

    drawPaddles = True
    drawBall = False
    gameStarted = True
    moveBall = False

    pygame.time.set_timer(THROW_BALL, 2000, loops = 1)

# serwowanie pilki
def throwBall():
    global ball, ballAngle, drawBall, ballVelX, ballVelY, pointsLeft, pointsRight, moveBall, playSound

    drawBall = True
    moveBall = True

    if playSound == False:
        playSound = True

    ball = pygame.Rect(954, random.randint(15, 1065), 12, 12)

    if whichPlayer == 0:
        whichAngle = random.randint(0, 1)
        
        if whichAngle == 0:
            ballAngle = 135
        
        elif whichAngle == 1:
            ballAngle = 225

    elif whichPlayer == 1:
        whichAngle = random.randint(0, 1)

        if whichAngle == 0:
            ballAngle = 45
        
        elif whichAngle == 1:
            ballAngle = 315

    ballAngleRad = math.radians(ballAngle)

    ballVelX = math.cos(ballAngleRad) * ballSpeed
    ballVelY = -math.sin(ballAngleRad) * ballSpeed

# roznica pomiedzy srodkiem pilki a paletka lewa
def checkOffset(paddle: pygame.Rect):
    offset = ball.centery - paddle.centery

    return offset

def resetGame():
    global gameStarted, gameEnded, drawBall, drawPaddles, clickStartVisible, freePlayVisible
    global pointsLeft, pointsRight, paddleLeft, paddleRight, ball, moveBall, playSound
    global ballVelX, ballVelY, ballAngle, ballAngleRad, ballSpeed

    gameStarted = False
    gameEnded = False
    drawBall = True
    drawPaddles = False
    clickStartVisible = True
    freePlayVisible = False
    pointsLeft = 0
    pointsRight = 0
    moveBall = True
    playSound = False

    paddleLeft = pygame.Rect(540, 515, 10, 50)
    paddleRight = pygame.Rect(1370, 515, 10, 50)
    ball = pygame.Rect(954, 534, 12, 12)

    whichAngle = random.randint(0, 1)
    if whichAngle == 0:
        ballAngle = 135
    else:
        ballAngle = 45

    ballAngleRad = math.radians(ballAngle)
    ballVelX = math.cos(ballAngleRad) * ballSpeed
    ballVelY = -math.sin(ballAngleRad) * ballSpeed


"""
# dynamiczny kat pilki
def dynamicBallRotationAngle(bat: pygame.Rect):
    maxOffset = bat.height / 2

    offset = checkOffset(bat)
    offset = max(-maxOffset, min(offset, maxOffset))

    normalizedOffset = offset / maxOffset

    if bat == batLeft:
        ballAngle = 0 + normalizedOffset * 45

    elif bat == batRight:
        ballAngle = 180 - normalizedOffset * 45

    return ballAngle
"""

pygame.time.set_timer(TOGGLE_CLICKSTART, 2000) # timer dla napisu CLICK START / FREE PLAY

while running:
    pressedKeys = pygame.key.get_pressed()

    mousex, mousey = pygame.mouse.get_pos()

    # obsluga eventow
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # wychodzenie z gry
        if pressedKeys[pygame.K_LCTRL]:
            running = False

        # otwieranie ustawien
        if pressedKeys[pygame.K_s] and settingsOpen == False:
            settingsOpen = True
        
        
        if settingsOpen and gameStarted == False:
            # zamykanie ustawien
            if pressedKeys[pygame.K_ESCAPE]:
                settingsOpen = False
            
            # przelaczanie trybu gry
            if pressedKeys[pygame.K_m]:
                if mode == "Two-player":
                    mode = "One-player"
                
                elif mode == "One-player":
                    mode = "Two-player"
            
            # przelaczanie predkasci paletek
            if pressedKeys[pygame.K_f]:
                if paddleSpeedMode == "Fast":
                    paddleSpeedMode = "Slow"
                
                elif paddleSpeedMode == "Slow":
                    paddleSpeedMode = "Fast"
            
            # przelaczanie Ball Rotation Mode
            if pressedKeys[pygame.K_b]:
                if ballRotationMode == "Dynamic":
                    ballRotationMode = "Static"
                
                elif ballRotationMode == "Static":
                    ballRotationMode = "Dynamic"
            
            if pressedKeys[pygame.K_a]:
                if ballSpeedMode == "Slow":
                    ballSpeedMode = "Fast"
                
                elif ballSpeedMode == "Fast":
                    ballSpeedMode = "Slow"
        
        # napis CLICK START / FREE PLAY
        if event.type == TOGGLE_CLICKSTART:
            clickStartVisible = not clickStartVisible
            freePlayVisible = not freePlayVisible

        # event staru gry na nacisniecie myszy
        if event.type == pygame.MOUSEBUTTONDOWN:
            if gameEnded:
                resetGame()

            startGame()

        
        # event serwowania pilki
        if event.type == THROW_BALL:
            throwBall()

        # przelaczanie debugu
        if pressedKeys[pygame.K_d]:
            if debug == False:
                debug = True
            
            elif debug == True:
                debug = False


    # rysowanie ekranu
    screen.fill("black")

    # ---BALL---

    # rysowanie ball
    if drawBall:
        pygame.draw.rect(screen, "white", ball)

    # predkosc ball
    if ballSpeedMode == "Slow":
        ballSpeed = 5
    
    elif ballSpeedMode == "Fast":
        ballSpeed = 6
        
    # ruch ball
    ball = ball.move(ballVelX, ballVelY)

    # odbijanie ball

    # na ekranie startowym / koncowym
    if ball.colliderect(wallTop) or ball.colliderect(wallBottom):
            ballVelY *= -1

            if gameStarted == True and gameEnded == False and playSound == True:
                wallSound.stop()
                wallSound.play()

    if gameStarted == False:
        if ball.colliderect(goalLeft) or ball.colliderect(goalRight):
            ballVelX *= -1

    # od paletek

    # STATIC
    if ballRotationMode == "Static":
        # lewa
        if ball.colliderect(paddleLeft):
            if ballVelY > 0 and checkOffset(paddleLeft) < 0:
                ballVelX *= -1
                ballVelY *= -1
        
            elif ballVelY > 0 and checkOffset(paddleLeft) > 0:
                ballVelX *= -1
        
            elif ballVelY < 0 and checkOffset(paddleLeft) > 0:
                ballVelX *= -1
                ballVelY *= -1
            
            elif ballVelY < 0 and checkOffset(paddleLeft) < 0:
                ballVelX *= -1

            if gameStarted == True and playSound == True:
                paddleSound.stop()
                paddleSound.play()
            
        #prawa
        if ball.colliderect(paddleRight):
            if ballVelY > 0 and checkOffset(paddleRight) < 0:
                ballVelX *= -1
                ballVelY *= -1

            elif ballVelY > 0 and checkOffset(paddleRight) > 0 :
                ballVelX *= -1
            
            elif ballVelY < 0 and checkOffset(paddleRight) > 0:
                ballVelX *= -1
                ballVelY *= -1
            
            elif ballVelY < 0 and checkOffset(paddleRight) < 0:
                ballVelX *= -1

            if gameStarted == True and playSound == True:
                paddleSound.stop()
                paddleSound.play()

    # DYNAMIC
    if ballRotationMode == "Dynamic":
        # lewa
        if ball.colliderect(paddleLeft):
            if checkOffset(paddleLeft) >= 40:
                ballAngle = 305

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif checkOffset(paddleLeft) < 40 and checkOffset(paddleLeft) >= 30:
                ballAngle = 315

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif checkOffset(paddleLeft) < 30 and checkOffset(paddleLeft) >= 20:
                ballAngle = 325

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif checkOffset(paddleLeft) < 20 and checkOffset(paddleLeft) >= 10:
                ballAngle = 335

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed

            elif checkOffset(paddleLeft) < 10 and checkOffset(paddleLeft) >= 0:
                ballAngle = 345

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed

            elif checkOffset(paddleLeft) < 0 and checkOffset(paddleLeft) >= -10:
                ballAngle = 15

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed

            elif checkOffset(paddleLeft) < -10 and checkOffset(paddleLeft) >= -20:
                ballAngle = 25

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed

            elif checkOffset(paddleLeft) < -20 and checkOffset(paddleLeft) >= -30:
                ballAngle = 35

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif checkOffset(paddleLeft) < -30 and checkOffset(paddleLeft) >= -40:
                ballAngle = 45

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed

            elif checkOffset(paddleLeft) < -40:
                ballAngle = 55

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed
        
            if gameStarted == True and playSound == True:
                paddleSound.stop()
                paddleSound.play()
            
        # prawa
        if ball.colliderect(paddleRight):
            if checkOffset(paddleRight) >= 40:
                ballAngle = 235

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif checkOffset(paddleRight) < 40 and checkOffset(paddleRight) >= 30:
                ballAngle = 225

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif checkOffset(paddleRight) < 30 and checkOffset(paddleRight) >= 20:
                ballAngle = 215

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif checkOffset(paddleRight) < 20 and checkOffset(paddleRight) >= 10:
                ballAngle = 205

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed

            elif checkOffset(paddleRight) < 10 and checkOffset(paddleRight) >= 0:
                ballAngle = 185

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed

            elif checkOffset(paddleRight) < 0 and checkOffset(paddleRight) >= -10:
                ballAngle = 175

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed

            elif checkOffset(paddleRight) < -10 and checkOffset(paddleRight) >= -20:
                ballAngle = 145

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed

            elif checkOffset(paddleRight) < -20 and checkOffset(paddleRight) >= -30:
                ballAngle = 135

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif checkOffset(paddleRight) < -30 and checkOffset(paddleRight) >= -40:
                ballAngle = 125

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed

            elif checkOffset(paddleRight) < -40:
                ballAngle = 125

                ballAngleRad = math.radians(ballAngle)

                ballVelX = math.cos(ballAngleRad) * ballSpeed
                ballVelY = -math.sin(ballAngleRad) * ballSpeed

            if gameStarted == True and playSound == True:
                    paddleSound.stop()
                    paddleSound.play()


    # wypadanie pilki
    if gameStarted == True:
        # po lewej
        if ball.colliderect(goalLeft):
            if moveBall and gameStarted:
                pointsRight += 1

            drawBall = False
            moveBall = False
            whichPlayer = 0

            if pointsRight == 15:
                gameStarted = False
                drawPaddles = False
                gameEnded = True

            if playSound:
                outSound.stop()
                outSound.play()

            pygame.time.set_timer(THROW_BALL, 2000, loops = 1)

        # po prawej
        if ball.colliderect(goalRight):
            if moveBall and gameStarted:
                pointsLeft += 1

            drawBall = False
            moveBall = False
            whichPlayer = 1

            if pointsLeft == 15:
                gameStarted = False
                drawPaddles = False
                gameEnded = True

            if playSound:
                outSound.stop()
                outSound.play()    

            pygame.time.set_timer(THROW_BALL, 2000, loops = 1)


    """
    # DYNAMIC
    if ballRotationMode == "Dynamic":
    # lewa
        if ball.colliderect(batLeft) and ballVelX < 0:
            ballAngle = dynamicBallRotationAngle(batLeft)
            ballAngleRad = math.radians(ballAngle)

            ballVelX = math.cos(ballAngleRad) * ballSpeed
            ballVelY = -math.sin(ballAngleRad) * ballSpeed  # minus, bo ekran y rośnie w dół

        # prawa paletka
        if ball.colliderect(batRight) and ballVelX > 0:
            ballAngle = dynamicBallRotationAngle(batRight)
            ballAngleRad = math.radians(ballAngle)

            ballVelX = math.cos(ballAngleRad) * ballSpeed  # odbicie w lewo
            ballVelY = -math.sin(ballAngleRad) * ballSpeed
"""

    # ---PALETKI---
    # predkosc paletek
    if paddleSpeedMode == "Fast":
        paddleSpeed = 10
    
    elif paddleSpeedMode == "Slow":
        paddleSpeed = 5

    # rysowanie paletek
    if drawPaddles:
        pygame.draw.rect(screen, "white", paddleLeft)
        pygame.draw.rect(screen, "white", paddleRight)
    
    # ruch paletek
    if gameStarted:
        if mode == "Two-player":
            # lewa
            if pressedKeys[pygame.K_w]:
                paddleLeft = paddleLeft.move(0, -paddleSpeed)
            
            elif pressedKeys[pygame.K_s]:
                paddleLeft = paddleLeft.move(0, paddleSpeed)

            # prawa
            if pressedKeys[pygame.K_i]:
                paddleRight = paddleRight.move(0, -paddleSpeed)
            
            elif pressedKeys[pygame.K_k]:
                paddleRight = paddleRight.move(0, paddleSpeed)
            
        if mode == "One-player":
            # lewa
            paddleLeft.centery = mousey

            # prawa
            if drawBall == True and ballRotationMode == "Static":
                paddleRight.centery = ball.centery
            
            if drawBall == True and ballRotationMode == "Dynamic":
                paddleRight.centery = ball.centery

                if ball.centerx > 1350:
                    paddleRight.centery = ball.centery + random.randint(-48, 48)

    # ---SCIANY I GOLE---

    # rysowanie scian i goli
    pygame.draw.rect(screen, "black", goalLeft)
    pygame.draw.rect(screen, "black", goalRight)
    pygame.draw.rect(screen, "black", wallTop)
    pygame.draw.rect(screen, "black", wallBottom)

    # ---PRZERYWANA KRESKA---

    # rysowanie przerywanej kreski
    for y in range(0, HEIGHT, dashLenght + gap):
        pygame.draw.line(screen, "white", (x, y), (x, y + gap), 3)

    # ---USTAWIENIA---

    # teksty ustawien
    if gameStarted == False:
        if settingsOpen == False:
            settingsText = freesansbold.render("SETTINGS", True, "white")
        
            screen.blit(settingsText, [120, 1000])
    
        elif settingsOpen == True:
            ballRotationText = freesansbold.render("Ball rotation: {}".format(ballRotationMode), True, "white")
            ballRotationToggleText = freesansbold.render("B to toggle", True, "white")
            modeText = freesansbold.render("Mode: {}".format(mode), True, "white")
            modeToggleText = freesansbold.render("M to toggle", True, "white")
            paddleSpeedText = freesansbold.render("Paddle speed: {}".format(paddleSpeedMode), True, "white")
            paddleSpeedToggleText = freesansbold.render("F to toggle", True, "white")
            ballSpeedText = freesansbold.render("Ball speed: {}".format(ballSpeedMode), True, "white")
            ballSpeedToggleText = freesansbold.render("A to toggle", True, "white")

            screen.blit(ballRotationText, [85, 815])
            screen.blit(ballRotationToggleText, [85, 845])
            screen.blit(modeText, [85, 875])
            screen.blit(modeToggleText, [85, 905])
            screen.blit(paddleSpeedText, [85, 935])
            screen.blit(paddleSpeedToggleText, [85, 965])
            screen.blit(ballSpeedText, [85, 995])
            screen.blit(ballSpeedToggleText, [85, 1025])

    # ---STATYSTYKI---
    
    # punkty
    pointsLeftText = atari.render("{}".format(pointsLeft), True, "white")
    pointsRightText = atari.render("{}".format(pointsRight), True, "white")

    screen.blit(pointsLeftText, [685, 10])
    screen.blit(pointsRightText, [1175, 10])

    # tekst CLICK START / FREE PLAY
    if gameStarted == False:
        if clickStartVisible:
            clickStartText = freesansbold.render("CLICK START", True, "white")

            screen.blit(clickStartText, [1600, 1000])

        elif freePlayVisible:
            freePlayText = freesansbold.render("FREE PLAY", True, "white")

            screen.blit(freePlayText, [1615, 1000])

    # teksty debugu
    if debug == True:
        text1 = freesansbold.render("A: {}; X: {}; Y: {}".format(ballAngle, round(ballVelX, 2), round(ballVelY, 2)), True, "white")
        text2 = freesansbold.render("PaddleSpeed: {}; BallSpeed: {}".format(paddleSpeedMode, ballSpeedMode), True, "white")
        text3 = freesansbold.render("Mode: {}".format(mode), True, "white")
        text4 = freesansbold.render("Rotation: {}".format(ballRotationMode), True, "white")
        text5 = freesansbold.render("FPS: {}".format(round(pygame.time.Clock.get_fps(clock), 2)), True, "white")

        screen.blit(text1, [0, 0])
        screen.blit(text2, [0, 30])
        screen.blit(text3, [0, 60])
        screen.blit(text4, [0, 90])
        screen.blit(text5, [0, 120])

    pygame.display.flip()

    clock.tick(0)