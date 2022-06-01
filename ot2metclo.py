import profile
from opentrons import protocol_api

metadata = {
    'apiLevel': '2.12',
    'protocolName': 'Metclo Assembly',
    'author': 'Daniella Matute <daniella.l.matute@gmail.com',
    'description':'OT-2 protocol that allows for methylase DNA assembly'
}

def run(protocol: protocol_api.ProtocolContext):

################################################################################
# LABWARE
# nest_96_wellplate_100ul_pcr, is placed on the top of the TempDeck 
################################################################################
    thermocycler = protocol.load_module('thermocycler')
    tc_plate = thermocycler.load_labware('biorad_96_wellplate_200ul_pcr')
    thermocycler.set_temperature(4)
        
    tr_20 = protocol.load_instrument('opentrons_96_tiprack_20ul','1')
    left_pipette = protocol.load_instrument('p20_single', 'left', tip_racks=tr_20)
    reagent_plate = protocol.load_labware('nest_96_wellplate_200ul_flat','2')

################################################################################
# REAGENTS
################################################################################
    ligase_buffer = reagent_plate.wells('A1')
    ligase = reagent_plate.wells('B1')
    bsai = reagent_plate.wells('C1')
    water = reagent_plate.wells('D1')
    #The way of inserting the inserts would need to change further on 
    insert1 = reagent_plate.wells('A2')
    insert2 = reagent_plate.wells('B2')
    insert3 = reagent_plate.wells('C2')
    Assembly_v = reagent_plate.wells('H1')
    
    
    thermocycler.open_lid()
    thermocycler.set_lid_temperature(4) #the lid should be slightly higher than the highest temp 

    thermocycler.set_block_temperature(37, hold_time_seconds=900, block_max_volume=20)
    thermocycler.close_lid()
    #they are updating this. the next release 6.0.0 is expected to solve this issue
    profile = [
        {'temperature': 37, 'hold_time_seconds': 120},
        {'temperature': 16, 'hold_time_seconds': 300},
        {'temperature': 37, 'hold_time_seconds': 1200},
        {'temperature': 80, 'hold_time_seconds': 300}
    ]
    thermocycler.execute_profile(steps=profile, repetitions = 45, block_max_volume=20) 
    thermocycler.deactivate()
    thermocycler.open_lid()