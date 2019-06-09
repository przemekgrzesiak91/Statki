import wyswietlacz
import wyswietlacz2
import yaml
import sys
import socket
import getopt
import time
import numpy as np

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
        print("!! Przeciwnik zatopił twój "+str(moje_statki[nr][0])+"!!")
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
                    #open(plik, 'w').write(yaml.dump(moje_statki))
                    if czy_zatopiony(i):
                        rezultat = ("zatopiony")
                        licznik+=1
                        if licznik==10:
                            rezultat = "koniec"
                            
    wyswietlacz2.rysuj_plansze(plik,plansza,plansza2)     
    return rezultat

def strzelaj():
    cel = input("Cel: ")
    
    while True:
        if cel[0] in ('a','b','c','d','e','f','i','j'):
            if int(cel[1:3]) in range (1,11):
                return(cel)
            else:
                print("Niepoprawny cel, spróbuj jeszcze raz")
                cel = input("Cel: ")
        else:
            print("Niepoprawny cel, spróbuj jeszcze raz")
            cel = input("Cel: ")
            
    

#----------PIERWSZY GRACZ----------
def first_player():
    print("-----Twoja plansza-----")
    wyswietlacz.rysuj_plansze(plik)
    count = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    moje_ip = socket.gethostbyname(socket.gethostname())
    server_address = (moje_ip, 10000)
    print ('IP: %s PORT: %s' % server_address)
    sock.bind(server_address)

    sock.listen(1)

    while True:
        # Wait for a connection
        print ('Czekam na przeciwnika')
        connection, client_address = sock.accept()

        try:
            print ('Adres przeciwnika: ', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                #STRZAŁ
                cel = strzelaj()
                col = pozycje_strzalow[cel[0]]-1
                row = int(cel[1:3])-1

                #WYSLANIE STRZALU
                cel = str.encode(cel)
                connection.sendall(cel)

                #ODPOWIEDZ PRZECIWNIKA NA MÓJ STRZAŁ
                odp = connection.recv(20)
                odp = odp.decode('utf-8')
                print(odp)

                if odp=="pudło":
                    plansza2[row,col]='P'
                elif odp=="trafiony" or odp=="zatopiony":
                    plansza2[row,col]='X'
                elif odp=="koniec":
                    break
            
                #STRZAŁ PRZECIWNIKA
                cel2 = connection.recv(20)
                cel2 = cel2.decode('utf-8')
                col = pozycje_strzalow[cel2[0]]-1
                row = int(cel2[1:3])-1

                #ODPOWIEDZ NA STRZAŁ PRZECWINIKA
                rezultat = sprawdz_strzal(row,col)
                rezultat = str.encode(rezultat)
                connection.sendall(rezultat)
                if rezultat=="koniec":
                    break
                
        finally:
            # Clean up the connection
            connection.close()

#----------DRUGI GRACZ----------
def second_player():
    
    print("-----Twoja plansza-----")
    wyswietlacz.rysuj_plansze(plik)
    quit = False

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    admin_ip=input("Wpisz ip admina: ")
    server_address = (admin_ip, 10000)
    print ('Połączono z IP: %s PORT: %s' % server_address)
    sock.connect(server_address)

    try:        
        while True:
                #POBIERZ STRZAŁ
                resp = sock.recv(20)
                cel = resp.decode('utf-8')

                #ODP na strzał
                col = pozycje_strzalow[cel[0]]-1
                row = int(cel[1:3])-1

                rezultat = sprawdz_strzal(row,col)
                rezultat = str.encode(rezultat)
                sock.sendall(rezultat)
                if rezultat=="koniec":
                    break
         
                #STRZEL
                cel = strzelaj()
                col = pozycje_strzalow[cel[0]]-1
                row = int(cel[1:3])-1

                #WYSLANIE STRZALU
                cel = str.encode(cel)
                sock.sendall(cel)
                
                #CZEKAJ na ODP
                odp = sock.recv(20)
                odp = odp.decode('utf-8')
                print(odp)

                if odp=="pudło":
                    plansza2[row,col]='P'
                elif odp=="trafiony" or odp=="zatopiony":
                    plansza2[row,col]='X'
                elif odp=="koniec":
                    break
                
                #CZEKAJ NA STRZAŁ

    finally:
        print ('koniec połączenia')
        sock.close()

plik=0
for opt, arg in opts:
    if opt in ('-u','--ustawienia'):
        plik=1
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
    if plik==0:
        print ("---Nie podano pliku ładuję planszę z domyślnego - ustawienia.txt")
        with open("ustawienia.txt",'r') as stream:
            moje_statki = yaml.safe_load(stream)
    print("---Strzelasz jako drugi")
    second_player()

    
    
