#cand_DP_38_T1_30_T2_1440_mkt_6.txt    cand_DP_51_T1_90_T2_1440_mkt_1.txt    strat_53_70.txt

import os
import re

path = '/Users/szagar/ZTS/Dropbox/Business/ats/Data/StrategyArchive'
regex = re.compile(r"_T.*mkt_")
for f in os.listdir(path):
  if f.startswith('cand_'):
    f2 = f.replace('cand_','strat_').replace(' ','_').replace('_DP_','_')
    f2 = regex.sub('_',f2)

    f = path+"/"+f
    f2 = path+"/"+f2

    print(f'{f2} <- {f}')
    os.rename(f,f2)

#[os.rename(f, f.replace('_', '-')) for f in os.listdir('.') if not f.startswith('.')]
#[os.rename(f, f.replace('cand', 'strat').replace('DP_','')) for f in os.listdir('.') if not f.startswith('.')]
