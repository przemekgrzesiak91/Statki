import numpy as np
import random
import yaml

plansza = np.full((10,10),".")
statki = [4,3,3,2,2,2,1,1,1,1]
moje_statki = {}


'''Generator tworzy plansze (macierz) na której rozmiesza statki,
zgodnie z zasadami gry, dodatkowo tworzny jest słownik przechowujący
wszystkie dane o ustawionych statkach.
'''

def stworz_plansze():
    i=1
    for statek in statki:
        #print (statek)
        done = False
        pozycje=[]
        
        while not done:
            licznik = statek
            
            x = random.randint(0,9)
            y = random.randint(0,9)

            #print(x,y)
            
            if(plansza[x,y]=="."):
                kierunek = random.randint(0,1)

                if kierunek == 0:
                    x_min=x-1
                    x_max=x+licznik+1
                    y_min=y-1
                    y_max=y+2
                    
                    #print(x_min,x_max,y_min,y_max)
                    if(x_min<0): x_min=0
                    if(x_max>=10): x_max=10
                    if(y_min<0): y_min=0
                    if(y_max>=10): y_max=10
                    #print(x_min,x_max,y_min,y_max)
                    
                    if (np.all(plansza[x:x+licznik,y]==".")  and x+licznik<10):
                        plansza[x_min:x_max,y_min:y_max]="*"
                        plansza[x:x+licznik,y]=statek


                        
                        for k in range(0,licznik):
                            pozycje.append([x,y,licznik])
                            x=x+1

                        moje_statki[i]=[str(licznik)+"-masztowiec",licznik,pozycje]

                            
                        i=i+1
                        done=True
                        
                    else:
                        done=False

                if kierunek ==1:
                    x_min=x-1
                    x_max=x+2
                    y_min=y-1
                    y_max=y+licznik+1
                    
                    #print(x_min,x_max,y_min,y_max)
                    if(x_min<0): x_min=0
                    if(x_max>=10): x_max=10
                    if(y_min<0): y_min=0
                    if(y_max>=10): y_max=10
                    #print(x_min,x_max,y_min,y_max)
                    
                    if (np.all(plansza[x,y:y+licznik]==".") and y+licznik<10):
                        plansza[x_min:x_max,y_min:y_max]="*"
                        plansza[x,y:y+licznik]=statek


                        for k in range(0,licznik):
                            pozycje.append([x,y,licznik])
                            y=y+1

                        moje_statki[i]=[str(licznik)+"-masztowiec",licznik,pozycje]

                        
                        i=i+1
                        done=True
                        
                    else:
                        done=False

    #YAML
    dane=yaml.dump(moje_statki)
##
##    for i in range(0,10):
##        for j in range(0,10):
##            if plansza[i][j]=='*': plansza[i][j]='.'
        
    return print(dane)

stworz_plansze()




                                    
    
