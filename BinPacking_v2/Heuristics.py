from imports import *
from imports import FILES
import random

def heuristic_FFD(w,c):
  t1 = time.time()
  n = len(w)
  order = sorted([i for i in range(n)], key = lambda i:w[i],reverse=True)
  bin_for_item = [-1 for i in range(n)]
  bin_space = []
  for i in order:
    for j in range(len(bin_space)):
      if w[i]<bin_space[j]:
        bin_for_item[i]=j
        bin_space[j]-=w[i]
        break
    if bin_for_item[i] < 0:
      j = len(bin_space)
      bin_for_item[i] = j
      bin_space.append(c-w[i])
  n_bin = len(bin_space)
  t2 = time.time()
  return n_bin, bin_for_item, t2-t1






def heuristic_FFI(w,c):
  t1 = time.time()
  n = len(w)
  #print(w,n)
  order = sorted([i for i in range(n)],key = lambda i:w[i])
  #print(order)
  bin_for_item = [-1 for i in range(n)]
  bin_space = []
  for i in order:
    for j in range(len(bin_space)):
      if w[i]<bin_space[j]:
        bin_for_item[i]=j
        #print(bin_for_item)
        bin_space[j]-=w[i]
        break
    if bin_for_item[i] < 0:
      j = len(bin_space)
      bin_for_item[i] = j
      #print(bin_for_item)
      bin_space.append(c-w[i])
  n_bin = len(bin_space)
  t2 = time.time()
  return n_bin, bin_for_item, t2-t1

#print(heuristic_FFI([50,40,45,36,32,15,30,29,23,20,16,12,9,8,5,1],50))

def heuristic_BF(w,c):
  t1 = time.time()
  n = len(w)
  bin_for_item = [-1 for i in range(n)]
  bin_space = []
  for i,wi in enumerate(w):
    tmp = sorted(bin_space)
    k=0
    while len(tmp)!=0:
      #k = bin_space.index(min(bin_space))
      if wi < tmp[k]:
        j = bin_space.index(tmp[k])
        bin_for_item[i]=j
        bin_space[j]-=wi
        break
      else:
        k+=1
        if (k == len(bin_space)): break
      
    if bin_for_item[i] < 0:
      j = len(bin_space)
      bin_for_item[i] = j
      bin_space.append(c-wi)
  n_bin = len(bin_space)
  t2 = time.time()
  return n_bin, bin_for_item, t2-t1

#print(heuristic_BF(c,items))

def heuristic_WF(w,c):
  t1 = time.time()
  n = len(w)
  bin_for_item = [-1 for i in range(n)]
  bin_space = []
  for i,wi in enumerate(w):
    if (bin_space != []):
      k = bin_space.index(max(bin_space))
      if wi < bin_space[k]:
        bin_for_item[i]=k
        bin_space[k]-=wi
      
    if bin_for_item[i] < 0:
      j = len(bin_space)
      bin_for_item[i] = j
      bin_space.append(c-wi)
  n_bin = len(bin_space)
  t2 = time.time()
  return n_bin, bin_for_item, t2-t1

#print(heuristic_WF(c,items))   

def heuristic_AWF(w,c):
  t1 = time.time()
  n = len(w)
  bin_for_item = [-1 for i in range(n)]
  bin_space = []
  for i,wi in enumerate(w):
    tmp = bin_space
    if (len(tmp)!=0):
      k = tmp.index(max(tmp)); tmp[k] = 0; k = tmp.index(max(tmp))
      if w[i]<bin_space[k]:
        bin_for_item[i]=k
        bin_space[k]-=wi
      
    if bin_for_item[i] < 0:
      j = len(bin_space)
      bin_for_item[i] = j
      bin_space.append(c-wi)
  n_bin = len(bin_space)
  t2 = time.time()
  return n_bin, bin_for_item, t2-t1

#print(heuristic_AWF(c,items)) 

def heuristic_NF(w,c):
  random.shuffle(w)
  t1 = time.time()
  n = len(w)
  bin_for_item = [-1 for i in range(n)]
  bin_space = []
  for i,wi in enumerate(w):
    for j in range(len(bin_space),0,-1):
      if wi<bin_space[j-1]:
        bin_for_item[i]=j-1
        bin_space[j-1]-=wi
        break
    if bin_for_item[i] < 0:
      j = len(bin_space)
      bin_for_item[i] = j
      bin_space.append(c-wi)
  n_bin = len(bin_space)
  t2 = time.time()
  return n_bin, bin_for_item, t2-t1

#print(heuristic_NF(c,items))  

def test_all_heuris():
  for f in FILES:
    print()
    print()
    print(f)
    items, meta, c, n = instance_v2(f)
    ffd = heuristic_FFD(items, c)
    ffi = heuristic_FFI(items, c)
    bf = heuristic_BF(items, c)
    nf = heuristic_NF(items, c)
    wf = heuristic_WF(items, c)
    print('\tFIRST FIT DEC  : ', ffd[0], ffd[2])
    print('\tFIRST FIT INC  : ', ffi[0], ffi[2])
    print('\tBEST FIT       : ', bf[0], bf[2])
    print('\tNEXT FIT       : ', nf[0], nf[2])
    print('\tWORST FIT      : ', wf[0], wf[2])

test_all_heuris()