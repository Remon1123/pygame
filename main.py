#DEBUG-MODE, if True prints some usefull statements in the command line
DEBUG=False

# Here we import the required modules
import pygame
import random
from cardsfile import *
from pathlib import Path
from sys import exit

dir = Path(__file__).resolve().parent
if DEBUG:
    print(dir)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((950,550))
pygame.display.set_caption('SET')
logopath = dir / "Pictures/Logo.png"
logo=pygame.image.load(logopath)
pygame.display.set_icon(logo)
clock=pygame.time.Clock()

# Giving some variables beginvalues
score=0
GameOver=False
inputdelay=0
NoSetsTextTime=0
highscore = 0
timesinceset = 0
displaytime = 0
computerscore = 0
# Setting the standard font
Font=pygame.font.SysFont('Arial',16)

#initializing all the RemainingCards (Function from cardsfile.py)
InitializeRemainingCards()

# This function retrieves a random card that hasnt been used yet
def getcard():
    if len(RemainingCards)>1:
        randomnumber=random.randint(0,len(RemainingCards)-1)
    elif len(RemainingCards)==1:
        randomnumber=0
    temp=RemainingCards[randomnumber]
    RemainingCards.pop(randomnumber)
    return temp

# This function checks for three selectes cards whether they form a set
# It includes a dictionary that makes the card checking easier
def Set_Check(Card1,Card2,Card3): 
    propertiescheck = {0:Table_Cards[Card1].amount==Table_Cards[Card2].amount and Table_Cards[Card1].amount==Table_Cards[Card3].amount and Table_Cards[Card2].amount==Table_Cards[Card3].amount, 1:Table_Cards[Card1].amount!=Table_Cards[Card2].amount and Table_Cards[Card1].amount!=Table_Cards[Card3].amount and Table_Cards[Card2].amount!=Table_Cards[Card3].amount,2:Table_Cards[Card1].fill==Table_Cards[Card2].fill and Table_Cards[Card1].fill==Table_Cards[Card3].fill and Table_Cards[Card2].fill==Table_Cards[Card3].fill,3:Table_Cards[Card1].fill!=Table_Cards[Card2].fill and Table_Cards[Card1].fill!=Table_Cards[Card3].fill and Table_Cards[Card2].fill!=Table_Cards[Card3].fill,4:Table_Cards[Card1].shape==Table_Cards[Card2].shape and Table_Cards[Card1].shape==Table_Cards[Card3].shape and Table_Cards[Card2].shape==Table_Cards[Card3].shape,5:Table_Cards[Card1].shape!=Table_Cards[Card2].shape and Table_Cards[Card1].shape!=Table_Cards[Card3].shape and Table_Cards[Card2].shape!=Table_Cards[Card3].shape,6:Table_Cards[Card1].color==Table_Cards[Card2].color and Table_Cards[Card1].color==Table_Cards[Card3].color and Table_Cards[Card2].color==Table_Cards[Card3].color,7:Table_Cards[Card1].color!=Table_Cards[Card2].color and Table_Cards[Card1].color!=Table_Cards[Card3].color and Table_Cards[Card2].color!=Table_Cards[Card3].color}

    # This loop checks whether all four properties are the same or all different.
    # If this condition is satisfied the boolean True is returned and otherwise the boolean False is returned.
    for i in range(0,8,2):
        if propertiescheck[i]:
            i=i
        elif propertiescheck[i+1]:
            i=i
        else:
            return False
    if DEBUG:
        print (chr(Card1+97) +" "+ str(Table_Cards[Card1]))
        print (chr(Card2+97) +" "+  str(Table_Cards[Card2]))
        print (chr(Card3+97) +" "+ str(Table_Cards[Card3]))
        print(True)
    return True

# This function makes a list of all the current sets
# from the twelve cards on the table
All_Sets=[]
def Get_All_Sets():
    for Card1 in range (len(Table_Cards)-2):
        for Card2 in range(Card1+1,len(Table_Cards)-1):
            for Card3 in range(Card2+1,len(Table_Cards)):
                if Set_Check(Card1,Card2,Card3):
                    All_Sets.append([Card1,Card2,Card3])

# This function initializes the table of twelve cards
Table_Cards=[]
def InitializeTable():
    for i in range(12):
        Table_Cards.append(getcard())
    Get_All_Sets()
InitializeTable()

#List that has all the selected RemainingCards
SET_SelectorList=[]

# Checking whether the selected cards are a set
# If so and there are still cards left, the table gets refilled
# Otherwise the cards from the set are just popped
# the score score gets returned as wel
def Set_Try(s,a,b,c):
    if Set_Check(a,b,c):
        global timesinceset
        timesinceset = 0
        if len(RemainingCards)>0:
            Table_Cards[a]=getcard()
            Table_Cards[b]=getcard()
            Table_Cards[c]=getcard()
        else:
            Table_Cards.pop(a)
            Table_Cards.pop(b-1)
            Table_Cards.pop(c-2)
        All_Sets.clear()
        Get_All_Sets()
        return s+1
    else:
        return s

# This def gets as input the set_selectorlist,
# as output it gives a random card that is part of a set

def hint():
    a = random.choice(All_Sets)
    b = random.choice(a)
    return ([b])

# A keys dictionary which makes checking all the inputs of the characters a to l easier
keysdictionary={0:pygame.K_a,1:pygame.K_b,2:pygame.K_c,3:pygame.K_d,4:pygame.K_e,5:pygame.K_f,6:pygame.K_g,7:pygame.K_h,8:pygame.K_i,9:pygame.K_j,10:pygame.K_k,11:pygame.K_l}     

# A dictionary with the pictures for easy medium and hard
difficulties = {0:dir / 'Pictures/Easy.png',1:dir / 'Pictures/Medium.png',2:dir / 'Pictures/Hard.png'}

# a def with a loop in which you select the difficulty you want, easy, medium or hard
def difficultyselector(difficulties):
    while True: 
        gameboard = pygame.Surface((950,550))
        gameboard.fill(pygame.Color(152, 155, 156))
        inputkeys=pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
        if inputkeys[pygame.K_a]:
            difficulty = 40
            inputdelay = 60
            break
        if inputkeys[pygame.K_b]:
            difficulty = 25
            inputdelay = 60
            break
        if inputkeys[pygame.K_c]:
            difficulty = 15
            inputdelay = 60
            break
        for i in range(3):
            temporary_surface = pygame.image.load(difficulties[i])
            temporary_surface = pygame.transform.scale(temporary_surface, (300,150))
            cardcharacter = Font.render(chr(97+i),False,(0,0,0))
            temporary_surface.blit(cardcharacter,(280,120))
            gameboard.blit(temporary_surface,(25+300*(i%6),200))
        Selector = Font.render("Please select a difficulty", False , (0,0,0))
        gameboard.blit(Selector,(475-Selector.get_width()//2,25))
        screen.blit(gameboard,(0,0))
        pygame.display.update()
        clock.tick(60)
    return(difficulty)

difficulty = difficultyselector(difficulties)

# This is the main game loop where the game is displayed
# and all necesary functions are called
while True:
    gameboard = pygame.Surface((950,550))
    gameboard.fill(pygame.Color(152, 155, 156))

    #Checking if the program is closed or not
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
    inputkeys=pygame.key.get_pressed()

    #checking if the keys from a to l are pressed with a delay of 10 frames
    if inputdelay==0:
        if len(SET_SelectorList)<3:
            for i in range(12):
                if inputkeys[keysdictionary[i]]:
                    if SET_SelectorList.count(i)<1:
                        SET_SelectorList.append(i)
                        inputdelay=10
                        break
    else:
        inputdelay-=1
    
    # this makes sure that the set is checked when enter is pressd
    # and that a set is being checked only when three cards are selected
    # the score is updated and the list of selected cars is emptied
    # if you try an invalid set, the computer gains a score and a set is removed
    if inputkeys[pygame.K_RETURN]: 
        if len(SET_SelectorList)==3: 
            temp = score
            score=Set_Try(score,SET_SelectorList[0],SET_SelectorList[1],SET_SelectorList[2])
            if score == temp:
                randomset = random.choice(All_Sets)
                computerscore = Set_Try(computerscore,randomset[0],randomset[1],randomset[2])
            SET_SelectorList=[]

    # The selected card is undone by clicking backspace
    if inputkeys[pygame.K_BACKSPACE]:
        SET_SelectorList=[]

    # If there are no sets but there are still cards left
    # a counter is set to 60
    # Otherwise its gameover
    if len(All_Sets)==0:
        if len(RemainingCards)>0:
            if NoSetsTextTime==0:
                NoSetsTextTime=60
        else:
            GameOver=True
    
    # when there are no sets this is displayed
    # the counter dicreases to zero and then the top layer is refilled with new cards
    # Now the table is checked again on sets

    if NoSetsTextTime>0:
        NoSets = Font.render("No Sets Available!",False,(0,0,0))
        gameboard.blit(NoSets,(475-NoSets.get_width()//2,25-NoSets.get_height()//2))
        NoSetsTextTime-=1
        if NoSetsTextTime==0:
            for i in range (0,12,4):
                a=random.randint(0+i,3+i)
                if DEBUG:
                    print(a)
                    print(Table_Cards[a])
                Table_Cards[a]=getcard()
                if DEBUG:
                    print(Table_Cards[a])
            Get_All_Sets()
    
    #if you take longer then a certain amount of time(determined by the difficulty) you lose too the computer
    #Furthemore then 3 cards are removed which formed a set and 3 new cards are added

    timesinceset += 1
    if timesinceset > difficulty * 60:
        displaytime = 60
        randomset = random.choice(All_Sets)
        SET_SelectorList = []
        computerscore = Set_Try(computerscore,randomset[0],randomset[1],randomset[2])
    
    #displays the "You took too long" for a second

    if displaytime > 0:
        displaytime -= 1
        Computerwon = Font.render("You took too long",False,(0,0,0))
        gameboard.blit(Computerwon,(475-Computerwon.get_width()//2,25-Computerwon.get_height()//2))
    
    # If you're struggling to find a set you can press spacebar to get a hint,
    # then the game will give you a card that is part of a set

    if GameOver == False and len(SET_SelectorList) == 0:
        if inputkeys[pygame.K_SPACE]:
            SET_SelectorList = hint()

    # if gameover this is displayed and space enables player to restart
    if GameOver == True:
        GameOverText = Font.render("Game Over! Press the Spacebar to play again.",False,(0,0,0))
        gameboard.blit(GameOverText,(475-GameOverText.get_width()//2,25-GameOverText.get_height()//2))
        if inputkeys[pygame.K_SPACE]:
            GameOver=False
            difficulty = difficultyselector(difficulties)
            Table_Cards=[]
            InitializeRemainingCards()
            InitializeTable()
            score=0
            computerscore=0

    # Adding the Table_Cards to the screen
    for i in range(len(Table_Cards)):
        temporary_surface = pygame.image.load(Table_Cards[i].filename)
        cardcharacter = Font.render(chr(97+i),False,(0,0,0))
        temporary_surface.blit(cardcharacter,(80,180))
        gameboard.blit(temporary_surface,(50+150*(i%6),50+250*(i//6)))

    # Adding the gameboard to the screen
    # Score,highscore and computerscore  are displayed and the highscore is updated
    screen.blit(gameboard,(0,0))
    scoretext=Font.render("score="+str(score),False,(0,0,0))
    screen.blit(scoretext,(20,20))
    if score>highscore:
        highscore=score
    highscoretext=Font.render("highscore="+str(highscore),False,(0,0,0))
    screen.blit(highscoretext,(930-highscoretext.get_width(),20))
    computerscoretext = Font.render("computerscore="+str(computerscore),False,(0,0,0))
    screen.blit(computerscoretext,(20,8))
    hinttext = Font.render("Press spacebar for a hint",False,(0,0,0))

    # Displays that you can press spacebar for a hint,
    # if and only if the game is not over and you've not selected anything 

    if GameOver == False and len(SET_SelectorList) == 0:
        screen.blit(hinttext,(20,520))
    
    for i in SET_SelectorList:
        temporary_surface = pygame.Surface((100,200))
        temporary_surface.fill(pygame.Color(255,255,0))
        temporary_surface.set_alpha(64)
        screen.blit(temporary_surface,(50+150*(i%6),50+250*(i//6)))
    

    pygame.display.update()
    clock.tick(60)