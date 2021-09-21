from hyperopt import hp,fmin, tpe, space_eval, STATUS_OK, Trials
from hyperopt.pyll.base import scope
from GeneticAlgorithm import AG
from SimulatedAnnealing import recuit_simule
from TabuSearch import TS
from Heuristics import heuristic_FFD
from imports import instance , instance_v2
import numpy as np
import time

def HAG():
        return 0
        


global FILE


def objective_hyper_AG(arg):
    items,_,c,_ = instance_v2(FILE)
    POPULATION_SIZE, MAX_GENERATIONS, MAX_NO_CHANGE,TOURNAMENT_SIZE, MUTATION_RATE, CROSSOVER_RATE = arg  
    nbin,conf,exec_time = HAG(items, c,POPULATION_SIZE, MAX_GENERATIONS, MAX_NO_CHANGE, TOURNAMENT_SIZE, MUTATION_RATE, CROSSOVER_RATE) 
    print(arg,nbin)
    return exec_time + nbin * 2
    
    
    
#return exec_time + (bins*2) #,'best_config':bins,'number_bins':conf}


def objective_SA(arg):
    items,_,c,_ = instance_v2(FILE)
    alpha , T_initial , T_cible , nb_it = arg
    _ , solution, _ = heuristic_FFD(items, c)
    nbin, conf,exec_time = recuit_simule(items, c, solution ,alpha , T_initial , T_cible , nb_it  )
    print(arg,nbin)
    return 2 * nbin + exec_time
   

def objective_TS(arg):
    items,_,c,_ = instance_v2(FILE)
    max_com , mx_iter  , no_chng = arg
    _, solution, _ = heuristic_FFD(items, c)
    nbin, conf, exec_time = TS( c,items, max_com , mx_iter  , no_chng)
    print(arg,nbin)
    return exec_time + nbin * 10
    #return exec_time + (nbin*2)
    #0.95 , 1000 , 0.1 , 50 

def line_prepender(filename,line):
        with open(filename,'r+') as f:
                trash = f.readline()
                content = f.read()
                f.seek(0,0)
                f.write(line.rstrip('\r\n')+'\n' +content)


def get_params_hyper_AG(filename):
        global FILE 
        FILE = filename
        trials = Trials()
        best_AG = fmin(objective_hyper_AG, space_hyper_AG, algo=tpe.suggest, max_evals=2, trials=trials)
        print(best_AG)
        return best_AG
        
def get_params_SA(filename):
        global FILE 
        FILE = filename
        trials = Trials()
        best_SA = fmin(objective_SA, space_SA, algo=tpe.suggest, max_evals=3, trials=trials)
        print(best_SA)
        return best_SA

def get_params_TS(filename):
        global FILE 
        FILE = filename
        trials = Trials()
        best_TS = fmin(objective_TS, space_TS, algo=tpe.suggest, max_evals=8, trials=trials)
        print(best_TS)
        return best_TS

space_hyper_AG =  [
        hp.choice('POPULATION_SIZE', np.arange(45,55,2)),
        hp.choice('MAX_GENERATIONS', np.arange(50, 300, 10)),
        hp.choice('MAX_NO_CHANGE',  np.arange(20, 150, 10)),
        hp.choice('TOURNAMENT_SIZE', np.arange(6, 30, 2)),
        hp.uniform('MUTATION_RATE', 0.1, 1),
        hp.uniform('CROSSOVER_RATE', 0.1, 1)
         ]

space_SA = [
        hp.uniform('ALPHA', 0.85, 0.95),
        hp.choice('TEMPERATURE', np.arange(100,140,10)),
        hp.choice('T_CIBLE', np.arange(0.5,1,0.1)),
        hp.choice('ITERATIONS', np.arange(35,45,1))
]

space_TS = [
        hp.choice('MAX_COMBINATION_LENGTH', np.arange(1000,10000,100)),
        hp.choice('MAX_ITERATIONS', np.arange(1000,10000,100)),
        hp.choice('MAX_NO_CHANGE', np.arange(10,200,10))
]



#for f in files:
        

# FILE = 'N1C3W1_A.txt'

# best_AG = get_params_AG()
# best_SA = get_params_SA()

# params = []
# for v in best_AG.values(): params.append(str(v))
# for v in best_SA.values(): params.append(str(v))

# line = ' '.join(params)
# line_prepender(filename, line)







