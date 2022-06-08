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

#the plasmids carry the insert/part [bp, concentration ng/ul]
part1 = np.array([13000, 78,0.0])
part2 = np.array([14000, 70,0.0])
part3 = np.array([18000, 50,0.0])
part4 = np.array([13000, 40,0.0])
part5 = np.array([14000, 60,0.0])
part6 = np.array([11000, 55,0.0])
partarr =np.array([part1, part2, part3, part4, part5, part6])

#the assembly vectors compiling the parts/inserts  [bp, concentration ng/ul]
assembly_v = [8000,66,0.0]

#Final Assembly size
assembly_size = 54200 




#the protocol says it need 30fmol of plasmid within the master mix. Method to calculate volume needed
def __calcpv__ (plasmid_size, ugul):
    num_copies_fmolul = round(ugul/plasmid_size * 1000000/650,3)
    print(num_copies_fmolul)
    plasmid_volume = 15/num_copies_fmolul
    print(type(plasmid_volume))
    return plasmid_volume
    

#calculates the master mix volume for a single plasmid
def __calcmm__(volumesum,assembly_size):
    ''' optional bsai volume difference depending on final assembly size
    if assembly_size <= 30000:
        bsai = 0.5
    else:
        bsai = 1
    '''
    bsai = 0.5
    ligase_buffer = 2
    DNA_ligase = 0.5
    water = 0
    if volumesum <=20:
        water = 20-plasmid_volume - bsai - ligase_buffer - DNA_ligase
    arr = [bsai, ligase_buffer, DNA_ligase, water]
    print(type(arr[3]))
    return arr*1.25

#the protocol says it need 30fmol of plasmid within the master mix. Method to calculate volume needed
volumesum = 0
for i in partarr:
    i[2] = 30/(i[1]/i[0] * 1000000/650)
    volumesum += i[2]

assembly_v[2] = 30/(i[1]/i[0] * 1000000/650)
volumesum += assembly_v[2]

print(__calcmm__(volumesum,assembly_size))