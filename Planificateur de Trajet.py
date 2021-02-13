#!/usr/bin/env python3
# -*- coding utf-8 -*-

"""Phase d'importation des différentes librairies tierces"""

###On importe la librairie Tkinter pour l'interface graphique
from tkinter import *

###Visiblement un bug de Tkinter empêche l'importation de filedialog avec les autres modules, on l'importe donc individuellement
from tkinter import filedialog

###Sert à afficher des images dans Tkinter avec moins de restriction
from PIL import Image, ImageTk

###On l'utilise pour déterminer le chemin du répertoire courant
from os import path as os_path

###On utilise configparser pour créer des fichiers de configuration
import configparser

###ast vérifie que les clés dans un fichier config ne soit pas dangereuse, et permet ainsi d'importer une liste plutôt qu'un string
import ast

###Tkinter ne gère pas par défaut des menus déroulants, on importe donc une extension de tkinter pour qu'il le fasse
from tkinter.ttk import Combobox


"""Définition des différentes variables global"""


###Pour simplifier l'écriture, on définit un raccourci avec parser vers la commande configparser.ConfigParser()
global parser
parser = configparser.ConfigParser()

###On crée notre fenetre principale
global fenetre
fenetre = Tk()

###Cette variable sert plus tard pour les radiosbuttons (Sélection entre les différents types de transports)
global v
v = StringVar()
v.set('NULL')

###Cette variable servira comme subsitution à v, afin de garder l'état des radioboutons, tout en pouvant modifier la valeur de w
global w
w = StringVar()
w.set('NULL')

###On utilise ces deux conditions afin de déterminer si les Combobox ont été utilisées, et ainsi, changer le comportement du programme
global Cond1, Cond2
Cond1 = False
Cond2 = False

###Permet de savoir si l'on doit recréer la carte ou non
global canvasCreated
canvasCreated = False

###Utilisé afin de ne pas modifier la variable trajet, pour pouvoir travailler dessus, sans modifier l'original, utilisée ailleurs
global trajetFinal
trajetFinal = []

###Utilisé afin de savoir si les Combobox ont été crées
global ComboExist
ComboExist = False

###Fichier contiendra le raccourci vers le fichier de configuration, pour pouvoir l'importer à travers le programme
global fichier
fichier = StringVar()


"""Définition des modules"""


def browse():
    """Fenêtre pour ouvrir un fichier config.ini contenant la carte désirée"""
    ###Cette commande définit la variable fichier en tant que le choix de l'utilisateur dans le fenêtre de sélection du fichier config.ini
    ###On affiche par défaut pour l'utilisateur les fichiers ini, mais tous les fichiers peuvent être sélectionnées
    fichier.set(filedialog.askopenfilename(defaultextension ='.ini', filetypes = [("Fichier de configuration ini","*.ini"),("Tous les fichiers","*.*")] ))

    ###Une fois que l'utilisateur a choisi sa config, on peut activer le choix du transport
    ###On change donc l'état des radioboutons de désactivé à normal
    RB1.configure(state=NORMAL)
    RB2.configure(state=NORMAL)
    RB3.configure(state=NORMAL)

    ###On ouvre le fichier config
    parser.read(fichier.get())

    ###On définit chacune de ses sections dans une liste nommée l
    l = parser.sections()

    ###On attribue les 3 premières sections aux noms des radioboutons, la quatrième étant reservé à autre chose
    name1.set(l[0])
    name2.set(l[1])
    name3.set(l[2])

    ###On désactive le bouton pour charger un fichier de config, car l'utilisateur en a déjà chargé un
    BrowseButton.configure(state = 'disabled')

def carteImage(transport):
    """Charge et affiche l'image de la carte depuis un fichier config.ini"""
    ###On déclare tk_img en global, sinon le "garbage collector" le videra de la mémoiren empêchant ainsi l'affichage de l'image et sa mise à jour
    global tk_img

    ###On lit le fichier de configuration chargé par l'utilisateur
    parser.read(fichier.get())

    ###On adapte le chemin de l'image pour n'importe quelle machine
    ###Pour cela on récupère le chemin courant, celui duquel le fichier python est lancé
    PATH = os_path.abspath(os_path.split(__file__)[0]) + "/"
    ###Ensuite on récupère le nom de l'image dans le fichier config
    image = parser.get('Divers', 'image')
    ###On ajoute les deux ensembles, pour créer le chemin complet
    picture = PATH+image

    ###On crée le canvas pour la carte
    ###On récupère nos deux variables global
    global canvas, canvasCreated

    ###Si le programme a dejà fonctionné une fois, on supprime la carte, pour ne pas en afficher plusieurs
    if canvasCreated == True:
        canvas.destroy()

    ###On préviens que la carte est crée avec canvasCreated
    canvasCreated = True
    ###On crée un canvas nommé "canvas", avec les dimensions de la carte, puis on l'affiche au milieu
    canvas = Canvas(sub2, width=500, height=461)
    canvas.pack(anchor = CENTER, padx=2, pady=2)

    ###Pour faciliter la manipulation de l'image, on l'appelle img
    img = Image.open(picture)
    ###Ensuite on la passe à Pillow qui la converti pour que Tkinter puisse l'afficher
    tk_img = ImageTk.PhotoImage(img)
    ###On affiche l'image dans le canvas
    canvas.create_image(250, 230, image=tk_img)

def canvasImage(trajet):
    """Affiche sur la carte les points ainsi que le chemin à l'aide du widget canvas"""
    ###On récupère nos variables global liée au canvas
    global canvas, canvasCreated

    ###Si un canvas a déjà était crée, on l'efface complètement, et on le recrée
    if canvasCreated == True:
        canvas.delete('all')
        canvas.destroy()
        carteImage(w.get())

    ###On lit le fichier config
    parser.read(fichier.get())

    ###On duplique notre liste nommée trajet
    trajetFinal = list(trajet)

    ###On récupère les coorodonnées des points de la carte dans le fichier config
    coordonnées = ast.literal_eval(parser.get('Divers','coords'))

    for i in range (0,len(coordonnées)) :
        x = coordonnées[i][2]
        y = coordonnées[i][3]
        ### On crée un point noir pour chaque ville
        canvas.create_oval((x-2),(y-2),(x+2),(y+2), outline = 'black', fill='black')

    points = [[] for i in range(0,len(trajet))]

    for i in range (0, len(trajet)) :
    ### Permet d'ajouter le nom des villes ainsi que de repasser leurs points en rouge

        for j in range(0, len(coordonnées)) :
            if trajet[i] == coordonnées[j][0] :
                ### On prend les coordonées de chaque ville pour les mettre dans une liste
                points[i].append(coordonnées[j][2])
                points[i].append(coordonnées[j][3])

                ### On ajoute le texte au canvas (la position du texte n'est pas la même selon les villes y afin d'éviter un chevauchement du texte selon les zones)
                if j == 15 :
                    canvas.create_text(points[i][0]-5, points[i][1]-17, anchor='ne', text=coordonnées[j][1])
                elif j == 16 :
                    canvas.create_text(points[i][0]-5, points[i][1], anchor='ne', text=coordonnées[j][1])
                elif coordonnées[j][3] > 280 :
                    canvas.create_text(points[i][0]-5, points[i][1]-11, anchor='ne', text=coordonnées[j][1])
                else :
                    canvas.create_text(points[i][0]-5, points[i][1]+2, anchor='ne', text=coordonnées[j][1])

        ### On repasse en rouge les points des villes qui font partie de la liste trajet
        canvas.create_oval((points[i][0]-4),(points[i][1]-4),(points[i][0]+4),(points[i][1]+4), outline = 'red', fill='red')

    for i in range(0, len(trajet)-1) :
        ### On crée les segments entre les points
        canvas.create_line(points[i][0],points[i][1], points[i+1][0], points[i+1][1],fill='red')

    ###On force la mise à jour des informations du canvas
    canvas.update_idletasks()
    canvas.update()

def TypeTransport(type):
    """Active le reste du programme selon le transport choisi"""
    ###On lit le fichier config
    parser.read(fichier.get())

    ###On assigne les sections de config à l
    l = parser.sections()

    ###On crée une variable qui donne le type de transport séléctioné par l'utilisateur
    if type == 'sec1':
        w.set(l[0])
    elif type == 'sec2':
        w.set(l[1])
    elif type == 'sec3':
        w.set(l[2])

    ###On appelle la fonctionne qui se charge d'afficher la carte
    carteImage(w.get())

    ###On récupère les villes (on crée deux listes dans le cas où il faudrait en modifier une des deux plus tard)
    villeDepartList = ast.literal_eval(parser.get('Divers', 'villes'))
    villeArriveeList = ast.literal_eval(parser.get('Divers', 'villes'))

    ###On récupère notre variable global
    global ComboExist

    ###Si les combobox ne sont pas encore configurées, alors on exécute ce code
    if ComboExist == False:
        """On change le statue des combobox, et on leur donne leur liste de points"""
        BDepart.configure(state=NORMAL)
        BDepart['values'] = villeDepartList
        BArrivee.configure(state=NORMAL)
        BArrivee['values'] = villeArriveeList
        ###On préviens que les Combobox sont configurées
        ComboExist = True

    ###On préviens l'utilisateur qu'il faut désormais qu'il choisisse une ville de départ
    Depart(0)

def Depart(de):
    """Préviens le reste du programme que la ville de départ est chosie"""
    global Cond1
    ###Si Combobox Départ n'a plus sa valeur de départ, une ville est forcément sélectionée
    if villeDepart.get() != '''Ville de départ''':
        ###Ainsi on transforme le nom de la ville en nombre
        numDepart = convVilleDep(villeDepart.get())
        ###On préviens que la ville de départ est sélectionée
        Cond1 = True
        ###On appelle la suite du programme
        binder()
    else:
        Cond1 = False
        line1.set("""Vous n'avez pas sélectionné la ville de départ""")

def Arret(ar):
    """Même fonction que Depart() mais pour l'arrivée"""
    global Cond2
    if villeArrivee.get() != '''Ville d'arrivée''':
        numArrivee = convVilleAr(villeArrivee.get())
        Cond2 = True
        binder()
    else:
        print('FAUX')
        line1.set("""Vous n'avez pas sélectionné la ville d'arrivée""")

def binder():
    """Binder rassemble les différentes fonctions du programme"""
    ###On remet la ligne 1 à zéro, on ne veut rien d'écrit dessus
    line1.set('')

    ###Si les deux villes sont sélectionnées, on exécute ce code
    if Cond1 == True and Cond2 == True:
        ###On associe la variable noms, à son équivalent dans le fichier config, de même pour ville_inaccessible et double_sens
        noms = Reader(w.get(), 'noms')
        ville_inaccessible = Reader(w.get(), 'ville_inaccessible')
        double_sens = Reader(w.get(), 'double_sens')

        ###Si jamais une ville n'est plus accessible, on préviens l'utilisateur
        if convVilleDep(villeDepart.get()) in ville_inaccessible:
            line1.set('''Ville de départ non reliée par ce mode de transport''')

        ###De même pour l'arrivée
        elif convVilleAr(villeArrivee.get()) in ville_inaccessible:
            line1.set('''Ville d'arrivée non reliée par ce mode de transport''')

        ###Si la ville de départ est la même que celle d'arrivée, on préviens l'utilisateur
        elif villeArrivee.get() == villeDepart.get():
            line1.set('''ERREUR FATALE ! LA VILLE D'ARRIVEE EST LA MEME QUE CELLE DE DEPART''')
            line2.set('''Veuillez sélectionnez une ville différente''')

        ###Si aucun problème n'est rencontré, on peut exécuter l'algorithme de Dijkstra
        else:
            ###On crée une matrice complète à partir du fichier config
            m_adjac = Generateur_Matrice(convVilleDep(villeDepart.get()), convVilleAr(villeArrivee.get()), noms, double_sens)

            ###On exécute Dijkstra, et on récupère la liste des villes à traverser, ainsi que le temps de voyage prévu, et la liste avec des noms
            trajet, tps, trajet_noms = matriceDijkstra(len(noms),m_adjac,noms)

            ###On affiche le trajet sur la carte
            canvasImage(trajet)

            ###Comme *.set n'accepte qu'une variable ou un string, on crée une variable avec les trajets et une phrase qui indique à l'utilisateur ce qu'on lui affiche
            trajetTotal = "Vous devrez passer par ces villes : ",trajet_noms
            ###On affiche cette variable en ligne 2
            line2.set(str(trajetTotal))

            ###De même pour le temps de trajet
            tpsTotal = "Temps total du trajet : ",tps, "minutes"
            line3.set(str(tpsTotal))

            ###On nettoie la ligne 4, pour être sur qu'elle n'affiche pas d'informations qui n'ont plus d'utilité
            line4.set("")

    ###Si l'utilisateur n'a pas encore choisi le départ et l'arrivée, on lui prévient de le faire
    else:
        line4.set('''Sélectionnez l'autre lieu''')

def convVilleDep(test):
    """Change les noms de villes en numéros"""
    ###On préviens que la ville n'est pas encore trouvée
    found = False

    ###On crée une variable i pour une boucle while qui démarre à -1
    i = -1

    ###On lit le fichier config
    parser.read(fichier.get())

    ###On récupère la liste noms de manière sécurisée
    noms = ast.literal_eval(parser.get(w.get(), 'noms'))

    ###On crée une boucle qui dure jusqu'à ce que l'on trouve la ville désirée
    while found == False:
        ###On incrémente i à chaque tour
        i = i+1
        ###On vérifie si test à la même valeur qu'une ville dans noms, si c'est le cas, on attribue i à test
        if test == str(noms[i][1]):
            ###On préviens la boucle qu'elle peut s'arrêter
            found = True
            return i

###Même utilité qu'au dessus
def convVilleAr(test):
    found = False
    i = -1
    parser.read(fichier.get())
    noms = ast.literal_eval(parser.get(w.get(), 'noms'))
    while found == False:
        i = i+1
        if test == str(noms[i][1]):
            return i

def Reader (carte, objet):
    """Permet de prendre des valeurs du fichier .ini"""
    return ast.literal_eval(parser.get(carte, objet))

def Generateur_Matrice (ville_départ, ville_arrivée, noms, double_sens) :
    """ Fonction qui génère la matrice adjacente en fonction des villes de départ et d'arrivée  """
    Nb = len(noms)

    ### On change les places des villes tel que la ville de départ soit en position 0 ...
    ### ... et que celle d'arrivée soit en dernière

    for i in range (0, Nb) :
        if noms[i][0] == ville_départ :
            ### On inverse noms[0] avec noms[i] qui représente la ville de départ
            noms[0] , noms[i] = noms[i] , noms[0]

    for i in range (0, Nb) :
        if noms[i][0] == ville_arrivée :
            ### Idem avec la ville d'arrivée qui échange de place avec la dernière ville
            noms[Nb-1] , noms[i] = noms[i] , noms[Nb-1]

    ### On crée la matrice remplie de 0 pour être complétée
    matrice = [[0 for i in range(0, Nb)] for j in range (0,Nb)]

    for i in range (0, Nb) :
        ### On complète la matrice ligne par ligne (i représentant les 'lignes')

        for j in range (2, len(noms[i])) :
            ville_accessible = noms[i][j][0]
            ### Donne le numéro de la gare j qui est reliée à la gare i

            for n in range (0, Nb) :
                if ville_accessible == noms[n][0]:
                    ### On prend la position de la gare j dans la liste noms
                    ### On écrit la durée du trajet (noms[i][j][1]) dans la matrice à la ligne i et ...
                    ### ... à la colonne qui correspond à la position de la gare j dans la liste noms
                    matrice[i][n] = noms[i][j][1]

                    if double_sens == True :
                        ### Si les trajets existent dans les deux sens, on peut aussi le noter le trajet sur la ligne de la gare j ...
                        ### ... sur la colonne de celle de i
                        matrice[n][i] = noms[i][j][1]

    ### Le programme retourne la matrice adjacente pour être utilisée par l'Algorithme de Dijkstra
    return matrice

def matriceDijkstra(Nvilles,m_adjac, noms):
    """Algorithme de Dijkstra, fonctionnant avec des matrices, converti sous Python"""

    ###On crée une liste vide pour notre tableau
    DIJ = []

    ###On crée une boucle qui va créer le tableau correctement, selon le nombre d'arrêts
    for i in range (Nvilles):
        DIJ.append([1000000,"X","N"])
        ville_select=0
        dist_interm=0

    ###On début l'algorithme, qui fonctionnera jusqu'à-ce que tout les arrêts aient été testés
    while ville_select != Nvilles-1:

        ###Comme Python ne permet pas de facilement créer des variables infinies, on en crée une suffisament grande pour qu'elle représente l'infini et soit inatteignable, après elle servira à connaître les distances minimales
        minimum = 1000000

        ###On démarre la boucle qui vérifie les distances séparant chaque point, à partir de la première ville sélectionnée, puis la seconde, jusqu'à la dernière
        for n in range(1,Nvilles):
            if DIJ[n][2] == "N":

                ###On ajoute les distances entre deux points pour les comparer plus tard
                dist = m_adjac[ville_select][n]
                dist_totale = dist_interm + dist

                ###On vérifie que la distance totale soit bien la plus plus petite
                if dist !=0 and dist_totale < DIJ[n][0]:
                    DIJ[n][0] = dist_totale
                    DIJ[n][1] = ville_select

                ###On vérifie aussi qu'elle ne soit pas égale à l'infini et on donne la distance minimum comme étant celle trouvée
                if DIJ[n][0]<minimum:
                    minimum=DIJ[n][0]
                    pville_select=n

        ###On finit la boucle, on remplit le tableau correctement
        ville_select=pville_select
        DIJ[ville_select][2]="0"
        dist_interm=DIJ[ville_select][0]

    ###On crée enfin une dernière liste qui affichera les points à emprunter
    chemin = []
    ville = Nvilles-1
    chemin.append(ville)
    while ville !=0:
        ville = DIJ[ville][1]
        chemin.append(ville)

    ###On inverse la liste
    chemin.reverse()

    ### On crée une autre liste avec cette fois les numéro correspondants à chaque ville, et non leurs positions dans la liste
    trajet = []
    trajet_noms = []
    for i in range (0, len(chemin)) :
            for j in range (0, len(noms)) :
                    if chemin[i] == j :
                            trajet.append(noms[j][0])
                            trajet_noms.append(noms[j][1])

    return trajet, DIJ[Nvilles-1][0], trajet_noms


"""------------------------------------ CORPS DU PROGRAMME ------------------------------------"""

###On nomme notre fenêtre, et on indique sa taille
fenetre.title('GPS Polyvalent (Dijkstra Edition)')
fenetre.geometry('1010x650')

###On veut pouvoir modifier le contenu des LabelFrame de partout dans le programme
global sub0, sub1, sub2, sub3

###On crée quatre sous ensemble de widget pour donner une structure générale à notre programme
###On définit leur taille selon celle de la fenêtre pour qu'ils occupent une proportion de la fenêtre
###On les étends dans tout les sens pour qu'ils prennent toute la place qu'on leur attribue
###Enfin, on ajoute simplement deux pixels entre chaque LabelFrame, pour aérer un peu
###La valeur grid_propagate permet à un widget d'avoir le pas sur un autre quand il s'étends
###Dans ce cas on veut que la carte prennent de la place supplémentaire si elle en a besoin
sub0 = LabelFrame(fenetre, text = "Sélection de la carte : ")
sub0.grid(column = 0, row=0, rowspan=1, columnspan=1, sticky=N+S+E+W, padx=2, pady=2)

sub1 = LabelFrame(fenetre, text = """Sélection d'arrêts : """)
sub1.grid(column=0, row=2, rowspan=3, columnspan=1, sticky=N+S+E+W, padx=2, pady=2)

sub2 = LabelFrame(fenetre, text = """Carte : """)
sub2.grid(column=2, row=0, columnspan=4, rowspan=4, sticky=N+S+E+W, padx=2, pady=2)
sub2.grid_propagate('false')

sub3 = LabelFrame(fenetre, text = """Résumé du voyage : """)
sub3.grid(column=2, row=4, columnspan=4, rowspan=1, sticky=N+S+W+E, padx=2, pady=2)
sub3.grid_propagate('false')

###On donne un poids à nos LabelFrame, afin qu'ils puissent s'étendre correctement
fenetre.columnconfigure(sub0, weight=1)
fenetre.rowconfigure(sub0, weight=1)

fenetre.rowconfigure(sub1, weight=1)
fenetre.columnconfigure(sub1, weight=1)

fenetre.columnconfigure(sub2, weight=1)
fenetre.columnconfigure(sub3, weight=1)

###Configuration de sub0
###on crée le bouton qui servira à sélectionner notre fichier de Configuration
global BrowseButton
BrowseButton = Button(sub0, text = 'Ouvrir...', command = browse, relief="raised")
BrowseButton.grid(row=0, columnspan=3, sticky=W+E, padx=5)
sub0.columnconfigure(BrowseButton, weight=1)
sub0.rowconfigure(BrowseButton, weight=1)

###On veut pouvoir activer et désactiver à la volée nos radioboutons depuis d'autres modules
###On veut aussi pouvoir récupérer la valeur de chaque radioboutons
global RB1, RB2, RB3
global name1, name2, name3
###Ainsi on crée trois variables dynamiques de type StringVar
###L'avantage de ces variables est qu'elle avertissent seul le programme que leur état est différents
###Ainsi le programme se met à jour automatiquement
name1 = StringVar()
name2 = StringVar()
name3 = StringVar()

###On crée trois Radiobuttons avec trois types de transport différents.
###On définit leurs noms selon le fichier config
###On leur donne une valeur qui nous permettra de configurer correctement w
###Elles appellent la fonction TypeTransport seulement quand on clique dessus
RB1 = Radiobutton(sub0, textvariable=name1, variable=v, value="sec1", command=lambda : TypeTransport(v.get()))
RB1.grid(row=1, column=0, padx=2, pady=2)
RB2 = Radiobutton(sub0, textvariable=name2, variable=v, value="sec2", command=lambda : TypeTransport(v.get()))
RB2.grid(row=1, column=1, padx=2, pady=2)
RB3 = Radiobutton(sub0, textvariable=name3, variable=v, value="sec3", command=lambda : TypeTransport(v.get()))
RB3.grid(row=1, column=2, padx=2, pady=2)

###Ces radioboutons sont désactivés du temps que le fichier de config n'est pas chargé
RB1.configure(state=DISABLED)
RB2.configure(state=DISABLED)
RB3.configure(state=DISABLED)


###Configuration de sub1
###On crée un texte
Label(sub1, text='Ville de départ : \n').pack(fill=X, padx=2, pady=2)

###On définit une variable dynamique de type "String", nécessaire pour afficher le texte par défaut dans la Combobox
global villeDepart
villeDepart = StringVar()
###On donne sa valeur à notre StringVar() précédent
villeDepart.set('''Ville de départ''')

### On ajoute le bouton et la variable contenant notre liste de villes à global, pour pouvoir les modifier de partout
global BDepart, villeDepartList
###On crée notre variable vierge
villeDepartList = ()

###On crée notre Combobox
###On lui associe une fonction lorsqu'on la sélectionne
###On configure sa taille et son état
BDepart = Combobox(sub1, textvariable=villeDepart, values = villeDepartList, state = 'readonly')
BDepart.bind("<<ComboboxSelected>>", Depart)
BDepart.pack(fill=X, padx=2, pady=2)
BDepart.configure(state = DISABLED)

###On crée un espace entre les deux Combobox
Label(sub1, text='\n\n\n\n').pack(padx=2, pady=2)

###Même chose que pour la ville de départ, mais cette fois ci pour l'arrivée
Label(sub1, text='''Ville d'arrivée : \n''').pack(fill=X, padx=2, pady=2)

global villeArrivee
villeArrivee = StringVar()
villeArrivee.set('''Ville d'arrivée ''')

global BArrivee
global villeArriveeList
villeArriveeList = ()
BArrivee = Combobox(sub1, textvariable=villeArrivee, values = villeArriveeList, state = 'readonly')
BArrivee.bind("<<ComboboxSelected>>", Arret)
BArrivee.pack(fill=X, padx=2, pady=2)
BArrivee.configure(state=DISABLED)



###Configuration de sub3
###On permet de modifier les 4 lignes de sub3, en les rendant globales
###De plus comme ce sont des StringVar(), elles se mettent à jour automatiquement
global line1, line2, line3, line4
line1, line2, line3, line4 = StringVar(), StringVar(), StringVar(), StringVar()

Label(sub3, textvariable = line1).pack(padx=2, pady=2)
Label(sub3, textvariable = line2).pack(padx=2, pady=2)
Label(sub3, textvariable = line3).pack(padx=2, pady=2)
Label(sub3, textvariable = line4).pack(padx=2, pady=2)

###On affiche la fenetre, et on mets sur pause l'exécution du programme, c'est-à-dire qu'il attend une action de l'utilisateur pour continuer
fenetre.mainloop()
