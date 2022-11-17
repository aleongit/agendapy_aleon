#Aleix Leon
#BIBLIOTECA - AGENDA

import random
#per alta massiva test

import os.path, time
#per info arxiu

import string
#print(string.ascii_letters) # lletres ascii
#print(string.digits)        # digits
#print(string.punctuation)   # símbols puntuació

lletres = string.ascii_letters + "ñàèéíòóúüï"

import re
#per validacions email i telegram
#Regular expression operations
#https://docs.python.org/3/library/re.html
#https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
regexemail = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
regextele = '^[@](\w|\_|\-)+$'

ESPAI = " "
SEP = ","
fitxer = "agenda.txt"
AUTOR = "Aleix Leon"

dmenu = {1:"Alta",2:"Llistat",3:"Modificació",4:"Baixa",5:"Cercar",6:"Alta Massiva *TEST BUIDA*",0:"Sortir"}
camps = ["Nom","Cognom/s","Telèfon","em@il","@telegram"]
registres = []

QM = 10 #quantitat per massiu

def printMenu():
    #mètode print(" %s " %(variable))
    print()
    for k,v in dmenu.items():
        print("%s -> %s" %(k,v))
    print()
    
def printCap(ll):
    print(f"\nAGENDA CONTACTES v1.0 by {AUTOR}")
    print(f"Fitxer contactes  : {fitxer}")
    print(f"Fitxer modificació: {time.ctime(os.path.getmtime(fitxer))}")
    print(f"Fitxer mida       : {os.path.getsize(fitxer)} bytes")
    print(f"Total contactes   : {len(ll)}")

#afegeixo comes i intro
def prepararRegistre(registre):
    ll = []
    #afegeixo element + separador menys últim camp
    for el in registre[:-1]:
        ll.append(el)
        ll.append(SEP)
    #últim camp
    ll.append(registre[-1])
    #return
    ll.append('\n')
    return ll

def crearAgenda(fitxer):
    #preparo camps
    r = prepararRegistre(camps)

    #obrim fitxer w, afegim i tanquem
    with open(fitxer, "w", encoding="utf8") as f:
        f.writelines(r)    

def esDigit(c):
    return c in string.digits

def esEspai(c):
    return c == ESPAI

def esSimbol(c):
    return c in string.punctuation

def esLletra(c):
    return c.lower() in lletres

def fesTrim(cad): 
    return " ".join(paraula for paraula in cad.split())

#suposo nom compost amb 1 espai
#vàlid per cognoms
def nomOK(nom):
    ller = []
    llok = []
    ok = num = sim = False
    missatge = ""
    
    for c in nom:
        if esDigit(c):
            ller.append(c)
            num = True
        elif esSimbol(c):
            ller.append(c)
            sim = True
        elif esLletra(c) or esEspai(c):
            llok.append(c)
    #print(ller)
    if not ller == []:
        if num:
            missatge += "\n*FATAL ERROR* no dígits"
        if sim:
            missatge += "\n*FATAL ERROR* no símbols"
        print(missatge)
    else:
        if not llok == []:
            nom = "".join([el for el in llok])
            ok = True
    return ok

#suposo 9 dígits, sense prefix estranger
def tlfOK(tlf):
    ok = False
    mida = 9
    missatge = ""

    if len(tlf) == 9:
        #print("mida ok")
        if tlf.isdigit():
            #print("ok és digit")
            ok = True
        else:
            missatge += "\n*FATAL ERROR* només dígits"
            print(missatge)
    else:
        missatge += "\n*FATAL ERROR* mida tlf = 9 dígits"
        if tlf != "":
            print(missatge)
    return ok

def emailOK(email):
    ok = False
    missatge = ""
    #comprova si email amb expressió re, flag ascii per no accents
    if(re.search(regexemail, email,flags=re.A)):
        #print("em@il ok")
        ok = True
    else:
        missatge += "\n*FATAL ERROR* em@ail no vàlid"
        if email != "":
            print(missatge)
    return ok

def teleOK(telegram):
    ok = False
    missatge = ""
    #comprova si telegram amb expressió re, flag ascii per no accents
    if(re.search(regextele, telegram,flags=re.A)):
        #print("@telegram ok")
        ok = True
    else:
        missatge += "\n*FATAL ERROR* @telegram no vàlid"
        if telegram != "":
            print(missatge)
    return ok

def cap(nom):
    return " ".join([paraula.lower().capitalize() for paraula in nom.split()])

def NouContacteFitxer(fitxer,contacte):
    #obrim fitxer a, afegim i tanquem
    with open(fitxer, "a", encoding="utf8") as f:
        f.writelines(contacte)
    #printFitxer(fitxer)
       
def printFitxer(fitxer):
    print("\n*FITXER TXT*")
    with open(fitxer, "r", encoding="utf8") as f:
        print(f.read())
        
def existeixFitxer(fitxer):
    try:
        with open(fitxer, "r", encoding="utf8") as f:
            ok = True
    except IOError:
        ok = False
    return ok

def llegeixFitxer(fitxer):
    with open(fitxer, "r", encoding="utf8") as f:
        #la capçalera no l'agafo
        ll = f.readlines()[1:]
    return ll

def rcadena(ll):
    return "".join([el for el in ll])
    
def guardaFitxer(ll,fitxer):
    #preparem registres (llista dics) per guardar a fitxer
    #cada dic a llista
    agenda = []
    
    #capçalera
    #agafeixo comes i salt + passo a cadena + afageixo a agenda
    agenda.append(rcadena(prepararRegistre(camps)))
     
    for dic in ll:
        contacte = []
        for el in dic:
            contacte.append(dic[el])
        #agafeixo comes i salt + passo a cadena + afageixo a agenda      
        agenda.append(rcadena(prepararRegistre(contacte)))
    #print(agenda)
    
    #obrim fitxer w, afegim i tanquem
    with open(fitxer, "w", encoding="utf8") as f:
        f.writelines(agenda) 

def carregaAgenda(linies):
    #creo diccionari amb camp + valor camp
    ll = []
    for linia in linies:
        #trec intro final línia
        linia = linia[:-1]
        d = {}
        i = 0
        for paraula in linia.split(','):
            d[camps[i]] = paraula
            i += 1
        ll.append(d)
    return ll

def llargadaCamp(ll):
    #màxim len
    maxim = 0
    for dic in ll:
        for el in dic.values():
            if len(el) > maxim:
                maxim = len(el)
    return maxim

def mostraLinies(ll,x,rp,llarg):
    #mostro per slice
    print()
    for dic in ll[x:(x+rp)]:
        #posició del registre (dic) + 1 dins llista
        i = str(ll.index(dic)+1)
        print((3-(len(i)))*" ", end ="")
        print(i,end= ". ")
        for el in dic.values():
            #paginació
            print(f"{(el)}",end= "")
            print((llarg-(len(el)))*" ", end =" ")
        print()

# c = index-1 camp en camps
def verificaCamp(c):
    ok = False
    #comprovem c
    if c.isdigit():
        #print("ok dígit")
        if int(c) in range(1,len(camps)+1):
            #print("ok en rang")
            ok = True
        else:
            print("\n*FATAL ERROR* dígit no vàlid") 
    else:
        print("\n*FATAL ERROR* no dígit")    
    return ok

#camps = ["Nom","Cognom/s","Telèfon","em@il","@telegram"]
def modificaCamp(dic,c):
    c = int(c) - 1
    camp = camps[c]
    #títol
    print(f"\n*MODIFICACIÓ DE {camp.upper()}*")
    #valor actual
    print(f"\nValor actual: {dic[camp]}")
    #nou valor
    ok = False
    while not ok:
        nou = input("Valor nou   : ")
        #validació depenent camps
        if c == 0 or c == 1:
            ok = nomOK(nou)
            if ok:
                #arreglar: espais i cap
                nou = cap(fesTrim(nou))
        elif c == 2:
            ok = tlfOK(nou)
        elif c == 3:
            ok = emailOK(nou)
        else:
            ok = teleOK(nou)

    #modifica a diccionari
    dic[camp] = nou
    print(f"\n*MODIFICACIÓ DE {camp.upper()} OK*")

def printRegistre(dic,o):
    print(f"\n* REGISTRE {o}*")
    print()
    i = 1
    for el in dic:
        print(f"{i}. {el}",end =" ")
        print((10-(len(el)))*" ", end =" ")
        print(dic[el])
        i += 1
    print()

#o = n registre / m = modifica / e = elimina
# retorno si canvis a registre (modificat o eliminat)
def accioRegistre(dic,o,m=False,e=False):
    canvis = False
    #print("m",m,"e",e)
    #si modifica
    if m:
        print("*MODIFICACIÓ REGISTRE*")
        ok=False
        while not ok:
            printRegistre(dic,o)
            camp = input(f"Camp a modificar {[i+1 for i in range(len(dic))]}[0 Sortir/Guardar]: ")
            if camp =="0":
                ok = True
            else:
                ko = False
                ko = verificaCamp(camp)
                #modificació camp a dic
                if ko:
                    modificaCamp(dic,camp)
                    canvis = True
    #si elimina
    elif e:
        print("*ELIMINACIÓ REGISTRE*")
        ok = False
        while not ok:
            printRegistre(dic,o)
            o = input("Eliminem? [s/n] :")
            if o.lower() == 'n':
                ok = True
            elif o.lower() == 's':
                #print("eliminem")
                #activem canvis i trec amb pop al retorn d'aquesta funció
                canvis = True
                ok = True
            else:
                print("\n*FATAL ERROR* opció no vàlida")
    else:
        printRegistre(dic,o)
        print("*INTRO PER CONTINUAR*", end ="")
        input()
        print()
    return canvis
        
#m = modifica / e = elimina
def printLlista(ll,m=False,e=False):
    #busca per llarg camp
    llarg = llargadaCamp(ll)
    
    #per paginació
    tr = len(ll)     #total registres
    RP = 5           #registres per pàgina
    x = 0            #registre canviant
    ok = False
    while not ok:
        #mostraLinies(ll[0:1])
        mostraLinies(ll,x,RP,llarg)
        print("INTRO continuar i sortir, NUM registre", end ="")
        o = input(": ")
        if o == "":
            #incrementem x slice inicial fins total
            if RP == tr:
                x = RP
            else:
                x += RP
            #print("x",x)
            #arreglem registres pàgina quan arriba a final
            #print("x+RP",x+RP,"tr",tr)
            if x + RP > tr:
                RP = tr
                #print("RP",RP)
            #si els ha ensenyat tots sortim
            if x == RP == tr:
                print("\n*FI REGISTRES*")
                ok = True
        #elif o == "0":
            #ok = True
        #si índex registre
        elif o in [str(i) for i in range(1,len(ll)+1)]:
            #print("ok index")
            #mostra registre
            #print(ll[int(o)-1]['Nom'])
            canvis = accioRegistre(ll[int(o)-1],o,m,e)
            if canvis:
                #print(e,canvis,"e amb canvis")
                #si canvis amb e, trec dic amb pop
                if e:
                    ll.pop(int(o)-1)
                    print("\n*REGISTRE ELIMINAT*")
                #guardem si canvis
                guardaFitxer(ll,fitxer)
                print("\n*AGENDA MODIFICADA I GUARDADA")
                ok = True
                            
def refrescaAgenda():
    ll = []
    #comprovo si agenda, sinó inicializo
    if not existeixFitxer(fitxer):
        crearAgenda(fitxer)
    #si existeix carrega (actualitza)
    else:
        ll = carregaAgenda(llegeixFitxer(fitxer))
    printFitxer(fitxer)
    return ll
       
def alta():
    #"Pepet, Nosurt, 666777888, pepet@nosurt.com, @pepetnosurt"
    contacte = []
    nom = cognom = tlf = email = telegram = ""
    
    print("\n*ALTA CONTACTE*")
    
    #nom
    while not nomOK(nom):
        nom = input("Nom: ")
    #arreglar nom: espais i cap
    nom = cap(fesTrim(nom))
    contacte.append(nom)
    
    #cognom/s
    while not nomOK(cognom):
        cognom = input("Cognom/s: ")
    #arreglar nom: espais i cap
    cognom = cap(fesTrim(cognom))
    contacte.append(cognom)
    
    #tlf
    while not tlfOK(tlf):
        tlf = input("Telèfon: ") 
    contacte.append(tlf)
    
    #em@ail
    while not emailOK(email):
        email = input("Em@ail: ") 
    contacte.append(email)
    
    #@telegram
    while not teleOK(telegram):
        telegram = input("@Telegram: ") 
    contacte.append(telegram)
    
    #print(contacte)
    contacte = prepararRegistre(contacte)
    #print(contacte)
    
    #comprovar repetit (tel o email o telegram)
    #mostrar les dues línies i demanar si actualitzar o substituir
    
    #escriu a fitxer
    NouContacteFitxer(fitxer,contacte)
    #printFitxer(fitxer)
    
def llista(registres):
    print("\n*LLISTA CONTACTES*")
    printLlista(registres)
        
def modifica(registres):
    print("\n*MODIFICA CONTACTE*")
    printLlista(registres,m=True)
    #printFitxer(fitxer)
    #print(registres)
    
def baixa(registres):
    print("\n*BAIXA CONTACTE*")
    printLlista(registres,e=True)
    #printFitxer(fitxer)
    #print(registres)
        
def altaMassiva(n):
    #"Pepet, Nosurt, 666777888, pepet@nosurt.com, @pepetnosurt"
    for i in range(1,n+1):
        contacte = []
        nom = "nom"
        cognom = "cognom"
        tlf = ""
        email = "@test.com"
        telegram = "@"
    
        print("\n*ALTA MASSIVA DE CONTACTE PER TEST*")
    
        #nom
        nom += str(i)
        contacte.append(cap(nom))
        
        #cognom/s
        cognom += str(i)
        contacte.append(cap(cognom))
        
        #tlf
        for i in range(9):
            tlf += random.choice(string.digits)
        contacte.append(tlf)
        
        #em@ail
        email = nom + email
        contacte.append(email)
        
        #@telegram
        telegram += nom
        contacte.append(telegram)
        
        #comes i intro
        contacte = prepararRegistre(contacte)
        
        #escriu a fitxer
        NouContacteFitxer(fitxer,contacte)
    
    #printFitxer(fitxer)

def printCamps():
    for i in range(len(camps)):
        print(i+1,end =". ")
        print(camps[i],end ="")
        print((10-(len(camps[i])))*" ")
        
def treuAccents(cadena):
    #mínuscules
    cadena = cadena.lower()
    #versió amb str.maketrans() i str.translate()
    #cadenes de mateixa longitud per a conversió caràcter 1 a 1
    amb = 'àáèéíïòóúü'
    sense ='aaeeiioouu'
    #taula de conversió de les dues cadenes
    taula = str.maketrans(amb,sense)
    #fer la conversió amb translate()
    return cadena.translate(taula)

#busco valors per camp diccionari
def buscaValors(ll,cadena,camp):
    indexs = []
    for dic in ll:
        #print(dic[camp])
        #llista si troba
        if treuAccents(cadena) in treuAccents(dic[camp]):
            num = str(ll.index(dic)+1)
            print(f"\n{num}",end =". ")
            print(dic[camp])
            indexs.append(num)
    #si consulta no buida
    if indexs != []:
        #demana registre
        ok = False
        while not ok:
            o = input("\nSelecciona registre [0=Sortir]: ")
            if o == "0":
                ok = True
            #si índex registre
            elif o in indexs:
                #print("ok índex")
                num = o
                while not ok:
                    o = input("Llistar/ Modificar/ Eliminar [l/m/e]: ")
                    if o.lower() == 'l':
                        #print("llistar")
                        canvis = accioRegistre(ll[int(num)-1],num)
                        ok = True
                    elif o.lower() == 'm':
                        #print("modificar")
                        canvis = accioRegistre(ll[int(num)-1],num,m=True)
                        ok = True
                    elif o.lower() == 'e':
                        #print("eliminar")
                        canvis = accioRegistre(ll[int(num)-1],num,e=True)
                        #elimino (pop)
                        if canvis:
                            ll.pop(int(num)-1)
                            print("\n*REGISTRE ELIMINAT*\n")
                        ok = True
                    else:
                        print("\n*FATAL ERROR* opció no vàlida") 
                if canvis:
                    guardaFitxer(ll,fitxer)
            else:
                print("\n*FATAL ERROR* opció no vàlida")
    else:
        print("\n*CAP RESULTAT*\n")

def cerca(registres):
    print("\n*CERCA CONTACTE*")
    ok = False
    while not ok:
        #triar camp
        printCamps()
        camp = input(f"\nCamp a cercar {[i+1 for i in range(len(camps))]}[0 Sortir]: ")
        if camp =="0":
            ok = True
        else:           
            if verificaCamp(camp):
                #camp = clau dic
                camp = camps[int(camp)-1]
                #valor a cercar
                valor = input(f"\n{camp} a cercar: ")
                buscaValors(registres,valor,camp)
    
    #printFitxer(fitxer)
    #print(registres)      
    
