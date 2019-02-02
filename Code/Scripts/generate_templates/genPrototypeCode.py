import os

sessions = ['13:830:1320',
            '14:830:1500',
            '15:945:1545',
            '16:830:1430',]
'''
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
            '11:830:1615',
            '12:800:1430']
'''

out_dir = f'{os.environ["ATS_DATA"]}/Queue/Queue-2-s3-2-ELD/'
out_dir = 'output/'
print(f'dir={out_dir}')

template1_file = "Day_1TF_template_v2.txt"
output1_prefix = "DayV2_1TF_"
template2_file = "Day_2TF_template_v2.txt"
output2_prefix = "DayV2_2TF_"

#template1_file = "Swing_1TF_template_v1.txt"
#output1_prefix = "SwingV1_1TF_"
#template2_file = "Swing_2TF_template_v1.txt"
#output2_prefix = "SwingV1_2TF_"

for tf in [15,20,25,30,45,60,90,120,240,360,1440]:
  for s in sessions:
    num,start,end = s.split(':')
    os.system("sed \'s/\<BARSIZE\>/"+str(tf)+"/;s/\<START\>/"+start+"/;s/\<END\>/"+end+"/;\' "+template1_file+" > "+out_dir+output1_prefix+str(tf)+"m_sess"+num+".txt")
    os.system("sed \'s/\<BARSIZE\>/"+str(tf)+"/;s/\<START\>/"+start+"/;s/\<END\>/"+end+"/;\' "+template2_file+" > "+out_dir+output2_prefix+str(tf)+"m_sess"+num+".txt")

