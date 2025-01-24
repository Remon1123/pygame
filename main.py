# Here we import the required modules
import pygame
import random
from cardsfile import *
from pathlib import Path
from sys import exit

dir = Path(__file__).resolve().parent
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

# Setting the standard font
Font=pygame.font.SysFont('Arial',16)

# Initializing all the RemainingCards
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

# This function initializes the table of twelve cards
Table_Cards=[]
def InitializeTable():
    for i in range(12):
        Table_Cards.append(getcard())
InitializeTable()

# This function checks for three selectes cards whether they form a set
# It includes a dictionary that makes the card checking easier
def Set_Check(Kaart1,Kaart2,Kaart3): 
    propertiescheck = { 
    0:Table_Cards[Kaart1].amount==Table_Cards[Kaart2].amount and Table_Cards[Kaart1].amount==Table_Cards[Kaart3].amount and Table_Cards[Kaart2].amount==Table_Cards[Kaart3].amount, 
    1:Table_Cards[Kaart1].amount!=Table_Cards[Kaart2].amount and Table_Cards[Kaart1].amount!=Table_Cards[Kaart3].amount and Table_Cards[Kaart2].amount!=Table_Cards[Kaart3].amount,
    2:Table_Cards[Kaart1].fill==Table_Cards[Kaart2].fill and Table_Cards[Kaart1].fill==Table_Cards[Kaart3].fill and Table_Cards[Kaart2].fill==Table_Cards[Kaart3].fill,
    3:Table_Cards[Kaart1].fill!=Table_Cards[Kaart2].fill and Table_Cards[Kaart1].fill!=Table_Cards[Kaart3].fill and Table_Cards[Kaart2].fill!=Table_Cards[Kaart3].fill,
    4:Table_Cards[Kaart1].shape==Table_Cards[Kaart2].shape and Table_Cards[Kaart1].shape==Table_Cards[Kaart3].shape and Table_Cards[Kaart2].shape==Table_Cards[Kaart3].shape,
    5:Table_Cards[Kaart1].shape!=Table_Cards[Kaart2].shape and Table_Cards[Kaart1].shape!=Table_Cards[Kaart3].shape and Table_Cards[Kaart2].shape!=Table_Cards[Kaart3].shape,
    6:Table_Cards[Kaart1].color==Table_Cards[Kaart2].color and Table_Cards[Kaart1].color==Table_Cards[Kaart3].color and Table_Cards[Kaart2].color==Table_Cards[Kaart3].color,
    7:Table_Cards[Kaart1].color!=Table_Cards[Kaart2].color and Table_Cards[Kaart1].color!=Table_Cards[Kaart3].color and Table_Cards[Kaart2].color!=Table_Cards[Kaart3].color
    }

    # This loop checks whether all four properties are the same or all different.
    # If this condition is satisfied the boolian True is returned and otherwise the boolian False is returned.
    for i in range(0,8,2):
        if propertiescheck[i]:
            i=i
        elif propertiescheck[i+1]:
            i=i
        else:
            return False
    return True

# This function makes a list of all the current sets
# from the twelve cards on the table
All_Sets=[]
def Get_Sets():
    for Kaart1 in range (len(Table_Cards)-2):
        for Kaart2 in range(Kaart1+1,len(Table_Cards)-1):
            for Kaart3 in range(Kaart2+1,len(Table_Cards)):
                if Set_Check(Kaart1,Kaart2,Kaart3):
                    All_Sets.append([Kaart1,Kaart2,Kaart3])
Get_Sets()

#List that has all the selected RemainingCards
SET_SelectorList=[]

# Checking whether the selected cards are a set
# If so and there are still cards left, the table gets refilled
# Otherwise the cards from the set are just popped
# the score score gets returned as wel
def Set_Try(s,a,b,c):
    if Set_Check(a,b,c):
        if len(RemainingCards)>0:
            Table_Cards[a]=getcard()
            Table_Cards[b]=getcard()
            Table_Cards[c]=getcard()
        else:
            Table_Cards.pop(a)
            Table_Cards.pop(b-1)
            Table_Cards.pop(c-2)
        All_Sets.clear()
        Get_Sets()
        return s+1
    else:
        return s

# A keys dictionary which makes checking all the inputs of the characters a to l easier
keysdictionary={0:pygame.K_a,1:pygame.K_b,2:pygame.K_c,3:pygame.K_d,4:pygame.K_e,5:pygame.K_f,6:pygame.K_g,7:pygame.K_h,8:pygame.K_i,9:pygame.K_j,10:pygame.K_k,11:pygame.K_l}     

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

    #checking if the keys from a to l are pressed
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
    if inputkeys[pygame.K_RETURN]: 
        if len(SET_SelectorList)==3: 
            score=Set_Try(score,SET_SelectorList[0],SET_SelectorList[1],SET_SelectorList[2])
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
                Table_Cards[a]=getcard()
            Get_Sets()

    # if gameover this is displayed and space enables player to restart
    if GameOver:
        GameOverText = Font.render("Game Over! Press the Spacebar to play again.",False,(0,0,0))
        gameboard.blit(GameOverText,(475-GameOverText.get_width()//2,25-GameOverText.get_height()//2))
        if inputkeys[pygame.K_SPACE]:
            GameOver=False
            Table_Cards=[]
            InitializeRemainingCards()
            InitializeTable()
            score=0

    # Adding the Table_Cards to the screen
    for i in range(len(Table_Cards)):
        temporary_surface = pygame.image.load(Table_Cards[i].filename)
        cardcharacter = Font.render(chr(97+i),False,(0,0,0))
        temporary_surface.blit(cardcharacter,(80,180))
        gameboard.blit(temporary_surface,(50+150*(i%6),50+250*(i//6)))

    # Adding the gameboard to the screen
    # Score and highscore are displayed and the highscore is updated
    screen.blit(gameboard,(0,0))
    scoretext=Font.render("score="+str(score),False,(0,0,0))
    screen.blit(scoretext,(20,20))
    if score>highscore:
        highscore=score
    highscoretext=Font.render("highscore="+str(highscore),False,(0,0,0))
    screen.blit(highscoretext,(930-highscoretext.get_width(),20))

    
    for i in SET_SelectorList:
        temporary_surface = pygame.Surface((100,200))
        temporary_surface.fill(pygame.Color(255,255,0))
        temporary_surface.set_alpha(64)
        screen.blit(temporary_surface,(50+150*(i%6),50+250*(i//6)))

    pygame.display.update()
    clock.tick(60)