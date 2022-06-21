import profile
from opentrons import protocol_api


metadata = {
    'apiLevel': '2.3',
    'protocolName': 'Metclo Assembly - hardcoded 6 part assembly',
    'author': 'Daniella Matute <daniella.l.matute@gmail.com',
    'description':'OT-2 protocol that allows for methylase DNA assembly'
}

def run(protocol: protocol_api.ProtocolContext):

################################################################################
# LABWARE
# nest_96_wellplate_100ul_pcr, is placed on the top of the TempDeck 
################################################################################

    # Load a Temperature Module GEN1 in deck slot.
    temperature_module = protocol.load_module("temperature module", 1)
    # Load a Magnetic Module GEN2 in deck slot.
    magnetic_module = protocol.load_module("magnetic module gen2", 4)
    # Thermocycler module:
    tc_mod = protocol.load_module("thermocycler module")

    tc_plate = tc_mod.load_labware('biorad_96_wellplate_200ul_pcr')
    tr_20 = protocol.load_labware('opentrons_96_tiprack_20ul', 3)
    lpipette = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[tr_20])
    reagent_plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 6)

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

    lpipette.transfer(2,reagent_plate['A1'], tc_plate['A1']) #ligase buffer
    lpipette.transfer(0.5,reagent_plate['B1'], tc_plate['A1']) #ligase
    lpipette.transfer(2,reagent_plate['A2'], tc_plate['A1']) #part1
    lpipette.transfer(2,reagent_plate['B2'], tc_plate['A1']) #part2
    lpipette.transfer(2,reagent_plate['C2'], tc_plate['A1']) #part3
    lpipette.transfer(2,reagent_plate['D2'], tc_plate['A1']) #part4
    lpipette.transfer(2,reagent_plate['E2'], tc_plate['A1']) #part5
    lpipette.transfer(2,reagent_plate['F2'], tc_plate['A1']) #part6
    lpipette.transfer(2,reagent_plate['H1'], tc_plate['A1']) #Assembly vector
    
    
    lpipette.transfer(0.5,reagent_plate['C1'], tc_plate['A1']) #bsaI
    #the master mix should equal 20. This volume is reached with the addition of water
    #this volume is variable
    lpipette.transfer(3,reagent_plate['D1'], tc_plate['A1'])  #water

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

