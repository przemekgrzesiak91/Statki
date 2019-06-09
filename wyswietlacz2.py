import sys
import yaml
import numpy as np

def rysuj_plansze(plik,plansza,plansza2):

    print ("      Twoja plansza              Przeciwnik")  
    print ("   a_b_c_d_e_f_g_h_i_j      a_b_c_d_e_f_g_h_i_j")
    
    for i in range(0,10):
        if i==9:
           print (str(i+1)+'|'+str(' '.join(plansza[i]))+'|  '+str(i+1)+'|'+str(' '.join(plansza2[i]))+'|')
        else:
            print (' '+str(i+1)+'|'+str(' '.join(plansza[i]))+'|   '+str(i+1)+'|'+str(' '.join(plansza2[i]))+'|')
    print ("   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯      ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
    return

if __name__ == "__main__":
    rysuj_plansze()
