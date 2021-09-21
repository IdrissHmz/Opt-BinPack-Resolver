from imports import *
from Heuristics import heuristic_FFD


def eval(conf):
  return max(conf)+1
  #if (nbin == -1): config impossible

def eval_choix(conf,items,c):
  bin = set(conf)
  bin_space = []
  for b in bin:
    indices = [index for index, element in enumerate(conf) if element == b]
    s = sum([items[i] for i in indices])
    bin_space.append(c-s)
  return max(bin_space) 

def choix(voisins,items,c):
  if len(voisins)>0:
    evals = [eval_choix(v,items,c) for v in voisins]
    choix = evals.index(max(evals))
    return voisins[choix],voisins
  return -1

def verif(conf,items,c):
  # if -1 in conf : return 0
  # else: 
  en = enumerate(conf)
  bin = set(conf)
  for b in bin:
    indices = [index for index, element in enumerate(conf) if element == b]
    s = sum([items[i] for i in indices])
    if s > c: return 0

  #verifier que les numero des bins sont bien séquentiel partant de 0
  mx = max(conf)
  lis = [i for i in range(mx)] 
  for i in lis:
    if (i not in list(set(conf))): 
      return 0
  return 1 

def bon_voisins(conf,ind,max_bin,taboue,L,items,c):
  V = []
  for i in range(max_bin):
    if i!=conf[ind]:
      v = conf.copy()
      v[ind]=i
      if verif(v,items,c) and ((v not in taboue) or len(taboue)== L or eval(v) < max_bin):
        if len(taboue)== 10: taboue.pop()
        return [v]
        V.append(v)
  return V        
#bon_voisins(soluce,2,5,[])

def RT(items,c,m,soluce,k_arret,L):
  #m,soluce = heuristic_FFD(c,items)
  x = soluce; fx = eval_choix(x,items,c)
  optimum = soluce
  o = m
  k=0
  Tabou = []
  while True and k != k_arret:
    j = random.randint(0,n-1)
    bv = choix(bon_voisins(x,j,m,Tabou,L,items,c),items,c)
    if bv == -1 :
        k+=1
        continue
    best, vois = bv
    v= best;fv = eval_choix(v,items,c)
    x = v
    Tabou.append(x)
    if eval(x) < o:
      optimum = x
      # print(optimum)
      o = eval(x)
    k+=1   
  return o,optimum



def test_RT(x):
  #m,soluce = heuristic_FFD(c,items)
  k_arret = x['k_arret']
  L = x['L']
  o,opt = RT(k_arret,L)
  return o
  

# meta,items = instance('N1C1W1_A.txt')
# m,soluce = heuristic_FFD(items,int(meta[0]))


# k_arret = 100
# L=100

# print(RT(m,soluce,k_arret,L,items))