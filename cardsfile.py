from pathlib import Path
dir = Path(__file__).resolve().parent

class Card:
    def __init__(self,amount,fill,shape,color,filename):
        self.amount=amount
        self.fill=fill
        self.shape=shape
        self.color=color
        filename=filenamecreator(amount,fill,shape,color)
        self.filename=filename
    def __str__(self): #making sure a card can be printed, usefull for debugging. 
        tempstring="["+str(self.amount)+ ", "+ str(self.fill)+", "+str(self.shape)+", "+str(self.color)+", "+str(self.filename)+"]"
        return tempstring

#Card storage method
#Amount, 1=0, 2=1, 3=2 
#Fill, empty=0, full=1, shaded=2
#Shape, diamond=0, oval=1, squiggle=2
#Color, green=0, purple=1, red=2

amount_dic = {0:"1",1:"2",2:"3"}
fill_dic={0:"empty",1:"filled",2:"shaded"}
shape_dic={0:"diamond",1:"oval",2:"squiggle"}
color_dic = {0:"green",1:"purple",2:"red"}

def filenamecreator(a,f,s,c):
    fileName = "kaarten"+"\\"+color_dic[c]+shape_dic[s]+fill_dic[f]+amount_dic[a]+".gif"
    return dir / fileName
        

#initializing all the RemainingCards
RemainingCards=[]
def InitializeRemainingCards():
    for i in range(3):
        for j in range (3):
            for k in range(3):
                for l in range(3):
                    RemainingCards.append(Card(i,j,k,l,""))
