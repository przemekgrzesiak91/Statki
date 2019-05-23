import wyswietlacz
import yaml


with open("ustawienia.txt",'r') as stream:
            moje_statki = yaml.safe_load(stream)
licznik = 10
plansza = wyswietlacz.plansza

pozycje_strzalow = {'a':1,'b':2,'c':3,
                    'd':4,'e':5,'f':6,
                    'g':7,'h':8,'i':9,'j':10}

#pętla aż do końca rozgrywki
    #strzela -> odczyt informacji  
    #odczyt strzału przeciwnika

def czy_zatopiony(nr):

    if moje_statki[nr][1]==0:
        print("zatopiłeś "+str(moje_statki[nr][0]))
        return True
    

def czy_koniec():
    #nie dziala!!
    if licznik==0:
        print("Koniec Gry!")
        return True
    

#wersja w strzelanie w swoje statki
while True:
    print('-----------------------')
    cel = input("Cel: ")
    col = pozycje_strzalow[cel[0]]-1
    row = int(cel[1:3])-1

    if plansza[row,col] == '*' or plansza [row,col] == '.':
        print("pudło")
        plansza[row,col]='P'
        wyswietlacz.rysuj_plansze()
    else:
        print("trafiony")
        plansza[row,col]='X'
        #aktualizacja stanu statków
        for i in range(1,11):
            for j in range(0,len(moje_statki[i][2])):
                a=moje_statki[i][2][j][0]
                b=moje_statki[i][2][j][1]

                if row==a and col==b:
                    moje_statki[i][1]-=1
                    moje_statki[i][2][j][2]='X'
                    open('ustawienia.txt', 'w').write(yaml.dump(moje_statki))
                    if czy_zatopiony(i):
                        licznik-=1
                        print("Pozostało Ci: ",licznik)
                        
    wyswietlacz.rysuj_plansze()     
    if czy_koniec(): break

        
print("Koniec gry!")

