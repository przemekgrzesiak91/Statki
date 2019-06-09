import wyswietlacz
import wyswietlacz2
import yaml
import sys
import getopt
import time
import numpy as np
import win32pipe, win32file, pywintypes

opts, args = getopt.getopt(sys.argv[1:], 'su:',['start','ustawienia='])
plansza = wyswietlacz.plansza
plansza2 = np.full((10,10),".")
plik='ustawienia.txt'
licznik = 0
start = 0

pozycje_strzalow = {'a':1,'b':2,'c':3,
                    'd':4,'e':5,'f':6,
                    'g':7,'h':8,'i':9,'j':10}

def czy_zatopiony(nr):

    if moje_statki[nr][1]==0:
        print("!! Przeciwnik zatopił twój "+str(moje_statki[nr][0]))
        return True


def sprawdz_strzal(row,col):
    global licznik
    
    if plansza[row,col] == '*' or plansza [row,col] == '.':
        rezultat=("pudło")
        plansza[row,col]='P'
        
    elif plansza[row,col] == 'X' or plansza [row,col] == 'P':
        rezultat=("już tu strzeliłeś")
        
    else:
        rezultat=("trafiony")
        plansza[row,col]='X'
        #aktualizacja stanu statków
        for i in range(1,11):
            for j in range(0,len(moje_statki[i][2])):
                a=moje_statki[i][2][j][0]
                b=moje_statki[i][2][j][1]

                if row==a and col==b:
                    moje_statki[i][1]-=1
                    moje_statki[i][2][j][2]='X'
                    open(plik, 'w').write(yaml.dump(moje_statki))
                    if czy_zatopiony(i):
                        rezultat = ("zatopiony")
                        licznik+=1
                        print(licznik)
                        if licznik==10:
                            rezultat = "koniec"
                            
    wyswietlacz2.rysuj_plansze(plik,plansza2)     
    return rezultat

#----------PIERWSZY GRACZ----------
def first_player():
    print("-----Twoja plansza-----")
    wyswietlacz.rysuj_plansze(plik)
    count = 0
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\Foo',
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    try:
        print("Oczekuje na 2 gracza")
        win32pipe.ConnectNamedPipe(pipe, None)
        print("2 gracz dołączył")

        while True:
            #STRZAŁ
            cel = input("Cel: ")
            col = pozycje_strzalow[cel[0]]-1
            row = int(cel[1:3])-1

            #WYSLANIE STRZALU
            cel = str.encode(cel)
            win32file.WriteFile(pipe, cel)

            #ODPOWIEDZ PRZECIWNIKA NA MÓJ STRZAŁ
            odp = win32file.ReadFile(pipe, 64*1024)
            odp = odp[1].decode('utf-8')
            print(odp)
            if odp=="pudło":
                plansza2[row,col]='P'
            elif odp=="trafiony" or odp=="zatopiony":
                plansza2[row,col]='X'
                
            
            

            #STRZAŁ PRZECIWNIKA
            cel2 = win32file.ReadFile(pipe, 64*1024)
            cel2 = cel2[1].decode('utf-8')
            col = pozycje_strzalow[cel2[0]]-1
            row = int(cel2[1:3])-1

            #ODPOWIEDZ NA STRZAŁ PRZECWINIKA
            rezultat = sprawdz_strzal(row,col)
            rezultat = str.encode(rezultat)
            win32file.WriteFile(pipe, rezultat)
            if rezultat=="koniec":
                break
            
    finally:
        win32file.CloseHandle(pipe)

#----------DRUGI GRACZ----------
def second_player():
    
    print("-----Twoja plansza-----")
    wyswietlacz.rysuj_plansze(plik)
    quit = False

    while not quit:
        try:
            handle = win32file.CreateFile(
                r'\\.\pipe\Foo',
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            if res == 0:
                print(f"SetNamedPipeHandleState return code: {res}")
            
            while True:
                #POBIERZ STRZAŁ
                resp = win32file.ReadFile(handle, 64*1024)
                cel = resp[1].decode('utf-8')

                #ODP na strzał
                col = pozycje_strzalow[cel[0]]-1
                row = int(cel[1:3])-1

                rezultat = sprawdz_strzal(row,col)
                rezultat = str.encode(rezultat)
                win32file.WriteFile(handle, rezultat)
                if rezultat=="koniec":
                    break
         
                #STRZEL
                cel = input("Cel: ")
                col = pozycje_strzalow[cel[0]]-1
                row = int(cel[1:3])-1

                #WYSLANIE STRZALU
                cel = str.encode(cel)
                win32file.WriteFile(handle, cel)
                
                #CZEKAJ na ODP
                odp = win32file.ReadFile(handle, 64*1024)
                odp = odp[1].decode('utf-8')
                print(odp)
                if odp=="pudło":
                    plansza2[row,col]='P'
                elif odp=="trafiony" or odp=="zatopiony":
                    plansza2[row,col]='X'
                
                #CZEKAJ NA STRZAŁ

            
        except pywintypes.error as e:
            if e.args[0] == 2:
                print("Brak admina, ponawiam probe połączenia")
                time.sleep(1)
            elif e.args[0] == 109:
                print("połączenie zerwane, żegnaj")
                quit = True

    

for opt, arg in opts:
    print(opt,arg)
    if opt in ('-u','--ustawienia'):
        print("---Plansza załaduję z : ",arg)
        try :
            plik=arg
            with open(plik,'r') as stream:
                moje_statki = yaml.safe_load(stream)
        except FileNotFoundError:
            print("---Nie ma takiego pliku, ładuję planszę z domyślnego - ustawienia.txt") 
            with open("ustawienia.txt",'r') as stream:
                moje_statki = yaml.safe_load(stream)
    if opt in ('-s','--start'):
        print("---Startujesz")
        start=1


if start==1: first_player()
elif start==0:
    print ("---Nie podano pliku ładuję planszę z domyślnego - ustawienia.txt")
    with open("ustawienia.txt",'r') as stream:
        moje_statki = yaml.safe_load(stream)
    print("---Strzelasz jako drugi")
    second_player()

    
    
