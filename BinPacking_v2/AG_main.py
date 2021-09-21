from GeneticAlgorithm import GeneticAlgorithm,Item
from random import shuffle
from datetime import datetime
import json
import time

def AG(items,capacite,POPULATION_SIZE = 50,MAX_GENERATIONS = 250,MAX_NO_CHANGE = 50 ,TOURNAMENT_SIZE = 20 ,MUTATION_RATE = 0.3 ,CROSSOVER_RATE = 0.6, population=None):
#with open('N1C3W1_A.txt', 'r') as file:
    #donnees = file.read().splitlines()
    #récupérer des objets, la capacité des box et le nombre total des objets
    nb_objets= items[0]
    objets = [Item(size=i) for i in items]
    shuffle(objets)
    #appliquer l'algorithme génétique et calculer le temps d'execuction
    solution = GeneticAlgorithm(capacite, objets,POPULATION_SIZE = 50,MAX_GENERATIONS = 250,MAX_NO_CHANGE = 50 ,TOURNAMENT_SIZE = 20 ,MUTATION_RATE = 0.3 ,CROSSOVER_RATE = 0.6, population=None)
    temps_Debut_exec = datetime.now()
    total_iter, x, best_conf = solution.run()
    temps_apres_exec= datetime.now()
    temps_exec = (temps_apres_exec - temps_Debut_exec).total_seconds()

    #for objet in objets:
    #best_conf
    beConf = []
    for i,bin in enumerate(best_conf):
                for item in bin.getItems():
                    #print("type of solution",item.getSize())
                    beConf.append([item.getSize(),i])

    print(beConf)           
    #afficher les résultats de l'algorithme
    print(nb_objets)
    print(capacite)
    print(str(temps_exec))
    print(solution.best_solution.num_bins)
    print(total_iter)
    return solution.best_solution.num_bins,beConf