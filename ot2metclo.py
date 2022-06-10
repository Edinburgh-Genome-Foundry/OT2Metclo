import profile
from opentrons import protocol_api
#import pandas as pd

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




metadata = {
    'apiLevel': '2.0',
    'protocolName': 'Metclo Assembly - hardcoded 6 part assembly',
    'author': 'Daniella Matute <daniella.l.matute@gmail.com',
    'description':'OT-2 protocol that allows for methylase DNA assembly'
}

def run(protocol: protocol_api.ProtocolContext):

################################################################################
# LABWARE
# nest_96_wellplate_100ul_pcr, is placed on the top of the TempDeck 
################################################################################
    tc_mod = protocol.load_module('Thermocycler Module')
    tc_plate = tc_mod.load_labware('biorad_96_wellplate_200ul_pcr')
    tr_20 = protocol.load_labware('opentrons_96_tiprack_20ul', 1)
    lpipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tr_20])
    reagent_plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 4)

    tc_mod.set_lid_temperature(4) 
    tc_mod.set_block_temperature(4)
    tc_mod.open_lid()

################################################################################
# REAGENTS
################################################################################
    #Reagents
    ligase_buffer = reagent_plate.wells('A1')
    ligase = reagent_plate.wells('B1')
    bsai = reagent_plate.wells('C1')
    water = reagent_plate.wells('D1')
    
    #Parts. There is a max of 6 parts with p15a and 4 parts with oriF vector plasmids
    part1 = reagent_plate.wells('A2')
    part2 = reagent_plate.wells('B2')
    part3 = reagent_plate.wells('C2')
    part4 = reagent_plate.wells('D2')
    part5 = reagent_plate.wells('E2')
    part6 = reagent_plate.wells('F2')

    #Assembly vectors (usually p-a )
    Assembly_v = reagent_plate.wells('H2')

################################################################################
# Assembly Plan
################################################################################
#Creating Master Mix
    lpipette.transfer(2,ligase_buffer, tc_plate['A1']) 
    lpipette.transfer(0.5,ligase, tc_plate['A1']) #ligase
    lpipette.transfer(2,part1, tc_plate['A1']) #part1
    lpipette.transfer(2,part2, tc_plate['A1']) #part2
    lpipette.transfer(2,part3, tc_plate['A1']) #part3
    lpipette.transfer(2,part4, tc_plate['A1']) #part4
    lpipette.transfer(2,part5, tc_plate['A1']) #part5
    lpipette.transfer(2,part6, tc_plate['A1']) #part6
    lpipette.transfer(2,Assembly_v, tc_plate['A1']) #Assembly vector
    
    #There is an optional step in protocol to ad 1ul of Bsai to assemblies larger than 30kb
    '''
    if assemblysize > 30000:
        lpipette.transfer(1,reagent_plate['C1'], tc_plate['A1']) #bsaI
        lpipette.transfer(2.5,reagent_plate['D1'], tc_plate['A1'])  #water
    else:
        lpipette.transfer(0.5,reagent_plate['C1'], tc_plate['A1']) #bsaI
        lpipette.transfer(3,reagent_plate['D1'], tc_plate['A1']) 
    '''
    
    lpipette.transfer(0.5,bsai, tc_plate['A1']) #bsaI
    #the master mix should equal 20. This volume is reached with the addition of water
    #this volume is variable
    lpipette.transfer(3,water, tc_plate['A1'])  #water

#Thermocycler
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

