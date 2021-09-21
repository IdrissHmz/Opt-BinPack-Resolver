from Heuristics import heuristic_FFD
from imports import *
from TB_me import verif,eval,choix


def voisins(conf,ind,max_bin,items,c):
  V = []
  for i in range(max_bin):
    if i!=conf[ind]:
      v = conf.copy()
      v[ind]=i
      if verif(v,items,c):
        V.append(v)
  return V    


def eval_choix(conf,items):
  bin = set(conf)
  bin_space = []
  for b in bin:
    indices = [index for index, element in enumerate(conf) if element == b]
    s = sum([items[i] for i in indices])
    bin_space.append(c-s)
  return max(bin_space) 


def RS(items,c,alpha,t,it_palier,k_arret):
  m,soluce = heuristic_FFD(items,c)
  x = soluce; fx = eval_choix(x,items)
  optimum = soluce
  o = m
  k=0
  while True:
    for i in range(it_palier):
      j = random.randint(0,n-1)
      bv = choix(voisins(x,j,m,items,c),items,c)
      if bv == -1 : continue
      best , vois = bv
      #v= best;fv = eval_choix(v)
      v = random.choice(vois); fv = eval_choix(v,items)
      if eval(v) < eval(x) : 
        optimum = v
        o = eval(v)
        fv *= 10
        #k=k_arret-1
        #break
      delta = fv - fx
      if delta > 0:
        x = v
        if eval(x) < o:
          optimum = x
          o = eval(x)
      else:
        u=random.random()  
        if u < math.exp(delta / t):
          x = v
      t = alpha * t 
      if t == 0: 
        t=100
        break    
    k+=1   
    if k == k_arret :break
  return o,optimum

# m,soluce = heuristic_FFD(c,items)
# alpha = 0.94
# t = 100
# it_palier = 100
# k_arret = 100

# solution = RS(alpha,t,it_palier,k_arret)