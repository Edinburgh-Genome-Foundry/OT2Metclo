import profile
from opentrons import protocol_api
#import pandas as pd

metadata = {
    'apiLevel': '2.12',
    'protocolName': 'Metclo Assembly',
    'author': 'Daniella Matute <daniella.l.matute@gmail.com',
    'description':'OT-2 protocol that allows for methylase DNA assembly'
}

def __calcfmol__(c,bp):
        n = c/(660*bp)* 10^15
        return n

def run(protocol: protocol_api.ProtocolContext):

################################################################################
# LABWARE
# nest_96_wellplate_100ul_pcr, is placed on the top of the TempDeck 
################################################################################
    tc_mod = protocol.load_module('Thermocycler Module')
    tc_plate = tc_mod.load_labware('biorad_96_wellplate_200ul_pcr')
    tr_20 = protocol.load_labware('opentrons_96_tiprack_20ul', 1)
    lpipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tr_20])
    reagent_plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 2)

################################################################################
# REAGENTS
################################################################################
    ligase_buffer = reagent_plate.wells('A1')
    ligase = reagent_plate.wells('B1')
    bsai = reagent_plate.wells('C1')
    #should I add a water trough? or tube? I need to calculate how much water would be 
    # needed because I dont think a 200ul well will be enough     
    water = reagent_plate.wells('D1')
    #The way of inserting the inserts would need to change further on 
    insert1 = reagent_plate.wells('A2')
    insert2 = reagent_plate.wells('B2')
    insert3 = reagent_plate.wells('C2')
    Assembly_v = reagent_plate.wells('H1')

    tc_mod.set_lid_temperature(4) 
    tc_mod.set_block_temperature(4)


################################################################################
# Assembly Plan
################################################################################
#    xfile = input("Enter pathway to excel (.xlsx) document: ")
#    df = pd.read_excel (r'xfile')
#    Assembly = [['frag1', 32,2250],['frag2',26,3000], ['frag3', 17,3400],['vector',20, 8000]]
    assemblysize = 20000   


    lpipette.transfer(2,reagent_plate['A1'], tc_plate['A1']) #ligase buffer
    # volume is too small for the pipette

    lpipette.transfer(0.5,reagent_plate['B1'], tc_plate['A1']) #ligase
    if assemblysize > 30000:
        lpipette.transfer(1,reagent_plate['C1'], tc_plate['A1']) #bsaI
    else: 
        lpipette.transfer(0.5,reagent_plate['C1'], tc_plate['A1']) #bsaI
    lpipette.transfer(3,reagent_plate['A2'], tc_plate['A1']) #insert1
    lpipette.transfer(2,reagent_plate['B2'], tc_plate['A1']) #insert2
    lpipette.transfer(2.5,reagent_plate['C2'], tc_plate['A1']) #insert3
    lpipette.transfer(2.5,reagent_plate['H1'], tc_plate['A1']) #Assembly vector
    lpipette.transfer(7,reagent_plate['D1'], tc_plate['A1'])  #water
    tc_mod.set_lid_temperature(85)
    tc_mod.set_block_temperature(37, hold_time_minutes=15, block_max_volume=20)
    tc_mod.close_lid()

    for x in range(45):
        tc_mod.set_block_temperature(37, hold_time_minutes=2, block_max_volume=20)
        tc_mod.set_block_temperature(16, hold_time_minutes=5, block_max_volume=20)
        tc_mod.set_block_temperature(37, hold_time_minutes=20, block_max_volume=20)

    tc_mod.deactivate()
    tc_mod.open_lid()
