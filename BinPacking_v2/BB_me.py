from Heuristics import heuristic_FFD
from TabuSearch import verif,eval

def Branch_Bound(items):
  n=len(items)
  Confs=[]
  Confs.append([-1]*n)
  m, soluce = heuristic_FFD(c,items)
  opt= soluce
  j=0
  while len(Confs)>0 :
    #print(Confs)
    v = Confs.pop(0)
    ev = eval(v)
    if (ev < m):
      j = v.index(-1)
      for i in range(n,-1,-1):
        v = v.copy()
        if (j<n): v[j]=i 
        if -1 in v:
            Confs.insert(0,v)
        else:
          if (verif(v)==1):
            if eval(v) <= m:
              m = eval(v)
              opt = v
              print('Solution trouvé',m,v)
      j+=1  
  return m,opt

#print('Solution optimal: ',m,opt)
items = [4,7,8,5,6,5,2,3,8,5,4,6,9,1,1,2,3,3,6,5]
n=len(items)
c = 10
#Branch_Bound(items)