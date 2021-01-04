from copy import deepcopy
from math import sqrt

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

