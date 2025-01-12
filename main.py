import pygame
import random
from sys import exit

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((950,550))
pygame.display.set_caption('SET')
clock=pygame.time.Clock()
score=0

gameboard = pygame.Surface((950,550))
gameboard.fill(pygame.Color(152, 155, 156))

#setting the standard font
Font=pygame.font.SysFont('Arial',16)

#Card storage method = [Amount,Fill,Shape,Color,filename]
#Amount, 1=0, 2=1, 3=2 
#Fill, empty=0, full=1, shaded=2
#Shape, diamond=0, oval=1, squiggle=2
#Color, green=0, purple=1, red=2

#Creating the all the cards
amount = {0:"1",1:"2",2:"3"}
fill={0:"empty",1:"filled",2:"shaded"}
shape={0:"diamond",1:"oval",2:"squiggle"}
color = {0:"green",1:"purple",2:"red"}

#initializing all the cards
Cards=[]
for i in range(3):
    for j in range (3):
        for k in range(3):
            for l in range(3):
                Cards.append([i,j,k,l,"pygame"+"\\"+"kaarten"+"\\"+color[l]+shape[k]+fill[j]+amount[i]+".gif"])

#getcard() retrieves a random card that hasnt been used yet
def getcard():
    randomnumber=random.randint(0,len(Cards)-1)
    temp=Cards[randomnumber]
    Cards.pop(randomnumber)
    return temp

#initializing the table
Table_Cards=[]
for i in range(12):
    Table_Cards.append(getcard())

def Set_Check(Kaart1,Kaart2,Kaart3): #function that checks for 3 given indices of cards in the table cards list if they are a set
    for i in range(4): 
        #testing for each of the for properties if they are all the same or all different
    	#if that is not the case it returns False other and otherwise returns True
        if not(Table_Cards[Kaart1][i]==Table_Cards[Kaart2][i]==Table_Cards[Kaart3][i] or Table_Cards[Kaart1][i]!=Table_Cards[Kaart2][i]!=Table_Cards[Kaart3][i]):
            return False
    return True

#List that has all the selected cards
SET_SelectorList=[]

#this functions handles the set selection of the player
def Set_Try(s,a,b,c):
    if Set_Check(a,b,c):
        Table_Cards[a]=getcard()
        Table_Cards[b]=getcard()
        Table_Cards[c]=getcard()
        return s+1
    else:return s

#keys dictionary which making checking all the inputs of the characters a to l way easier
keysdictionary={0:pygame.K_a,1:pygame.K_b,2:pygame.K_c,3:pygame.K_d,4:pygame.K_e,5:pygame.K_f,6:pygame.K_g,7:pygame.K_h,8:pygame.K_i,9:pygame.K_j,10:pygame.K_k,11:pygame.K_l}     

#Main game loop
while True:
    #Checking if the program is closed or not
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
    
    inputkeys=pygame.key.get_pressed()

    #checking if a to l are pressed
    for i in range(12):
        if inputkeys[keysdictionary[i]]:
            if SET_SelectorList.count(i)<1:
                SET_SelectorList.append(i)
        
    if len(SET_SelectorList)>=3:
        score=Set_Try(score,SET_SelectorList[0],SET_SelectorList[1],SET_SelectorList[2])
        SET_SelectorList=[]


    #adding the cards to the screen
    for i in range(len(Table_Cards)):
        temporary_surface = pygame.image.load(Table_Cards[i][-1])
        cardcharacter = Font.render(chr(97+i),False,(0,0,0))
        temporary_surface.blit(cardcharacter,(80,180))
        gameboard.blit(temporary_surface,(50+150*(i%6),50+250*(i//6)))


    #adding the gameboard to the screen
    screen.blit(gameboard,(0,0))

    scoretext=Font.render("score="+str(score),False,(0,0,0))
    screen.blit(scoretext,(20,20))
    
    pygame.display.update()
    clock.tick(60)