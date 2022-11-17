#Aleix Leon

""" Dissenyeu una aplicació anomenada cognom_nom_agenda.py 
que permeti entrar dades de clients en una agenda, mostrar-les 
i enregistrar-les en un arxiu (amb el format que vulgueu). 
Cal verificar que totes les dades entrades tinguin el format i la longitud correctes.

Crea una classe Client que contingui:
 - les dades per un sol client: nom, cognoms, data_naixement, telefon
 - els mètodes d'entrada: un per a cada atribut
 - els mètodes d'impressió de dades: un per a cada atribut

L'aplicació principal ha de mostrar el següent menú:

1: Introdueix dades a l'agenda.
2: Importa agenda de l'arxiu desitjat.
3: Mostra dades de l'agenda actual.
4: Exporta l'agenda actual a l'arxiu desitjat.
5: Sortir """

import os.path, time #per info arxiu exportat

import string
#print(string.ascii_letters) # lletres ascii
#print(string.digits)        # digits
#print(string.punctuation)   # símbols puntuació

from datetime import datetime

LLETRES = string.ascii_letters + "ñàèéíòóúüï"
DATA_FORMAT = "%d-%m-%Y"

ESPAI = " "
SEP = ","
NO ="NO"
FITXER = "agendapoo.txt"
AUTOR = "Aleix Leon"

MENU = {'1':'Introdueix client','2':'Importa fitxer','3':'Mostra clients','4':'Guarda fitxer','5':'Sortir'}
CAPÇALERA = "nom,cognoms,data_naixement,telèfon\n"

clients = {}

#registres = []
#ll = []

#funcions TEST ___________________________________________________
#imprimir client dic
def print_dic_obj(dic):
    for k,v in dic.items():
        print("%s -> %s" %(k,v))
    print()

def print_dic_obj_ind(dic):
    for k,v in dic.items():
        v.p_nom(),v.p_cognoms(),v.p_data_n(),v.p_tlf()
        print()

# funcions agenda ___________________________________________________
     
def existeix_fitxer(fitxer):
    try:
        with open(fitxer, "r", encoding="utf8") as f:
            ok = True
    except IOError:
        ok = False
    return ok

def print_fitxer(fitxer):
    print("\n*FITXER TXT*")
    with open(fitxer, "r", encoding="utf8") as f:
        print(f.read())

#obrim fitxer w, afegim i tanquem
def guarda_fitxer(fitxer,ll):    
    with open(fitxer, "w", encoding="utf8") as f:
        f.writelines(ll) 

def llegeix_fitxer(fitxer):
    with open(fitxer, "r", encoding="utf8") as f:
        #la capçalera no l'agafo
        ll = f.readlines()[1:]
    return ll

def print_menu():
    #mètode print(" %s " %(variable))
    print()
    for k,v in MENU.items():
        print("%s -> %s" %(k,v))
    print()
    
def print_info(dic):
    print(f"\nAGENDA CLIENTS POO v2.0 by {AUTOR}")
    print(f"Fitxer impo/expo  : {FITXER}")
    print(f"Fitxer modificat  : {time.ctime(os.path.getmtime(FITXER)) if existeix_fitxer(FITXER) else NO}")
    print(f"Fitxer mida       : {os.path.getsize(FITXER) if existeix_fitxer(FITXER) else 0} bytes")
    print(f"Clients a memòria : {len(dic)}")

def es_digit(c):
    return c in string.digits

def es_espai(c):
    return c == ESPAI

def es_simbol(c):
    return c in string.punctuation

def es_lletra(c):
    return c.lower() in LLETRES

def fes_trim(cad): 
    return " ".join(paraula for paraula in cad.split())

def cap(nom):
    return " ".join([paraula.lower().capitalize() for paraula in nom.split()])

#suposo nom compost amb 1 espai
#per nom i cognoms
def nom_ok(nom):
    ller = []
    llok = []
    ok = num = sim = False
    missatge = ""
    
    for c in nom:
        if es_digit(c):
            ller.append(c)
            num = True
        elif es_simbol(c):
            ller.append(c)
            sim = True
        elif es_lletra(c) or es_espai(c):
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
            #nom = "".join([el for el in llok])
            ok = True
    return ok

#data, format = 'dd-mm-aaaa'
def data_ok(data):
    ok = False
    missatge = ""
    if data != '':
        # datetime.strptime retorna error si format incorrecte
        try:
            datetime.strptime(data, DATA_FORMAT)
            ok = True
        except ValueError:
            missatge += "\n*FATAL ERROR* data incorrecte"
            print(missatge)
    return ok

#suposo 9 dígits, sense prefix estranger
def tlf_ok(tlf):
    ok = False
    mida = 9
    missatge = ""

    if len(tlf) == mida:
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

def alta():
    nom = cognoms = tlf = data_n = ""
    obj_client = Client() #nou objecte client
    
    print("\n*ALTA CONTACTE*")
    
    #nom
    while not nom_ok(nom):
        nom = input("Nom: ")
    #arreglar espais i cap
    nom = cap(fes_trim(nom))
        
    #cognoms
    while not nom_ok(cognoms):
        cognoms = input("Cognoms: ")
    #arreglar espais i cap
    cognoms = cap(fes_trim(cognoms))

    #data_n
    while not data_ok(data_n):
        data_n = input("Data Naixement [dd-mm-aaaa]: ")

    #tlf
    while not tlf_ok(tlf):
        tlf = input("Telèfon [9 dígits]: ")
        
    #assignar camps a objecte
    obj_client.a_nom(nom)
    obj_client.a_cognoms(cognoms)
    obj_client.a_data_n(data_n)
    obj_client.a_tlf(tlf)

    #afegir objecte a diccionari
    clients[obj_client.nom] = obj_client
    
    #test
    #print(clients)
    #print_dic_obj(clients)
    #print(len(clients))

def mostra(dic):
    print("\n*LLISTA CONTACTES*")

    #capçalera és string camps amb ',' i '\n' final
    #separo per comes a llista, i ajunto amb tabulador a str
    camps = '\t'.join(CAPÇALERA.split(','))
    print(camps)
    
    #mostra valors
    for k,v in dic.items():
        v.p_nom(),print('\t',end="")
        v.p_cognoms(),print('\t',end="")
        v.p_data_n(),print('\t',end="")
        v.p_tlf()
        print()
    
    input('\nTecla per continuar ...') #pause

def importa(fitxer):
    ok = False
    print("\n*IMPORTA FITXER*")

    if existeix_fitxer(fitxer):
        #print('fitxer existeix')
        #llegeix fitxer, retorna llista menys capçalera
        ll_fitxer = llegeix_fitxer(fitxer)
        #print(len(ll_fitxer))

        #per cada línia llista
        for lin in ll_fitxer:
            #llista valors per comes i elimina \n final
            #print(type(lin))
            #print(lin)
            ll = lin[:-1].split(',') #no agafo últim caràcter '\n' de línia
            #print(ll)
            
            #supòsit no validació (caldria validació per manipulació fitxer)
            #si tots validats, crea objecte          
            #valors a atributs, mètodes individuals

            obj_client = Client() #nou objecte client

            #valors llista a objecte
            obj_client.a_nom(ll[0])
            obj_client.a_cognoms(ll[1])
            obj_client.a_data_n(ll[2])
            obj_client.a_tlf(ll[3])

            #afegir objecte a diccionari
            clients[obj_client.nom] = obj_client
    
        #test
        #print(clients)
        #print_dic_obj(clients)
        #print(len(clients))
        #print(ll_fitxer)
    else:
        print("\n*FATAL ERROR* fitxer no existeix")
    return ok

def guarda(dic,fitxer):
    print("\n*EXPORTA FITXER*")

    #preparem registres (llista) per guardar a fitxer
    ll = []
    
    #capçalera
    ll.append(CAPÇALERA)
    
    #per cada obj crido mètode str_fitxer() que prepara per guardar a fitxer i guardo a llista
    for cli in dic:
        ll.append(dic[cli].str_fitxer())
        #registre.append(dic[cli].nom)
    #print(ll)

    #guarda fitxer
    guarda_fitxer(fitxer,ll)

#classe objecte ________________________________________________________
class Client(object):
    #per defecte
    def __init__(self):
        self.nom = "test"
        self.cognoms = "test"
        self.data_n = "00-00-0000"
        self.tlf = "000000000"
    #print objecte
    def __str__(self):
        return "%s %s %s %s" %(self.nom, self.cognoms, self.data_n, self.tlf)
    #assignar
    def a_nom (self,nom):
        self.nom = nom
    def a_cognoms (self,cognoms):
        self.cognoms = cognoms
    def a_data_n (self,data_n):
        self.data_n = data_n
    def a_tlf (self,tlf):
        self.tlf = tlf
    #print
    def p_nom (self):
        print(self.nom, end =" ")
    def p_cognoms (self):
        print(self.cognoms, end =" ")
    def p_data_n (self):
        print(self.data_n, end =" ")
    def p_tlf (self):
        print(self.tlf, end =" ")
    #retorna registre preparat per fitxer (str)
    def str_fitxer(self):
        return f"{self.nom},{self.cognoms},{self.data_n},{self.tlf}\n" 

if __name__ == "__main__":

    """
    #TEST objecte ___________________________________________
    #objectes valors per defecte
    obj1 = Client()
    obj2 = Client()
    print(obj1,obj2)

    #valors (afegir, modificar)
    obj1.a_nom('Pepito')
    obj1.a_cognoms('Gutiérrez Morales')
    obj1.a_data_n('30-01-1975')
    obj1.a_tlf('666666666')
    print(obj1)

    obj2.a_nom('Pepita')
    obj2.a_cognoms('Ramírez Rodríguez')
    obj2.a_data_n('15-03-1980')
    obj2.a_tlf('999999999')
    print(obj2)

    #print atributs
    obj1.p_nom()
    obj2.p_nom()

    #afegir objectes a diccionari
    dic = {}
    dic[obj1.nom] = obj1
    dic[obj2.nom] = obj2
    print(dic)

    #mostrar dades objecte des de diccionari objectes
    #per __str__
    print_dic_obj(dic)

    #individual per mètode individual
    print_dic_obj_ind(dic)
"""
    #PROGRAMA ______________________________________________
    op = ''
    while op != '5':
        print_info(clients)
        print_menu()
        op = input("opció: ")
        if op in MENU.keys() or op == '':
            #print("opció vàlida")
            if op == '1':
                    alta()
            elif op == '2':
                    importa(FITXER)
            elif op == '3':
                    mostra(clients)
            elif op == '4':
                    guarda(clients,FITXER)
            elif op == '5':
                    pass
                    #sortir
        else:
            print("\n*FATAL ERROR* opció no vàlida\n")
    