#!/usr/bin/python3.7.9
#Importations de random et time
import random
import time
#On créé la variable sudoku
sudoku=[]



#Fonction permettant la création d'une matrix de x sur y
def matrix(x,y):
    Matrix = [[None for x in range(x)] for y in range(y)]
    return Matrix

#on genere une matrix de 9x9 et l'affecte a sudoku
sudoku = matrix(9,9)


#Fonction renvoyant la ligne d'un index
def line(sudoku,l):
    ligne=[]
    for z in sudoku[l]:
        ligne.append(z)
    return ligne

#Fonction renvoyant la colonne d'un certain index
def colonne(sudoku,c):
    col=[]
    for x in range(len(sudoku)):
        col.append(sudoku[x][c])
    return col

#A partir d'une position on obtient la valeur
def getpos(sudoku,x,y):
    return sudoku[x][y]

#Fonction permettant d'obtenir les coordonnées des valeurs du carré à partir des coordonnées d'une valeur wllh  c'est pas claire
def square(sudoku,Y,X):
    res=[]
    for y in range((Y//3)*3,(Y//3)*3+3):
        for x in range((X//3)*3,(X//3)*3+3):
            res.append([y,x])
    return res
            

#Fonction qui donne les valeurs entre 0 et 9 non présente dans la liste          
def check(l):
    v = [1,2,3,4,5,6,7,8,9]
    for x in range(len(l)):
        
        if not(l[x] == None):
            v.remove(l[x])
    return v
    
#Fonction donnant les valeurs à partir des coordonnées du carré    
def valuesquare(sudoku,l):
    res=[]
    for x in range(len(l)):
        y1=l[x][0]
        x1=l[x][1]
        res.append(sudoku[y1][x1])
    return res
    
#Fonction parmi 3 liste donne les valeurs commune a c'est liste qui seront ici les valeurs d'entrée non utilisé
def possible(l1,l2,l3):
    z=list(set(l1).intersection(l2))
    
    z=list(set(z).intersection(l3))
    return z
    
#Fonction générant un sudoku complet    
def generator():
    #Importations de sudoku
    global sudoku
    
    #Rénitialise le sudoku
    sudoku = matrix(9,9)
    #Parcour chaque valeur du sudoku
    for y in range(len(sudoku)):
        for x in range(len(sudoku[y])):
            #Essaye une partie du code provoquant une erreur 
            try:
                #print(x,y)
                #Donne la colonne
                col = colonne(sudoku,x)
                #Donne la ligne
                lig = line(sudoku,y)
                #Donne les coordonnées des valeurs du carré
                sqa = square(sudoku,y,x)
                #Donne les valeurs référé aux coordonnées
                sqa_val = valuesquare(sudoku,sqa)
                
                #Donne les valeurs possible pour chaque et donne les valeurs commune à chaque qui sont les valeurs utilisable    
                num = possible(check(col),check(lig),check(sqa_val))
                #Parmi les valeur possible en choisi une aléatoire
                numi= random.randint(0,len(num)-1)
                sudoku[y][x] = num[numi]
               
                
            #Si on rencontre une erreur alors
            except ValueError:
                #On essaye un bout de code dangereux aussi
                try:
                    #Si la dernière case n'est pas complété alors
                    if sudoku[8][8] == None:
                        #On reset le sudoku
                        sudoku = matrix(9,9)
                        
                        #et on relance cette même fonction
                        generator()
                    #Sinon on sort de l'excepte
                    else:
                        raise
                    #si on rencontre une erreur alors on sort de la fonction
                except ValueError:
                    return
                    
                    
                    


#Fonction qui supprime n nombres de valeur du sudoku
def generate(n):
    #On lance la fonction
    generator()
    #On met le compteur a zéro
    i=0
    #Tant que i est inférieur a n-1
    while i <= n-1:
        #Prend des coordonnées x , y aléatoire
        yrand = random.randint(0,len(sudoku)-1)
        xrand = random.randint(0,len(sudoku[1])-1)
        #Si elle ne sont pas égale à None alors on la transforme en None et on rajoute 1 à i
        if not(sudoku[yrand][xrand] == None):
            sudoku[yrand][xrand] = None
            i+=1
    
    return sudoku
    





    
    
    




    
