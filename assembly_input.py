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
import math

#Input Excel file
while True:
    try:
        xfile = input(r'Input the pathway to the excel file: ')
        xl_file = pd.ExcelFile('xfile') 
    except:
        print('Excel file needed, try again.')
    else:
        break

#get number of inserts, and their data

#get vector and its data

#get assembly size 
#assembly_size = excel cel number XXXX

#make array [vector name, size, concetration], [Insert1 name, size, conc.]...]
    #array called assembly



plasmidvol_array = [0]*numberofinsertplasmids+1

def __calcpv__ (plasmid_size, ugul):
    num_copies_fmolul = ugul*math.avogadro/(plasmid_size*10**15*650)
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


assembly_vol = [0]*(insert_count+1)
sum_assembly_vol = [0]*4

for i in length(assembly):
    plasmid_volume = __calcpv__(assembly[i][1], assembly[i][1])
    plasmid_mm = __calcmm_(plasmid_volume, assembly_size)
    assembly_vol[i] = plasmid_mm
    sum_assembly_vol = np.add(sum_assembly_vol, assembly_vol[i][1:])  


#Output Lawbare setup plan and OT2 input Excel format 









