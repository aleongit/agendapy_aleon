#Aleix Leon
#Programa Agenda

from agendapy_funcions import *

o = ""
while o != 0:
    registres = refrescaAgenda()
    printCap(registres)
    printMenu()
    try:
        o = int(input("opció: "))
        if o in dmenu.keys():
            #print("opció vàlida")
            if o == 1:
                alta()
            elif o == 2:
                llista(registres)
            elif o == 3:
                modifica(registres)
            elif o == 5:
                cerca(registres)
            elif o == 4:
                baixa(registres)
            elif o == 6:
                altaMassiva(QM)
        else:
            print("\n*FATAL ERROR* opció no vàlida\n")
        
    except ValueError as e:
            #cas no dígit
            print("\n*FATAL ERROR * només dígits\n")
            #print(e)
    