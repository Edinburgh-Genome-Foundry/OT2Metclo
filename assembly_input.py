'''Input your assembly plan in an excel format, checks file. It makes a plan for the OT2 labware set-up specifically for this assembly 
and provides it to the user. The user then can populate the OT2 labware with the appropriate solutions. The OT2 labware plan is then provided 
to the the OT2 protocol. 
INPUT: excel document with insert and assembly vector 
(1) size of each plasmid
(2) miniprep ug/ul contration of each plasmid 
(3) final assembly size
PROCESS:
(1) check file 
(2) retraive data from file
(3) calculate valumes needed for the assembly from the data
(4) make a labware plan allocating position and quantity of the solutions for user and OT2 protocol
'''
import pandas as pd
import numpy as np
from scipy.constants import Avogadro 

#Input excel file
xl_file = (pd.read_excel(r'/home/dany/data/software/metclo_gh/metclo/testAssinput.xlsx', header = None)).to_numpy()
line_len= len(xl_file)

plasmid_vol = [0]*(line_len-1)

def __calcpv__ (plasmid_size, ugul):
    num_copies_fmolul = round((ugul*Avogadro/(plasmid_size*10**15*650)),3)
    plasmid_volume = 15/num_copies_fmolul
    return plasmid_volume

#calculates the master mix volume for a single plasmid
def __calcmm__(plasmid_volume, assembly_size):
    if assembly_size <= 30000:
        bsai = 0.5
    else:
        bsai = 1
    ligase_buffer = 2
    DNA_ligase = 0.5
    water = 20-plasmid_volume - bsai - ligase_buffer - DNA_ligase
    arr = [plasmid_volume, bsai, ligase_buffer, DNA_ligase, water]
    return arr*1.25


for i in range (len(xl_file)-1):
    plasmid_volume = __calcpv__(xl_file[i][1], int(xl_file[i][2]))
    print(type(plasmid_volume))
    plasmid_mm = __calcmm__(plasmid_volume, xl_file[-1][1])
    #print(plasmid_vol + ' ' + plasmid_mm)
    #assembly_vol[i] = plasmid_mm
    #sum_assembly_vol = np.add(sum_assembly_vol, assembly_vol[i][1:])  


#Output Lawbare setup plan and OT2 input Excel format 