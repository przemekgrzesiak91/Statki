import sys
import yaml
import numpy as np

plansza = np.full((10,10),".")

def rysuj_plansze(plik="ustawienia.txt"):

    if sys.stdin.isatty():
        with open(plik,'r') as stream:
            moje_statki = yaml.safe_load(stream)
    else:
        moje_statki=yaml.safe_load(sys.stdin.read())
        open(plik, 'w').write(yaml.dump(moje_statki))

    for i in range(1,11):
        for j in range(0,len(moje_statki[i][2])):
            x=moje_statki[i][2][j][0]
            y=moje_statki[i][2][j][1]
            plansza[x,y]=moje_statki[i][2][j][2]

    print ("   a_b_c_d_e_f_g_h_i_j")
    
    for i in range(0,10):
        if i==9:
           print (str(i+1)+'|'+str(' '.join(plansza[i]))+'|')
        else:
            print (' '+str(i+1)+'|'+str(' '.join(plansza[i]))+'|')
    print ("   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
    return

if __name__ == "__main__":
    rysuj_plansze()
