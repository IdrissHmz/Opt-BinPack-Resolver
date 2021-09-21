import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from Tests import load_tests
mpl.rcParams['toolbar'] = 'None' 

soluce = {
            'N1C1W1_A.txt':25,
            'N1C3W1_A.txt':16,
            'N2C1W1_A.txt':48,
            'N2C3W1_A.txt':35,
            'N3C1W1_A.txt':105,
            'N3C3W1_A.txt':66,
            'N4C1W1_A.txt':240,
            'N4C3W1_A.txt':164,

            'N1W4B1R0.txt':6,
            'N2W1B1R0.txt':34,
            'N2W4B1R0.txt':12,

            'N3W1B1R0.txt':67,
            'N3W4B1R0.txt':23,
            'N4W1B1R0.txt':167,
            'N4W4B1R0.txt':56,

            'HARD0.txt':56,
            'HARD1.txt':57,
            'HARD2.txt':56,


            'N1W4B3R9.txt':6,
            'N2W4B3R0.txt':12,
            'N4W4B3R9.txt':55,#solution exacte manquante
            'N1C1W1_R.txt':25,
            'N2C1W2_Q.txt':65,
            'N4C1W2_H.txt':315,
        }



skip =  ['N1W4B1R0.txt','N2W4B1R0.txt','N4W4B1R0.txt','N1C1W1_A.txt','N2C1W1_A.txt','N4C1W1_A.txt']

test = load_tests()

file_paths = test.keys()
labels = [st.split('/')[-1].split('.')[0] for st in file_paths if st.split('/')[-1] not in skip]

ffd_time= []; ffd_bins = []
ffi_time= []; ffi_bins = []
bf_time = []; bf_bins = []
nf_time = []; nf_bins = []
wf_time = []; wf_bins = []
rs_time = []; rs_bins = [] 
ts_time = []; ts_bins = [] 
ag_time = []; ag_bins = [] 
exact = [] 
for k,fl in test.items() : 
   
    if k.split('/')[-1] in skip:
        #print(k)
        continue
    ffd_time.append(fl['FIRST FIT DEC']['TIME'] )
    ffd_bins.append(fl['FIRST FIT DEC']['BINS'] )
    ffi_time.append(fl['FIRST FIT INC']['TIME'])
    ffi_bins.append(fl['FIRST FIT INC']['BINS'] )
    bf_time.append(fl['BEST FIT']['TIME'] )
    bf_bins.append(fl['BEST FIT']['BINS'] )
    nf_time.append(fl['NEXT FIT']['TIME'] )
    nf_bins.append(fl['NEXT FIT']['BINS'] )
    wf_time.append(fl['WORST FIT']['TIME'] )
    wf_bins.append(fl['WORST FIT']['BINS'] )
    rs_time.append(fl['SIMULATED ANNEALING']['TIME'] )
    rs_bins.append(fl['SIMULATED ANNEALING']['BINS'] )
    ts_time.append(fl['TABU SEARCH']['TIME'] )
    ts_bins.append(fl['TABU SEARCH']['BINS'] )
    ag_time.append(fl['GENETIC ALGO']['TIME'] )
    ag_bins.append(fl['GENETIC ALGO']['BINS'] )
    exact.append(soluce[k.split('/')[-1]])


print(exact)


x = np.arange(0,3*len(labels),3)  # the label locations
width = 0.2  # the width of the bars



fig, ax = plt.subplots()
rects_ffd = ax.bar(x - width - 1/2, ffd_bins, width, label='FFD')
rects_ffi = ax.bar(x - width/2 - 1/4, ffi_bins, width, label='FFI')
rects_bf = ax.bar(x, bf_bins, width, label='BF')
rects_nf = ax.bar(x + width/2 + 1/4, nf_bins, width, label='NF')
rects_wf = ax.bar(x + width +1/2, wf_bins, width, label='WF')
# rects_rs = ax.bar(x + 3*width, rs_bins, width, label='RS')
# rects_ts = ax.bar(x + 7*width/2, ts_bins, width, label='TS')
# rects_ag = ax.bar(x + 4*width, ag_bins, width, label='AG')
rects_exact = ax.bar(x + 3*width/2 + 3/4, exact, width, label='EXACT')


ax.set_ylabel('bins')
ax.set_title('Number of bins')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.xticks(rotation=40)
# ax.bar_label(rects1, padding=3)
# ax.bar_label(rects2, padding=3)

fig.tight_layout()
#plt.show()

plt.savefig('captures/heuristic_bin_final.png')





fig, ax = plt.subplots()
rects_ffd = ax.bar(x - width - 1/2, ffd_time, width, label='FFD')
rects_ffi = ax.bar(x - width/2 - 1/4, ffi_time, width, label='FFI')
rects_bf = ax.bar(x , bf_time, width, label='BF')
rects_nf = ax.bar(x + width/2 + 1/4, nf_time, width, label='NF')
rects_wf = ax.bar(x + width + 1/2, wf_time, width, label='WF')
# rects_rs = ax.bar(x + 3*width, rs_time, width, label='RS')
# rects_ts = ax.bar(x + 7*width/2, ts_time, width, label='TS')
# rects_ag = ax.bar(x + 4*width, ag_time, width, label='AG')


ax.set_ylabel('execution time')
ax.set_title('Execution Time')
ax.set_xticks(x)
ax.set_xticklabels(labels)
plt.xticks(rotation=40)
ax.legend()
fig.tight_layout()
plt.savefig('captures/heuristic_bin_withoutExcedent.png')







x = np.arange(0,3*len(labels[:-1]),3)  
fig, ax = plt.subplots()
rects_ffd = ax.bar(x - width - 1/2, ffd_time[:-1], width, label='FFD')
rects_ffi = ax.bar(x - width/2 - 1/4, ffi_time[:-1], width, label='FFI')
#rects_bf = ax.bar(x , bf_time, width, label='BF')
rects_nf = ax.bar(x , nf_time[:-1], width, label='NF')
rects_wf = ax.bar(x + width/2 + 1/4, wf_time[:-1], width, label='WF')
# rects_rs = ax.bar(x + 3*width, rs_time, width, label='RS')
# rects_ts = ax.bar(x + 7*width/2, ts_time, width, label='TS')
# rects_ag = ax.bar(x + 4*width, ag_time, width, label='AG')


ax.set_ylabel('execution time')
ax.set_title('Execution Time')
ax.set_xticks(x)
ax.set_xticklabels(labels[:-1])
plt.xticks(rotation=40)
ax.legend()
fig.tight_layout()
plt.savefig('captures/heuristic_time_final.png')

x = np.arange(0,3*len(labels),3)  






width =0.35
fig, ax = plt.subplots()
# rects_ffd = ax.bar(x - width - 1/2, ffd_bins, width, label='FFD')
# rects_ffi = ax.bar(x - width/2 - 1/4, ffi_bins, width, label='FFI')
# rects_bf = ax.bar(x, bf_bins, width, label='BF')
# rects_nf = ax.bar(x + width/2 + 1/4, nf_bins, width, label='NF')
# rects_wf = ax.bar(x + width +1/2, wf_bins, width, label='WF')
rects_ts = ax.bar(x - width - 1/2, ts_bins, width, label='TS')
rects_rs = ax.bar(x - width/2 - 1/4, rs_bins, width, label='RS')
rects_ag = ax.bar(x , ag_bins, width, label='AG')
rects_exact = ax.bar(x + width/2 + 1/4, exact, width, label='EXACT')


ax.set_ylabel('bins')
ax.set_title('Number of bins')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.xticks(rotation=40)
fig.tight_layout()
plt.savefig('captures/meta_heuristic_bin_final.png')




fig, ax = plt.subplots()
# rects_ffd = ax.bar(x - width - 1/2, ffd_bins, width, label='FFD')
# rects_ffi = ax.bar(x - width/2 - 1/4, ffi_bins, width, label='FFI')
# rects_bf = ax.bar(x, bf_bins, width, label='BF')
# rects_nf = ax.bar(x + width/2 + 1/4, nf_bins, width, label='NF')
# rects_wf = ax.bar(x + width +1/2, wf_bins, width, label='WF')
rects_rs = ax.bar(x - width/2 - 1/4, rs_time, width, label='RS')
rects_ts = ax.bar(x, ts_time, width, label='TS')
rects_ag = ax.bar(x + width/2 + 1/4, ag_time, width, label='AG')


ax.set_ylabel('time')
ax.set_title('Execution Time')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.xticks(rotation=40)
fig.tight_layout()
plt.savefig('captures/meta_heuristic_time_final.png')









width =0.4
fig, ax = plt.subplots()
# rects_ffd = ax.bar(x - width - 1/2, ffd_bins, width, label='FFD')
# rects_ffi = ax.bar(x - width/2 - 1/4, ffi_bins, width, label='FFI')
# rects_bf = ax.bar(x, bf_bins, width, label='BF')
# rects_nf = ax.bar(x + width/2 + 1/4, nf_bins, width, label='NF')
# rects_wf = ax.bar(x + width +1/2, wf_bins, width, label='WF')
rects_ts = ax.bar(x - width/2 - 1/4, ts_bins,width, label='TS')
rects_exact = ax.bar(x , exact, width, label='EXACT')


ax.set_ylabel('bins')
ax.set_title('Number of bins')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

plt.xticks(rotation=40)

fig.tight_layout()
plt.savefig('captures/meta_heuristic_bin_TS_EX.png')







fig, ax = plt.subplots()
rects_rs = ax.bar(x - width/2 - 1/4, rs_time, width, label='RS')
rects_ts = ax.bar(x, ts_time, width, label='TS')
# rects_ag = ax.bar(x + width/2 + 1/4, ag_time, width, label='AG')


ax.set_ylabel('time')
ax.set_title('Execution Time')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.xticks(rotation=40)
fig.tight_layout()

plt.savefig('captures/meta_heuristic_bin_withoutExecedent_AG.png')





fig, ax = plt.subplots()
rects_rs = ax.bar(x, rs_time, 0.4, label='RS')
ax.set_ylabel('time')
ax.set_title('Execution Time')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.xticks(rotation=40)
fig.tight_layout()

plt.savefig('captures/meta_heuristic_bin_withoutExecedent_AG_RT.png')






rect_width = .2

x = np.arange(0,6*len(labels),6) 
width = 0.3
fig, ax = plt.subplots()
rects_ffi = ax.bar(x - 3*width/2 - 3/4, ffi_bins, rect_width, label='FFI')
rects_bf = ax.bar(x - width - 1/2, bf_bins,rect_width, label='BF')
rects_nf = ax.bar(x - width/2 - 1/4, nf_bins,rect_width, label='NF')
rects_ffd = ax.bar(x , ffd_bins, rect_width, label='FFD')
rects_wf = ax.bar(x + width/2 + 1/4, wf_bins,rect_width, label='WF')
rects_rs = ax.bar(x + width + 1/2, rs_bins,rect_width, label='RS')
rects_ts = ax.bar(x + 3*width/2 + 3/4, ts_bins, rect_width, label='TS')
rects_ag = ax.bar(x + 2*width + 1, ag_bins, rect_width, label='AG')
ax.set_ylabel('bins')
ax.set_title('Number of bins')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

plt.xticks(rotation=40)
fig.tight_layout()

plt.savefig('captures/all.png')




# fig, ax = plt.subplots()
# rects_ffi = ax.bar(x - 3*width/2 - 3/4, ffi_bins, width, label='FFI')
# rects_bf = ax.bar(x - width - 1/2, bf_bins, width, label='BF')
# rects_nf = ax.bar(x - width/2 - 1/4, nf_bins, width, label='NF')
# rects_ffd = ax.bar(x, ffd_bins, width, label='FFD')
# rects_wf = ax.bar(x + width/2 + 1/4, wf_bins, width, label='WF')
# rects_rs = ax.bar(x + width + 1/2, rs_time, width, label='RS')
# rects_ts = ax.bar(x + 3*width/2 + 3/4, ts_time, width, label='TS')
# rects_ag = ax.bar(x + 2*width + 1, ag_time, width, label='AG')


# ax.set_ylabel('time')
# ax.set_title('Execution Time')
# ax.set_xticks(x)
# ax.set_xticklabels(labels)
# ax.legend()

# plt.xticks(rotation=40)

# fig.tight_layout()
# plt.show()




