import profile, string
from opentrons import protocol_api
import numpy as np

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
    # Instrument
    p_20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tr_20])
    p_300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tr_300])
################################################################################
# REAGENTS
################################################################################
    #Filling the reagent plate

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
