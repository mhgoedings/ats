import os

sessions = ['1:800:1300',
            '2:810:1300',
            '3:825:1325',
            '4:830:1515',
            '5:830:1315',
            '6:830:1305',
            '7:900:1430',
            '8:930:1600',
            '9:930:1615',
            '10:820:1330',
            '11:830:1615']

for tf in [15,20,30,60,90,120,240]:
  for s in sessions:
    num,start,end = s.split(':')
    os.system("sed \'s/\<BARSIZE\>/"+str(tf)+"/;s/\<START\>/"+start+"/;s/\<END\>/"+end+"/;\' BOS_2TF_template_v1.txt > output/DP_2TF_"+str(tf)+"m_sess"+num+".txt")
    os.system("sed \'s/\<BARSIZE\>/"+str(tf)+"/;s/\<START\>/"+start+"/;s/\<END\>/"+end+"/;\' BOS_1TF_template_v1.txt > output/DP_1TF_"+str(tf)+"m_sess"+num+".txt")

