from imports import *


class Node:
    def __init__(self, poidrest, niveau, numbin,conf):
        self.poidrest = poidrest    #Tableau des poids restants pour chaque boîte
        self.niveau = niveau        #Le niveau du noeud dans l'arbre
        self.numbin = numbin        #nombre de boîtes utilisées
        self.conf = conf

    def getNiveau(self):
        return self.niveau

    def getNumBin(self):
        return self.numbin

    def getpoidrests(self):
        return self.poidrest

    def getpoidrest(self, i):
        return self.poidrest[i]

    def getconf(self):
        return self.conf  



def branchAndBound(w, c):
        n = len(w)
        minBins = n  # initialiser la valeur optimale à n
        Nodes = []  # les noeuds à traiter
        poidrest = [c] * n  # initialiser les poids restants dans chaque boite [c,c,c,.......c]
        numBins = 0  # initialiser le nombre de boites utilisées
        conf = [-1] * n
        conf_opt = []
        for k in range(len(w)):
            if w[k] > c:
                print("les poids des objets ne doivent pas dépasser la capacité du bin")
                return 0
            else:
                
                curN = Node(poidrest, 0, numBins,conf)  # créer le premier noeud, niveau 0, nombre de boites utilisées 0
                
                Nodes.append(curN)  # ajouter le noeud à l'arbre

                while len(Nodes) > 0:  # tant qu'on a un noeud à traiter

                    curN = Nodes.pop()  # récupérrer un noeud pour le traiter (curN)
                    curNiveau = curN.getNiveau()  # récupérrer son niveau

                    if (curNiveau == n) and (curN.getNumBin() < minBins):  # si c'est une feuille et nbr boites utilisées < minBoxes
                        minBins = curN.getNumBin()  # mettre à jour minBoxes
                        conf_opt = curN.getconf()
                        print(conf_opt)
                        
                    else:

                        indNewBox = curN.getNumBin()
                        conf = curN.getconf() # je recupere la configuration du noeud
                        
                        if (indNewBox < minBins):

                            poidCurNiveau = w[curNiveau]

                            for i in range(indNewBox + 1):
                                
                                if (curNiveau < n) and (curN.getpoidrest(i) >= poidCurNiveau):  # si c'est possible d'insérer l'objet dans la boite i
                                    # on crée un nouveau noeud.
                                    conf[curNiveau] = i # j'insere l'affectation dans la config a l'indice de l'objet

                                    newWRemaining = curN.getpoidrests().copy()
                                    newWRemaining[i] -= poidCurNiveau  # la capacité restante i - le poids du nouvel objet

                                    if (i == indNewBox):  # nouvelle boite
                                        newNode = Node(newWRemaining, curNiveau + 1, indNewBox + 1,conf)
                                       
                                        for j in range(curNiveau + 1, len(w)):
                                            s = + w[j]

                                        if (((indNewBox + 1) + s / c) < minBins):
                                            Nodes.append(newNode)
                                    else:  # boite deja ouverte
                                        newNode = Node(newWRemaining, curNiveau + 1, indNewBox,conf)
                                        
                                        for j in range(curNiveau + 1, len(w)):
                                            s = + w[j]
                                        if ((indNewBox + s / c) < minBins):
                                            Nodes.append(newNode)
                return minBins,conf_opt
            

# meta, items = instance('N1C1W1_A.txt')
# t1 = time.time()
# a = branchAndBound(items,int(meta[0]))
# print(a,time.time()-t1)