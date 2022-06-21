import profile, string
from opentrons import protocol_api
import numpy as np

################################################################################
# METHODS
################################################################################
def __calcvolume__ (ngul, bp):
    'takes the concentration in ng/ul and sequence lenght of the sample and finds the volume needed containing 30fmol'
    volume = round(30/((ngul/(1e-6))/(bp*617.96+ 36.04)),3)
    return volume

def __getparts__ (file):
    with open(file, 'r') as parts_file:
        parts={}
        for l in parts_file:  
            name, ngul, bp = l.strip().split(',')
            volume = __calcvolume__(float(ngul),int(bp))
            parts[name]=[float(ngul),int(bp),volume] 
    return(parts)

def __calcreagents__ (parts, as_s):
    sum_parts = round(sum((parts[t][2]) for t in parts),3)
    ligase_buffer = 2.0
    ligase = 0.5
    bsai = 1.0 if as_s > 30000 else 0.5
    water = round(20 - sum([ligase_buffer,ligase, bsai, sum_parts]),3) if sum([ligase_buffer,ligase, bsai, sum_parts]) < 20 else 0
    reagents = {}
    for v in ['ligase_buffer','ligase','bsai','water']:
        reagents[v] = eval(v) 
    return(reagents)

def __checkwells__ (reagent_arr):
    test = np.zeros(8, dtype=bool)
    print(test)
    for i in reagent_arr.T:
        if i == test:
            print('yay')

alpha = dict(zip(range(0,8),string.ascii_uppercase))
numb = np.linspace(1,12,12)
reagent_arr = np.zeros((8,12), dtype=bool)
constructarr = np.zeros((8,12), dtype=bool)

#parts_file = input("Enter the path of your <parts>.txt:")
# #assemblysize= int(input("Enter final assembly size (bp):") )
parts_file = '/home/dany/data/software/GitHub/metclo/test_assembly_parts.txt'
assemblysize= 800000


parts = __getparts__(parts_file) 
reagents = __calcreagents__ (parts, assemblysize)

print("PARTS ('part_name':[ng/ul, bp, volume])\n",parts, "\n\nREAGENTS ('reagent':volume)", reagents, "\n\nASSEMBLY SIZE", assemblysize )
__checkwells__(reagent_arr)
################################################################################
# PROTOCOL
################################################################################

metadata = {
    'apiLevel': '2.3',
    'protocolName': 'Metclo Assembly - hardcoded with one assembly that cna change in size',
    'author': 'Daniella Matute <daniella.l.matute@gmail.com',
    'description':'OT-2 protocol that allows for methylase DNA assembly'
}

def run(protocol: protocol_api.ProtocolContext):

################################################################################
# LABWARE
# nest_96_wellplate_100ul_pcr, is placed on the top of the TempDeck 
################################################################################
    
    # Instrument
    p_20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tr_20])
    p_300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tr_300])
    
    # Modules
    temp_module = protocol.load_module("temperature module", 1)
    mag_module = protocol.load_module("magnetic module gen2", 4)
    tc_mod = protocol.load_module("thermocycler module")
    
    # Labware
    tr_20 = protocol.load_labware('opentrons_96_tiprack_20ul', 9)
    tr_300 = protocol.load_labware('opentrons_96_tiprack_300ul', 6)
    part_plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 2)
    tc_plate = tc_mod.load_labware('biorad_96_wellplate_200ul_pcr')
    falcon = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical',5)
    
################################################################################
# REAGENTS
################################################################################
    #Filling the reagent plate


    
'''
    globals()['ligase_buffer'] = part_plate.wells('A1')
    globals()['ligase'] = part_plate.wells('B1')
    globals()['bsai'] = part_plate.wells('C1')
    globals()['water'] = part_plate.wells('D1')
    
    for key,v in parts.items():
        n = (list(parts.keys()).index(key))
        p = alpha[n] + '2'
        globals()[key]= part_plate.wells(p)

################################################################################
# Assembly 
################################################################################
#Creating Master Mix
    tc_mod.set_lid_temperature(4) 
    tc_mod.set_block_temperature(4)
    tc_mod.open_lid()
    
    for i in parts:
        protocol.comment('Transferring '+ i)
        lpipette.transfer(parts[i][2],globals()[i], tc_plate['A1'])

    
    for i in reagents:
        protocol.comment('Transferring '+ i)
        lpipette.transfer(reagents[i],globals()[i],tc_plate['A1'])


#Thermocycler
    protocol.comment('Assembly reaction ongoing')
    tc_mod.set_lid_temperature(85)
    tc_mod.set_block_temperature(37, hold_time_minutes=15, block_max_volume=20)
    tc_mod.close_lid()
    profile = [
        {'temperature':37, 'hold_time_minutes':2},
        {'temperature':16, 'hold_time_minutes':5},
        {'temperature':37, 'hold_time_minutes':20},
        {'temperature':80, 'hold_time_minutes':5}
    ]
    tc_mod.execute_profile(steps= profile, repetitions= 45, block_max_volume= 20)
    tc_mod.set_lid_temperature(4) 
    tc_mod.set_block_temperature(4)
    protocol.comment('Metclo assembly done. Assembly is incubating at 4 degrees Celsius.')
    '''