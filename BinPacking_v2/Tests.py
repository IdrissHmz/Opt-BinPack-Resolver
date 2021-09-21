from Heuristics import *
from GeneticAlgorithm import AG
from SimulatedAnnealing import recuit_simule
from BranchBound import branchAndBound
from TabuSearch import TS
from imports import instance,instance_v2,FILES
from Hyperize import get_params_TS,get_params_AG,get_params_SA, line_prepender

import pickle


FILES = [
                # # 'instances/Facile/T_Tres_Petite_50/N1C1W1_A.txt',
                # # 'instances/Facile/T_Tres_Petite_50/N1C3W1_A.txt',
                # # 'instances/Facile/T_Petite_100/N2C1W1_A.txt',
                # # 'instances/Facile/T_Petite_100/N2C3W1_A.txt',

                # # 'instances/Facile/T_Moyenne_200/N3C1W1_A.txt',
                # # 'instances/Facile/T_Moyenne_200/N3C3W1_A.txt',

                # # 'instances/Facile/T_Grande_500/N4C1W1_A.txt',
                # # 'instances/Facile/T_Grande_500/N4C3W1_A.txt',

                # 'instances/Facile/T_Tres_Grande_1000/Falkenauer_u1000_00.txt',
                # 'instances/Facile/T_Tres_Grande_1000/Falkenauer_u1000_19.txt',


                # # 'instances/Moyenne/T_Tres_Petite_50/N1W4B1R0.txt',
                # # 'instances/Moyenne/T_Petite_100/N2W1B1R0.txt',
                # # 'instances/Moyenne/T_Petite_100/N2W4B1R0.txt',

                # # 'instances/Moyenne/T_Moyenne_200/N3W1B1R0.txt',
                # # 'instances/Moyenne/T_Moyenne_200/N3W4B1R0.txt',

                # # 'instances/Moyenne/T_Grande_500/N4W1B1R0.txt',
                # # 'instances/Moyenne/T_Grande_500/N4W4B1R0.txt',


                # # 'instances/Difficile/T_Moyenne_200/HARD0.txt',
                # # 'instances/Difficile/T_Moyenne_200/HARD1.txt',
                # # 'instances/Difficile/T_Moyenne_200/HARD2.txt',

              # #  'instances/Moyenne/T_Tres_Petite_50/N1W4B3R9.txt',
              # #  'instances/Moyenne/T_Petite_100/N2W4B3R0.txt',
              # #  'instances/Moyenne/T_Grande_500/N4W4B3R9.txt',
              # #  'instances/Facile/T_Tres_Petite_50/N1C1W1_R.txt',
              # #  'instances/Facile/T_Petite_100/N2C1W2_Q.txt',
              # #  'instances/Facile/T_Grande_500/N4C1W2_H.txt',
        ]


def test_all_instances():

  tests = load_tests()
  print(tests)
  if len(tests)==0 : tests = {}

  for f in FILES:
    print()
    print()
    print(f)
    items,meta,c,n  = instance_v2(f)
    ffd = heuristic_FFD(items, c)
    dico = {}

    print('\tFIRST FIT DEC           : ', ffd[0], ffd[2])
    ffd_dict = {'BINS':ffd[0],'TIME':ffd[2]}
    dico['FIRST FIT DEC']=ffd_dict

    ffi = heuristic_FFI(items, c)
    print('\tFIRST FIT INC           : ', ffi[0], ffi[2])
    ffi_dict = {'BINS':ffi[0],'TIME':ffi[2]}
    dico['FIRST FIT INC'] = ffi_dict

    bf = heuristic_BF(items, c)
    print('\tBEST FIT ALGORITHM      : ', bf[0], bf[2])
    bf_dict = {'BINS':bf[0],'TIME':bf[2]}
    dico['BEST FIT'] = bf_dict

    nf = heuristic_NF(items, c)
    print('\tNEXT FIT ALGORITHM      : ', nf[0], nf[2])
    nf_dict = {'BINS':nf[0],'TIME':nf[2]}
    dico['NEXT FIT'] = nf_dict

    wf = heuristic_WF(items, c)
    print('\tWORST FIT ALGORITHM     : ', wf[0], wf[2])
    wf_dict = {'BINS':wf[0],'TIME':wf[2]}
    dico['WORST FIT'] = wf_dict


    param_SA = get_params_SA(f)
    rs = recuit_simule(items, c, ffd[1], param_SA['ALPHA'] , param_SA['TEMPERATURE'] , param_SA['T_CIBLE'],param_SA['ITERATIONS'])
    print('\tSIMEULATED ANNEALING    : ', rs[0], rs[2])
    rs_dict = {'BINS':rs[0],'TIME':rs[2]}
    dico['SIMULATED ANNEALING'] = rs_dict


    param_TS = get_params_TS(f)
    ts = TS(c, items,param_TS['MAX_COMBINATION_LENGTH'],param_TS['MAX_ITERATIONS'],param_TS['MAX_NO_CHANGE'])
    print('\tTABU SEARCH             : ', ts[0], ts[2])
    ts_dict = {'BINS':ts[0],'TIME':ts[2]}
    dico['TABU SEARCH']=ts_dict


    param_AG = get_params_AG(f)
    ag = AG(items, c,param_AG['POPULATION_SIZE'],param_AG['MAX_GENERATIONS'],param_AG['MAX_NO_CHANGE'],param_AG['TOURNAMENT_SIZE'],param_AG['MUTATION_RATE'],param_AG['CROSSOVER_RATE'])
    print('\tGENETIC ALGORITHM       : ', ag[0], ag[2])
    ag_dict = {'BINS':ag[0],'TIME':ag[2]}
    dico['GENETIC ALGO'] = ag_dict




    params = []
    for v in param_TS.values(): params.append(str(v))
    for v in param_SA.values(): params.append(str(v))
    for v in param_AG.values(): params.append(str(v))

    line = ' '.join(params)
    line_prepender(f, line)


    tests[f] = dico

  test_file = open("test.txt","wb")
  json_test = pickle.dump(tests,test_file)
  test_file.close()
    # bb = branchAndBound(w, c)


def load_tests():
  f = open("test.txt","rb")
  dico = pickle.load(f)
  f.close()
  for f,t in dico.items():
    f = f.split('/')[-1]
    print(f)
    for a,alg in t.items():
      print("\t" + a)
      print("\t\t ecxecution time : " + str(alg['TIME']))
      print("\t\t number of bins  : " + str(alg['BINS']))
      print()
    print('*************************************************************')
  return dico


d = load_tests()
new_file = open('tavu.txt','w')
for key,file in d.items():
  f = key.split('/')[-1]
  print(f)
  print('Recherche taboue : ',file['TABU SEARCH'])
  new_file.write(f + ' : ' + str(file['TABU SEARCH']) + '\n')
  print()
    
print(d['instances/Facile/T_Tres_Petite_50/N1C1W1_A.txt']['FIRST FIT DEC'])
#test_all_instances()
