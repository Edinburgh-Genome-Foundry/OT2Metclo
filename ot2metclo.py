import profile
from opentrons import protocol_api

metadata = {
    'apiLevel': '2.12',
    'protocolName': 'Metclo Assembly',
    'author': 'Daniella Matute <daniella.l.matute@gmail.com',
    'description':'OT-2 protocol that allows for methylase DNA assembly'
}

def run(protocol: protocol_api.ProtocolContext):
    #Labware
    thermocycler = protocol.load_module('thermocycler')
    tc_plate = thermocycler.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

    plate = protocol.load.labware('nest_96_wellplate_100ul_pcr_full_skirt',1)

    left_pipette = protocol.load_instrument('p300_single', 'left', tip_racks=[tiprack])

    #pipetts
   
    #command
    thermocycler.open_lid()
    #the lid should be slightly higher than the highest temp
    thermocycler.set_lid_temperature(85) #the lid should be slightly higher than the highest temp 
    #20ul of raction will be exposed to 37C for 15 min
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