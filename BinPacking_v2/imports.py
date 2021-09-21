import random
import math
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt


# items = [4,7,8,5,6,5,2,3,8,5,4,6,9,1,1,2,3,3,6,5]
# n=len(items)
# c = 10

FILES = [
                # 'instances/Facile/T_Tres_Petite_50/N1C1W1_A.txt',
                # 'instances/Facile/T_Tres_Petite_50/N1C3W1_A.txt',
                # 'instances/Facile/T_Petite_100/N2C1W1_A.txt',
                # 'instances/Facile/T_Petite_100/N2C3W1_A.txt',
                # 'instances/Facile/T_Moyenne_200/N3C1W1_A.txt',
                # 'instances/Facile/T_Moyenne_200/N3C3W1_A.txt',
                # 'instances/Facile/T_Grande_500/N4C1W1_A.txt',
                # 'instances/Facile/T_Grande_500/N4C3W1_A.txt',
                # 'instances/Facile/T_Tres_Grande_1000/Falkenauer_u1000_00.txt',
                # 'instances/Facile/T_Tres_Grande_1000/Falkenauer_u1000_19.txt',
                # 'instances/Moyenne/T_Tres_Petite_50/N1W1B1R0.txt',
                # 'instances/Moyenne/T_Tres_Petite_50/N1W4B1R0.txt',
                # 'instances/Moyenne/T_Petite_100/N2W1B1R0.txt',
                # 'instances/Moyenne/T_Petite_100/N2W4B1R0.txt',
                # 'instances/Moyenne/T_Moyenne_200/N3W1B1R0.txt',
                # 'instances/Moyenne/T_Moyenne_200/N3W4B1R0.txt',
                # 'instances/Moyenne/T_Grande_500/N4W1B1R0.txt',
                # 'instances/Moyenne/T_Grande_500/N4W4B1R0.txt',
                # 'instances/Difficile/T_Moyenne_200/HARD0.txt',
                # 'instances/Difficile/T_Moyenne_200/HARD1.txt',
                # 'instances/Difficile/T_Moyenne_200/HARD2.txt',
               'instances/Moyenne/T_Tres_Petite_50/N1W4B3R9.txt',
               'instances/Moyenne/T_Petite_100/N2W4B3R0.txt',
               'instances/Moyenne/T_Grande_500/N4W4B3R9.txt',
               'instances/Facile/T_Tres_Petite_50/N1C1W1_R.txt',
               'instances/Facile/T_Petite_100/N2C1W2_Q.txt',
               'instances/Facile/T_Grande_500/N4C1W2_H.txt',



        ]



  
# def instance_v1(inst):
#   lis = [int(line.strip()) for line in open(inst, 'r')]
#   return lis[2:],[],lis[1],lis[0]


def instance(inst):
  fic = open(inst, 'r')
  param = fic.readline().split()
  param = [float(m) for m in param]

  if len(param) == 13:
    param_dict ={}
    param_dict['MAX_COMBINATION_LENGTH'] = param[0]
    param_dict['MAX_ITERATIONS'] = param[1]
    param_dict['MAX_NO_CHANGE_TS'] = param[2]
    param_dict['ALPHA'] = param[3]
    param_dict['TEMPERATURE'] = param[4]
    param_dict['T_CIBLE'] = param[5]
    param_dict['ITERATIONS'] = param[6]
    param_dict['POPULATION_SIZE'] = param[7]
    param_dict['MAX_GENERATIONS'] = param[8]
    param_dict['MAX_NO_CHANGE_AG'] = param[9]
    param_dict['TOURNAMENT_SIZE'] = param[10]
    param_dict['MUTATION_RATE'] = param[11]
    param_dict['CROSSOVER_RATE'] = param[12]
  else: param_dict = param  
  N = int(fic.readline())
  C = int(fic.readline())
  items = [int(line.strip()) for line in fic.readlines()]
  return  items, param_dict, C, N

def instance_v2(inst):
  fic = open(inst, 'r+')
  param = fic.readline().split()
  if len(param) == 2 :
    fic.close()
    return instance(inst)
  if len(param) == 1:
    content = fic.read()
    fic.seek(0,0)
    fic.write('0 0' + '\n' + param[0] + '\n' + content)
    fic.close()
    return instance(inst)
  else:
    fic.close()
    return instance(inst)    

#print(instance_v2('instances/Moyenne/T_Petite_100/N2W1B1R0.txt'))    