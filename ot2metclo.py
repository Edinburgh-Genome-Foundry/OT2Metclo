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
    lpipette = protocol.load_instrument('p20_single', 'left', tip_racks=tr_20)
    reagent_plate = protocol.load_labware('nest_96_wellplate_200ul_flat','2')

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
    
################################################################################
# PROTOCOL
################################################################################
    thermocycler.set_lid_temperature(4) 
    thermocycler.set_block_temperature(4)

#Making a metclo assembly reaction for one insert
#volumes are not a priority right now

    lpipette.pick_up_tip()
    lpipette.transfer(2,reagent_plate()['A1'], tc_plate()['A1']) #ligase buffer
    # volume is too small for the pipette
    lpipette.transfer(0.5,reagent_plate()['B1'], tc_plate()['A1']) #ligase
    lpipette.transfer(0.5,reagent_plate()['C1'], tc_plate()['A1']) #bsaI

    lpipette.transfer(3,reagent_plate()['A2'], tc_plate()['A1']) #insert1
    lpipette.transfer(2,reagent_plate()['B2'], tc_plate()['A1']) #insert2
    lpipette.transfer(2.5,reagent_plate()['C2'], tc_plate()['A1']) #insert3

    lpipette.transfer(2.5,reagent_plate()['H1'], tc_plate()['A1']) #Assembly vector

    lpipette.transfer(7,reagent_plate()['D1'], tc_plate()['A1'])  #water

    
