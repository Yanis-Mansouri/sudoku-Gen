#Importations
from copy import deepcopy
from math import sqrt

#Ici on importe l'autre script pour générer un sudoku
from sudoku_generator import generate
from tkinter import *
from tkinter import messagebox
from time import *

#Créations de la fenêtre
mywindow = Tk()

#Variable stockant tout les numeros de l'interface graphique
numbers=[]

#Variable ou est le Sudoku
sudoku=[]

#Variable du sudoku avant résolution
oldSudoku=[]

#Variable du temps mit pas le générateur
genproc = 0

#Défini si on peut changer la couleur des chiffre en rouge
rouged  = False

#CoolDown du générateur
cooldownGen= 0

#CoolDown du Resolvateur
cooldownRes=0
#Taille de l'écran en longeure
screen_width = mywindow.winfo_screenwidth()

#Taille de l'écran en largeur
screen_height = mywindow.winfo_screenheight()

#Print avec code couleur des dimensions 
print(f"\033[1;37;40m Dimensions: \033[1;32;40m{screen_width}x{screen_height}")



#Résolvateur de grille de sudoku
def Resolve(Sudoku):
    
    
    #Duplique une list sans que la list principal ne se modifie
    def DupList(List):
        return deepcopy(List)
    
    #vérifie qu'il y ai bien le bon nombre de chiffre dans la grille
    def Valid(Sudoku):
        if(Sudoku==None):
            return False
        for y in range(len(Sudoku)):
            hor=[n+1 for n in range(len(Sudoku))]
            ver=[n+1 for n in range(len(Sudoku))]
            for x in range(len(Sudoku)):
                try:
                    hor.remove(Sudoku[y][x])
                    ver.remove(Sudoku[x][y])
                except ValueError:
                    return False
        return True
    
    #enlève les chiffre impossible des lignes hor/vert en xy
    def Line(Sudoku,y,x,possible):
        for i in range(len(Sudoku)):
            
            #On enlève à chaque fois les chiffres qu'on trouve sur la ligne et sur la colone
            #Ligne
            try:
                possible.remove(Sudoku[y][i])
            except: pass
            
            #Colone
            try:
                possible.remove(Sudoku[i][x])
            except: pass
    
    #enlève les chiffre impossible dans le sous carré en xy
    def Square(Sudoku,Y,X,possible):
        #Prend les dimenssions d'un sous carré
        i=int(sqrt(len(Sudoku)))
        #(Y//i)*i,(Y//i)*i+i correspond au début et la fin de la grille pareil pour (X//i)*i,(X//i)*i+i
        for y in range((Y//i)*i,(Y//i)*i+i):
            for x in range((X//i)*i,(X//i)*i+i):
                try:
                    possible.remove(Sudoku[y][x])
                except: pass
    
    #modification des possibilité pour les cases alentoure à l'ajout d'une case trouvé
    def HVAdd(Sudoku,y,x,rest):
        for i in range(len(Sudoku)):
            
            #Ligne
            if(type(Sudoku[y][i])==list):
                #si c'est une list (case vide)
                try:
                    Sudoku[y][i].remove(Sudoku[y][x])
                    #si il ne reste qu'une possibilité
                    if(len(Sudoku[y][i])==1):
                        AddNumber(Sudoku,y,i,rest)
                except: pass
                
            #Colonne
            if(type(Sudoku[i][x])==list):
                #si c'est une list (case vide)
                try:
                    Sudoku[i][x].remove(Sudoku[y][x])
                    #si il ne reste qu'une possibilité
                    if(len(Sudoku[i][x])==1):
                        AddNumber(Sudoku,i,x,rest)
                except: pass
                
    #modification des possibilité à l'ajout d'une case trouvé pour les sous carré
    def SquareAdd(Sudoku,Y,X,rest):
        #Prend les dimenssions d'un sous carré
        i=int(sqrt(len(Sudoku)))
        #(Y//i)*i,(Y//i)*i+i correspond au début et la fin de la grille pareil pour (X//i)*i,(X//i)*i+i
        for y in range((Y//i)*i,(Y//i)*i+i):
            for x in range((X//i)*i,(X//i)*i+i):
                if(type(Sudoku[y][x])==list):
                    #si c'est une list (case vide)
                    try:
                        #si il ne reste plus qu'une possibilité
                        Sudoku[y][x].remove(Sudoku[Y][X])
                        if(len(Sudoku[y][x])==1):
                            AddNumber(Sudoku,y,x,rest)
                    except: pass
    
    #les valeurs possible pour une case
    def ValidPossibilities(Sudoku,y,x):
        possible=[n+1 for n in range(len(Sudoku))]
        Line(Sudoku,y,x,possible)
        Square(Sudoku,y,x,possible)
        return possible
    
    #Ajout un chiffre dans la grille 
    def AddNumber(Sudoku,y,x,rest):
        rest.remove([y,x])
        Sudoku[y][x]=Sudoku[y][x][0]
        HVAdd(Sudoku,y,x,rest)
        SquareAdd(Sudoku,y,x,rest)
    
    #Quand le process logique ne peut plus avancer on test un reponse pour une case
    def Rand(Sudoku,Rest):
        #On prend une case vide et on essaye chacune de ses possibilité
        for i in Sudoku[Rest[0][0]][Rest[0][1]]:
            #On duplique la list pour ne pas modifier la première
            sudoku_2=DupList(Sudoku)
            #On change la case à tester par chacune de ses possibilités
            sudoku_2[Rest[0][0]][Rest[0][1]]=i
            #On essaye de le résoudre
            a=Resolve(sudoku_2)
            #On vérifie que le sudoku donné sois valid
            if(Valid(a)):
                #si oui on le renvoie
                return a
        return None

    #Main
    #Prend les dimenssions d'un sous carré
    ind=int(sqrt(len(Sudoku)))
    rest=[]
    for y in range(len(Sudoku)):
        for x in range(len(Sudoku)):
            #pour chaque type de case vide (list,None ou 0)
            if(Sudoku[y][x]==None or type(Sudoku[y][x])==list or Sudoku[y][x]==0):
                #On va cherher à tous ce qu'il pourrait avoir comme possibilités
                Sudoku[y][x] = ValidPossibilities(Sudoku,y,x)
                #on le rajoute dans la list des case vide
                rest.append([y,x])
                #si il n'y a qu'une possibilitée
                if(len(Sudoku[y][x])==1):
                    AddNumber(Sudoku,y,x,rest)
    #repeat correspond au nombre de case vérifié sans qu'il n'y ait une de modification
    repeat=0
    while(len(rest)!=0):
        #on rajoute un à repeat
        repeat+=1
        #si on a testé toutes les cases et qu'aucune n'a été modifié
        if(repeat==len(rest)):
            #on fais un test
            a=Rand(Sudoku,rest)
            if(a==None):
                #si impossible on renvoie None
                return None
            else:
                #Sinon on renvoie la bonne grille
                return a
        #on change l'ordre de la list rest (a,b,c -> b,c,a -> c,a,b)
        rest.append(rest.pop(0))
        #On récupère chaque possibilités d'une case vide 
        possible=[n for n in Sudoku[rest[0][0]][rest[0][1]]]
    
        #On regarde dans la grille
        for y in range((rest[0][0]//ind)*ind,(rest[0][0]//ind)*ind+ind):
            for x in range((rest[0][1]//ind)*ind,(rest[0][1]//ind)*ind+ind):
                #si c'est une list et qu'elle n'est pas la case vide que l'on cherhce à modifier
                if(type(Sudoku[y][x])==list and (y!=rest[0][0] or x!=rest[0][1])):
                        for i in Sudoku[y][x]:
                            try:
                                #on enlève les possibilités en commun
                                possible.remove(i)
                            except: pass
        try:
            #si la case vide possède un chiffre different de toutes les case de la grille
            if(len(possible)==1):
                #On change les possiblité de la case vide
                Sudoku[rest[0][0]][rest[0][1]]=possible
                AddNumber(Sudoku,rest[0][0],rest[0][1],rest)
                #on a changé une case donc on remet repeat à 0
                repeat=0
        except : pass
        
    return Sudoku



#Début de la fonction main 
def main(mywindow,canvas,cooldownGen,cooldownRes):
    #Importations des variable sudoku et oldSudoku
    global sudoku
    global oldSudoku
    
    #Agence l'interface
    canvas.pack()
    
    #Nombre de colonne et ligne de la grille
    n=9
    
    #Taille en px de chaque petit carré 
    z=75
    
    #On lance la fonction grille et on stock les valeurs retourné dans deux variables
    posx,posy = grille(mywindow,canvas,n,z)
    #On écrit le titre
    canvas.create_text(screen_width//2 , posy-100, text="SUDOKU GENERATOR", font="Arial 16 bold", fill="black")
    
    #On écrit le temps prix par la génération qu'on stock dans une variable
    GenProcText = canvas.create_text(posx+z*4.5, posy-70, text=f"La génération a prit {genproc}s", font="Arial 10 bold", fill="black")
    #On ecrit le nom des fameux créateur de ce programme
    Creator = canvas.create_text(15, screen_height - 120, text="Mathis feat Yanis", font="Arial 8",anchor=NW ,fill="black")
    
    
    #On lance la fonction display qui affiche les chiffres
    display(mywindow,canvas,posx,posy,n,z)
    
    
    #Création du bouton  Génération lançant la fonction LaunchGen
    bouttonGen = Button(mywindow,text="Génération",command=lambda: LaunchGen(mywindow,GenProcText,cooldownGen))
    canvas.create_window(posx+z*1.5,posy-5, window=bouttonGen,anchor=S)
    
    #Création du bouton  Résolution lançant la fonction LaunchRes
    bouttonRes = Button(mywindow,text="Résolution",command=lambda: LaunchRes(mywindow,GenProcText,cooldownRes))
    canvas.create_window(posx+z*4.5,posy-5, window=bouttonRes,anchor=S)
    
    #Création du bouton  Réinitialiser lançant la fonction LaunchClear
    bouttonRen = Button(mywindow,text="Réinitialiser",command=lambda: LaunchClear(mywindow,GenProcText))
    canvas.create_window(posx+z*7.5,posy-5, window=bouttonRen,anchor=S)
    
    
    #Si la variable Rouged est fausse alors on parcours oldSudokue et on change les None en 10 et le reste en None
    if rouged  == False :
        for y in range(len(oldSudoku)):
            for x in range(len(oldSudoku[y])):
                if oldSudoku[y][x] == None:
                    oldSudoku[y][x] = 10
                else:
                    oldSudoku[y][x]=None
    #On actualise la fenêtr
    mywindow.update()
    
#Fonction LaunchClear suprimmant tout les nombres et le temps mit par la fonction génération
def LaunchClear(mywindow,GenProcText):
    #Importations des variables  numbers et rouged
    global numbers
    global rouged
    rouged  = False
    #Suppresion des chiffres
    for i in range(len(numbers)):
        canvas.delete(numbers[i])
    #Suppression du temps mit pour la génération
    canvas.delete(GenProcText)
    
#Fonction LaunchGen 
def LaunchGen(mywindow,GenProcText,cooldownGen):
    #Importations de differente variable
    global numbers
    global sudoku
    global genproc
    global oldSudoku
    global rouged
    
    #Temps de coolDown
    cooldownGen = perf_counter()- cooldownGen
    
    #Si le cooldown est superieur à 2s alors on excute la generation sinon on créé une pop-up
    if cooldownGen>=2:
        #Mets rouged a false
        rouged  = False
        #Prise du temps actuel
        tps1 = process_time()
        #On lance la fonction generate prenant en paramètre le nombre de  chiffre à enlevé et on stock le resultat
        sudoku=generate(50)
        #Prise du second temps
        tps2 = process_time()
        #On obtient la durée d'éxcution
        ltime = tps2 - tps1
        #on copie la liste  sudoku dans old Sudoku
        oldSudoku=deepcopy(sudoku)
        
        #On supprime les chiffre de l'interface
        for i in range(len(numbers)):
            canvas.delete(numbers[i])
        #On supprime le temps d'éxecution
        canvas.delete(GenProcText)
        
        genproc = ltime
        #On actualise la page
        mywindow.update()
        #On reset  le cooldown
        cooldownGen= perf_counter()
        #et on lance la fonction main 
        main(mywindow,canvas,cooldownGen,2)
    else:
        #Création de la pop-up nous disant d'aller moin vite
        
        messagebox.showwarning(title="Vous allez trop vite", message="Attendez 2s avant de relancer la génération!")
        
        #print le temps a attendre
        print("wait please",cooldownGen)


def LaunchRes(mywindow,GenProcText,cooldownRes):
    #Importations du differente variable
    global numbers
    global sudoku
    global rouged
    
    #On calcule le cooldown
    cooldownRes = perf_counter()- cooldownRes
    #Si le cooldown est superieur à 2s alors on excute la generation sinon on créé une pop-up
    if cooldownRes>=2:
        rouged = True
        #On appelle la fonction Resolve et on stock le sudoku resolu dans sudoku
        sudoku=Resolve(sudoku)
        
        #On supprime les chiffre de l'interface
        for i in range(len(numbers)):
            canvas.delete(numbers[i])
        #On supprime le temps d'éxecution
        canvas.delete(GenProcText)
        #On mets a jour la fenêtre
        mywindow.update()
        #On reset de cooldown
        cooldownRes= perf_counter()
        #On lance la fonction main 
        main(mywindow,canvas,2,cooldownRes)
    else:
        messagebox.showwarning(title="Vous allez trop vite", message="Attendez 2s avant de relancer la résolution!")
        print("wait please",cooldownGen)
    
#Fonction Display affichant les chiffres  
def display(mywindow,canvas,posx,posy,n,z):
    #Importations de numbers
    global numbers
    #Parcour le suudoku
    for y in range(len(sudoku)):
        for x in range(len(sudoku[0])):
            #si pour les mêmes index la valeur n'y était pas après la génération on la colori en rouge sinon en noir
            if oldSudoku[y][x] == 10:
                numbers.append(canvas.create_text(posx+x*z+(z//2), posy+y*z+(z//2), text=sudoku[y][x], font="Arial 16 bold", fill="red"))
            else:
                numbers.append(canvas.create_text(posx+x*z+(z//2), posy+y*z+(z//2), text=sudoku[y][x], font="Arial 16 bold", fill="black"))
    
#Fonction grille qui créée la grille du sudoku
def grille(mywindow,canvas,n,z):
    #On ajoute 1 a n
    n +=1
    
    #Calcule de la position centrale a partir de la taille de l'écran
    posx= (screen_width//2)-((n-1)*z)//2
    posy= (screen_height//2)-((n-1)*z)//2
    
    #on créé les lignes de la grille verticale
    for x in range(n):
        #Si x est divisible par trois alors on double l'epaisseur sinon on la laisse à 2
        if x%3==0:
            wi=4
        else:
            wi =2
        #On créé la ligne dont la position dépand de la position relative central quon decale de 75 en x à chaque itération
        canvas.create_line(z*x+posx, posy, z*x+posx, posy+(n-1)*z,width=wi)
    for y in range(n):
        #Si y est divisible par trois alors on double l'epaisseur sinon on la laisse à 2
        if y%3==0:
            wi=4
        else:
            wi =2
        #On créé la ligne dont la position dépand de la position relative central quon decale de 75 en y à chaque itération
        canvas.create_line(posx,posy+z*y,posx+(n-1)*z,y*z+posy,width=wi)
        mywindow.update()
    #On retourne les position relative a cette grille
    return posx,posy
    
#Donne le nom de la fenêtre
mywindow.wm_title("SUDOKU")

#Définie la couleur de la fenêtre
mywindow.configure(bg="white")

#Fait en sorte que la fenêtre sont en pleine écran
mywindow.state("zoomed")

#Créé l'air ou on pourra ajouté des élément de meme taille que l'ecran et de fond blanc
canvas = Canvas(mywindow,width=screen_width, height=screen_height, background='white')
    
#Lance la fonction main
main(mywindow,canvas,cooldownGen,cooldownRes)
#Fait entré  la fenêtre dans un état passif
mywindow.mainloop()

