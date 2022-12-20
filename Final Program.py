
# Astroids Game
# pygame initialisation
import pygame
import random
pygame.font.init()
pygame.init()
#Defines Screen Size
screen_width = 1920
screen_bottom = 1080
#Sets Screen Size
screen = pygame.display.set_mode((screen_width,screen_bottom))
clock = pygame.time.Clock()
#Sets Name of game as Asteroids
pygame.display.set_caption("Asteroid Defense Game")


#Global------------------------------------------------------------------------
game_playing = True
#===2-d Array====
#astEntire_array is a 2-d arrayof asterods
#arrays get appended in the asteroids spawn function
astEntire_array = []
bullets_array = []
current_time = 0
time_until  = 180
total_score = 0
total_lives = 3
already_pressed = False
already_pressed_pause = False
stary = pygame.image.load("background_stars.png").convert_alpha()
stary = pygame.transform.scale(stary,(screen_width,screen_bottom))
game_over_screen = pygame.image.load("game_over_screen.png").convert_alpha()
game_over_screen = pygame.transform.scale(game_over_screen,(screen_width,screen_bottom))
#------------------------------------------------------------------------------

#Creats a record called Ship
class Ship:

    #Constructor, defines the properties used within the method in the record
    def __init__(self):
        #Loads the png image file to be used for the ship
        self.image = pygame.image.load("Asteroid_blaster3.png").convert_alpha()
        #Defines the ships x
        #Starts in the middle
        self.x = (screen_width/2)
        #Defines the ships y
        self.y = screen_bottom - self.image.get_height()



    #Creats a method called draw
    def draw(self):
        #Draws ships corrosponding to the position, which was defined in the constuctor
        screen.blit(self.image,(self.x,self.y))


#Creates a record called Bullet
class Bullet:

    #Constructor, defines the properties used within the method in the record
    #Also passes in the players/ships x and y
    def __init__(self,x,y):
        #Loads the png image file to be used for the bullet
        self.image = pygame.image.load("blue_bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(20,40))
        #Defines the bullets x as the x passed in
        self.x = x
        #Defines the bullets y as the y passed in
        self.y = y
        #Defines the the speed of the bullet to be used later on
        self.speed = 10
        #Defines the right side to be used later on
        self.rightside = 0

    #Creates a procedure called update
    def update_position(self):
        #Takes the bullets speed from the bullets y value
        #which causes the bullet to move upwards
        self.y -= self.speed

    #Creats a method called draw
    def draw(self):
        #Draws ships corrosponding to the positions(x,y) value
        screen.blit(self.image,(self.x,self.y))

    #Creates a procedure called update
    def collision(self):
        #Rightside is the bullet images bottom + the bullets x position
        self.rightside = self.image.get_height() +  self.x

#Creats a record called Asteroid
class Asteroid:

    #Constructor, defines the properties used within the method in the record
    #Also passes in the x,i,j,hidden
    def __init__(self,x,ast_num,random_num,hidden):

        self.random_num = random_num
        self.vx = 0
        #Defines vy as as a random real number between 0.5 and 2.0
        self.vy = 1
        #Defines hidden as the hidden passed in
        self.hidden = hidden
        #Loads the png image file to be used for the Asteroid and uses the i and j
        #property to determine what png will be choosen
        self.Ast = pygame.image.load("Asteroid_"+str(self.random_num) + str(ast_num)+".png").convert_alpha()
        #Defines bottom as 0 which will be changed later on in the program
        self.bottom = 0
        #Defines rightside as 0 which will be changed later on in the program
        self.rightside = self.Ast.get_width()
        #Defines the x as the x passed in
        self.x = x - self.rightside
        self.y = 0 - self.Ast.get_height()

    #Creats a procedure called draw
    def draw(self):
        #When hidden == False DO
        if self.hidden == False:
            #Draws asterids corrosponding to the x and y properties
            screen.blit(self.Ast,(self.x,self.y))
##            pygame.draw.line(screen, (100, 200, 255), (self.x, self.bottom), (self.rightside, self.bottom), 1)

    #Creates a procedure called move
    def move(self):
        #When hidden == False DO
        if self.hidden == False:
            #Changes the y value by its y value plus its vy value
            #which causes the Asteroid image to be drawn slightly further down
            self.y = self.y +self.vy
            self.x = self.x + self.vx

    #Creates a procedure called collison
    def collision(self):
        #Sets the bottom property to the asteroid png images bottom + the asteroids y
        self.bottom = self.Ast.get_height() +  self.y - 20
        #Sets the rightside property to the asteroid png images width
        self.rightside = self.Ast.get_width() + self.x
        if self.x <= 0:
            self.x = 0

player = Ship()

########################################################################################################################################
########################################################################################################################################
#===2-d Array====
def asteroids_spawn(current_time,time_until,astEntire_array):
    #--asteroid_spawn---
    #sets an empty array to be filled with asterid classes
    #and will ultimatly be appended to astEntire_array
    astG_array = []
    current_time += 1
    #time_until == 60 at start
    #Every time the program cycles time_until will decrease
    #meaning over time asteroids will spawn in more rapidly
    time_until -= 0.02
    if current_time >= time_until:
        #This will create a new set of asteroids
        #Their is 4 random parent asteroids that it could be
        #This determine which one it will be
        randoms = str(random.randint(1,4))
        #Parent asteroid
        astG_array.append(Asteroid(random.randint(1,screen_width),1,randoms,False))
        #Child asteroid 1 is decided by the parent asteroid
        astG_array.append(Asteroid(random.randint(1,screen_width),2,randoms,True))
        #Child asteroid 2 is decided by the parent asteroid
        astG_array.append(Asteroid(random.randint(1,screen_width),3,randoms,True))
        astEntire_array.append(astG_array)
        #Resets current_time to 0
        current_time = 0
    return current_time,time_until,astEntire_array

########################################################################################################################################
########################################################################################################################################
def key_presses(already_pressed,bullets_array):
     #---presskeys---
    #Creats a varible that calls the pygame method "key"
    key = pygame.key.get_pressed()

    #When "a" key is pressed DO
    if key[pygame.K_a]:
        #Deducts 10 from the ships x
        #meaning when its drawn again it will be drawn more to the left
        player.x -= 15

    #When "d" key is pressed DO
    if key[pygame.K_d]:
        #Adds 10 to the ships x
        #meaning when its drawn again it will be drawn more to the right
        player.x += 15

    #When "SPACE" key is pressed AND already_pressed == True DO
    if already_pressed == False and key[pygame.K_SPACE]:
        #Sets the boolean already_pressed to false
        already_pressed = True
        #Calls the bullets_spawn procedure that is created out with the ship record
        #Creats a procedure called bullets_spawn
        #To get bullet x, I added the ships x position + the shps width/2
        bullet = Bullet((player.x + (player.image.get_width()/2)),(player.y))
        bullets_array.append(bullet)


    elif already_pressed == True and key[pygame.K_SPACE] == False:
        already_pressed = False

    return already_pressed,bullets_array

########################################################################################################################################
########################################################################################################################################
def collision(bullets_array,astEntire_array,total_score):
    loop_end = False
    #---collisions---
    for i in range(len(bullets_array)):
        for j in range(len(astEntire_array)):

            #1.Checks if a parent asteroid is hidden if not
            #2.checks if the bullets y is less than or equal to the bottom of the asteroid
            #(the bottom being its y + its image height)
            #3.checks if the bullets x is less than or equal to the right side of the asteroid
            #(the rightside being its x + its image width)
            #4.checks if the bullets rightside is more than or equal to the x of the asteroid
            #(the rightside being its x + its image width)
            if astEntire_array[j][0].hidden == False and \
            bullets_array[i].y <= astEntire_array[j][0].bottom and \
            bullets_array[i].x <= astEntire_array[j][0].rightside and \
            bullets_array[i].rightside >= astEntire_array[j][0].x:

                #Sets the parent aseroid to hidden
                astEntire_array[j][0].hidden = True

                #Sets the first child aseroid hidden
                astEntire_array[j][1].hidden = False
                #Sets first child aseroid the same x as the parent
                astEntire_array[j][1].x = astEntire_array[j][0].x
                #Sets the new horizontal velocity
                astEntire_array[j][1].vx = -0.5
                #Sets first child aseroid the same y as the parent
                astEntire_array[j][1].y = astEntire_array[j][0].y

                #Sets the second child aseroid to hidden
                astEntire_array[j][2].hidden = False
                #Offsets the second child asteroid so it looks like they've been split in half
                astEntire_array[j][2].x = astEntire_array[j][0].x + astEntire_array[j][1].Ast.get_width()
                #Sets the new horizontal velocity
                astEntire_array[j][2].vx = 0.5
                #Sets second child aseroid the same y as the parent
                astEntire_array[j][2].y = astEntire_array[j][0].y

                #Increases score by 10 every successful collision
                total_score += 10
                #Deletes the bullet that collided with the asteroid
                bullets_array.pop(i)
                #Sets the loop end to true so that it can later end the entire i loop to avoid a looping error
                loop_end = True
                #Ends the j loop to avoid index out of range error
                break

            #1.Checks if the first set of child asteroids are hidden if not
            #2.checks if the bullets y is less than or equal to the bottom of the asteroid
            #(the bottom being its y + its image height)
            #3.checks if the bullets x is less than or equal to the right side of the asteroid
            #(the rightside being its x + its image width)
            #4.checks if the bullets rightside is more than or equal to the x of the asteroid
            #(the rightside being its x + its image width)
            elif astEntire_array[j][1].hidden == False and \
            bullets_array[i].y <= astEntire_array[j][1].bottom and \
            bullets_array[i].x <= astEntire_array[j][1].rightside and \
            bullets_array[i].rightside >= astEntire_array[j][1].x:

                #Sets hidden back to true if bullet collides with it
                astEntire_array[j][1].hidden = True
                #Increases score by 10 every successful collision
                total_score += 10
                #Deletes the bullet that collided with the asteroid
                bullets_array.pop(i)
                #Sets the loop end to true so that it can later end the entire i loop to avoid a looping error
                loop_end = True
                #Ends the j loop to avoid index out of range error
                break

            #1.Checks if the second set of child asteroids are hidden if not
            #2.checks if the bullets y is less than or equal to the bottom of the asteroid
            #(the bottom being its y + its image height)
            #3.checks if the bullets x is less than or equal to the right side of the asteroid
            #(the rightside being its x + its image width)
            #4.checks if the bullets rightside is more than or equal to the x of the asteroid
            #(the rightside being its x + its image width)
            elif astEntire_array[j][2].hidden == False and \
            bullets_array[i].y <= astEntire_array[j][2].bottom and \
            bullets_array[i].x <= astEntire_array[j][2].rightside and \
            bullets_array[i].rightside >= astEntire_array[j][2].x:

                #Sets hidden back to true if bullet collides with it
                astEntire_array[j][2].hidden = True
                #Increases score by 10 every successful collision
                total_score += 10
                #Deletes the bullet that collided with the asteroid
                bullets_array.pop(i)
                #Sets the loop end to true so that it can later end the entire i loop to avoid a looping error
                loop_end = True
                #Ends the j loop to avoid index out of range error
                break

        #Will end the i loop if loop end == true
        if loop_end == True:
            break

    return bullets_array,astEntire_array,total_score

########################################################################################################################################
########################################################################################################################################
def lose_lives(astEntire_array,total_lives):
    #This procedure will take one away from lives when an asteroid goes off screen
    for m in range(len(astEntire_array)):
        for n in range(len(astEntire_array[m])):
            if astEntire_array[m][n].y >= screen_bottom:
                #Remove 1 from total lives
                total_lives -= 1
                for i in range(3):
                    astEntire_array[m][i].hidden = True
                break
    return total_lives

########################################################################################################################################
########################################################################################################################################
def bullet_delete():
    #Delets bullet when it reaches top
    for i in range(len(bullets_array)):
        if bullets_array[i].y <= 0:
            #Delets that item in the array
            bullets_array.pop(i)
            break




########################################################################################################################################
########################################################################################################################################
def game_text(total_lives,total_score):
    #TEXT
    myfont = pygame.font.SysFont('Ultra Serif SF', 36)
    score_text = myfont.render(('Score:'+ str(total_score)), False, (255, 255, 255))
    lives_text = myfont.render(('Lives:'+ str(total_lives)), False, (255, 255, 255))

    #Writes the text to the screen
    screen.blit(score_text,(0,0))
    screen.blit(lives_text,(0,30))

########################################################################################################################################
########################################################################################################################################
def events(astEntire_array,bullets_array):
    #Draws player on screen
    player.draw()

    #Runs bullets basic functions
    for i in range(len(bullets_array)):
        bullets_array[i].update_position()
        bullets_array[i].draw()
        bullets_array[i].collision()

        #---asteroids_events---
    #Runs asteroids basic functions
    for j in range(len(astEntire_array)):
        #required to loop through each item in the array
        #1 parent 2 children for each array
        for i in range(3):
            astEntire_array[j][i].move()
            astEntire_array[j][i].collision()
            astEntire_array[j][i].draw()

    #Dels asteroid if all set true
    for i in range(len(astEntire_array)):
        if astEntire_array[i][0].hidden == True and \
        astEntire_array[i][1].hidden == True and \
        astEntire_array[i][2].hidden == True:
            astEntire_array.pop(i)
            break

########################################################################################################################################
########################################################################################################################################
def read_data_from_file():
    #<-----HIGHSCORE TEXT FILE CREATOR----->
    scoreboard_array = []
    #LeaderBoard - Saving data to file
    #1.--READ DATA--
    file = open("leaderboard.txt", "r")
    # Read each line and seperate out values using ","
    for line in file:
        # Removes return value
        line = line.strip()
        # Splits Values by commas
        name,each_score = line.split(",")
        each_score = int(each_score)
        #Save each line into a 2d array
        array = [name,each_score]
        scoreboard_array.append(array)
    file.close()

    return scoreboard_array

########################################################################################################################################
########################################################################################################################################
def name_and_score(scoreboard_array,total_score):
    #2--Input and save name--
    name = input(str("Insert name: "))
    while len(name) > 4 or len(name) <4:
        name = input(str("Insert name that is 4 characters long: "))
    array = [name,total_score]
    scoreboard_array.append(array)

    return scoreboard_array

########################################################################################################################################
########################################################################################################################################
#===BUBBLE-SORT====
def bubblesort_data(scoreboard_array):
    #3--SORT THE DATA--
    if len(scoreboard_array) > 2:

        # Repeat the sort code for all pos in array
        for outer in range(len(scoreboard_array)-1, 0, -1):
            # Loops through array to be sorted
            for i in range(outer):
                # If current array item is bigger than
                if scoreboard_array[i][1] < scoreboard_array[i+1][1]:
                    # Swap using temp var
                    temp_swap = scoreboard_array[i]
                    scoreboard_array[i] = scoreboard_array[i+1]
                    scoreboard_array[i+1] = temp_swap
    return scoreboard_array

########################################################################################################################################
########################################################################################################################################
def write_data_from_file(scoreboard_array):
    #4.--Save highscores to file--
    # Open the file to write
    file = open("leaderboard.txt", "w")
    for i in range(len(scoreboard_array)):
        # Write the data score array to the text file
        file.write((scoreboard_array[i][0]))
        file.write((","))
        file.write(str(scoreboard_array[i][1]))
        file.write("\n")
        # Close the text file
    file.close()
    return scoreboard_array

########################################################################################################################################
########################################################################################################################################
def paused(already_pressed_pause,game_playing):
    key = pygame.key.get_pressed()
    if already_pressed_pause == False and key[pygame.K_e]:
        #Sets the boolean already_pressed to false
        already_pressed_pause = True
        #Calls the bullets_spawn procedure that is created out with the ship record
        #Creats a procedure called bullets_spawn
        pause = True

        while pause == True and game_playing:
            key = pygame.key.get_pressed()

            if already_pressed_pause == True and key[pygame.K_e] == False:
                already_pressed_pause = False

            if key[pygame.K_e] and already_pressed_pause == False:
                already_pressed_pause = True
                pause = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_playing = False

    elif already_pressed_pause == True and key[pygame.K_e] == False:
        already_pressed_pause = False


    return already_pressed_pause,game_playing

#----------------------------------------------------------------------------------------------------------------------------------------
#First while starting the program begins
while game_playing:
# If the player quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_playing = False

    #Updates screen !important!
    pygame.display.flip()
    #The fps -max30
    clock.tick(30)

    #Draws background first
    screen.blit(stary,(0,0))

    #Spawns asteroids if ready
    current_time,time_until,astEntire_array = asteroids_spawn(current_time,time_until,astEntire_array)

    #Inputs for game
    already_pressed,bullets_array = key_presses(already_pressed,bullets_array)

    #This deals with the collsion between the bullets and the asteroids
    bullets_array,astEntire_array,total_score = collision(bullets_array,astEntire_array,total_score)

    #When asteroids reach bottom of scree a life is lost
    total_lives = lose_lives(astEntire_array,total_lives)

    #Delets a for the array if it reaches top of screen
    bullet_delete()

    #Displays the players current lives and score on screen
    game_text(total_lives,total_score)

    #Runs all the events/methods for the classes
    events(astEntire_array,bullets_array)

    already_pressed_pause,game_playing = paused(already_pressed_pause,game_playing)

    #When the lives reaches the following will run
    if total_lives <= 0:

        scoreboard_array = read_data_from_file()

        scoreboard_array = name_and_score(scoreboard_array,total_score)

        scoreboard_array = bubblesort_data(scoreboard_array)

        write_data_from_file(scoreboard_array)

        #Game over Screen
        while total_lives <= 0 and game_playing:
            screen.blit(game_over_screen,(0,0))
            middle = 250

            #---TEXT---
            for i in range(4):
                if i < len(scoreboard_array):
                    myfont = pygame.font.SysFont('Ultra Serif SF', 36)
                    allscore_text = myfont.render(str(scoreboard_array[i][0]) + "      " + str(scoreboard_array[i][1]), False, (0, 0, 0))
                    middle += 50
                    #Writes the text to the screen
                    screen.blit(allscore_text,((screen_width/2)-120,middle))

            pygame.display.flip()
            # If the player quits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_playing = False

#---------------------------------------------------------------------------------------------------------------------------------------------


pygame.quit()

