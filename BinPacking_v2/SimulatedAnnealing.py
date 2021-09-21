from imports import *
from Heuristics import heuristic_FFD

def eval_RS (items,c,config ) :
    nb_bins = max(config)+1 
    weights = [0 for i in range(nb_bins)]
    eval = 0 
    for i in range(len(config)):
        weights[config[i]] += items[i] 
    for j in range (len(weights)) :
        eval += math.pow(  weights[j]  , 2 ) 
    return eval 
    

def get_voisin (items,c,config , T_moy , T): 
    if  T <  T_moy:
        voisin  = mouv_basseT (items,c,config )  
    else :
        voisin  = mouv_hauteT (items,c,config )
    return voisin

def verified_solution(items,c,config) : 
    nb_bins = max(config)+1 
    weights = [0 for i in range(nb_bins)]
    verified = True 
    k= 0  
    while(  k < len(config)) :
        weights[config[k]] += items[k] 
        if (weights[config[k]]> c):
            verified = False 
            break 
        k += 1   
    return verified 


def mouv_hauteT (items,c,config) : 
    result = config[::] 
    while ( True  ) : 
        #print('whhile haute')
        result = config[::]
        i = random.randint(0,len(config)-1) 
        j = random.randint(0,len(config)-1) 
        result[i], result[j] = result[j], result[i]
        if(result == config) : continue 
        if (verified_solution(items,c,result) ) : break  
    return result 

def mouv_basseT (items,c,config) : 
    result = config[::] 
    Set =  set(config) 
    list_bins  = list(Set)
    minuteur = 0
    while ( True  ) : 
        #print('whhile basse')
        result = config[::]
        i = random.randint(0,len(config)-1) 
        result[i] = random.choice(list_bins)
        if(result == config) : continue 
        if (verified_solution(items,c,result) ) : break 
        if minuteur == 8 : 
            #print('/////////////////////////////////////////////////////')
            result = config; continue 
        minuteur += 1
    return result 


def recuit_simule(items,c,sol , alpha , T_initial , T_cible , nb_it) : 
    start_time = time.time()
    x = sol[::]
    T = T_initial 
    fx = eval_RS(items,c,sol )
    y= 0
    fy = 0 
    delta =0 
    u =0  
    expo = 0 
    T_moy =  ( T_cible + T_initial ) / 2 
    best = sol[::]
    while ( T > T_cible) : 
        for i in range(math.ceil(nb_it)+1) :
           # print('                  '+ str(i))
            y = get_voisin (items,c, x , T_moy , T) 
            if( y == x ) : continue  
            fy = eval_RS(items,c,y) 
            delta = fy - fx 
            if (  delta > 0 ) : 
                x = y[::] 
                fx = fy  
            else : 
                u = random.random() 
                expo  = math.exp(( delta)/T) 
                if(u < expo ) : 
                        x= y[::]
                        fx = fy 
            if (eval_RS(items,c,best)< eval_RS(items,c,x) )  :  best = x[::]
        #print(str(T) +' '+ str(T_cible) +' '+ str(alpha) +' '+ str(nb_it))    
        T = T *alpha 
    nb_bins_RS = len ( set(best) ) 
    nb_bins_FDD = len ( set(sol)  )  
    exec_time = (time.time() - start_time)
    
    # return {  "nombre des bins RS" : nb_bins_RS ,best,"evaluation RS " : eval_RS(best) ,
    #           "evaluation FDD " : eval_RS(sol) , "nombre des bins FDD" : nb_bins_FDD , "execution time " : " %s seconds" % exec_time  } 
    return nb_bins_RS,best,exec_time

