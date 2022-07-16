import profile, string, csv, sys, math
from opentrons import protocol_api
import numpy as np


def __openfile__(file):    
    try:
        with open(file, newline='') as csvfile:
            rows = csv.reader(csvfile)
            header = next(rows)
            if header != None:
                data = []
                for j in rows:
                    data.append(j)
                return data
    except:
        print('File error.')
        sys.exit(1)

def __volumecheck__ (i, x, count, plate):
    if x/200 < 1:
        plate[count] = i
        count +=1
    else:
        wells = math.ceil(x/200)
        for t in range (wells):
            plate[count] = i+ '.'+str(t+1)
            count +=1
    return plate, count



assembly_data =  __openfile__('assembly_data.csv')
part_data = __openfile__('part_data.csv')
reagent_data = __openfile__('reagents_data.csv')

plate_position = {}
count = 0
for i in reagent_data:
    plate_position, count = __volumecheck__(i[0],float(i[1]),count, plate_position)
for i in part_data:
    plate_position, count = __volumecheck__(i[0],float(i[1]),count, plate_position)

tcplate_position = {}
count = 0
for i in range (len(assembly_data)):
    tcplate_position[i] = assembly_data[i][0]

print(assembly_data)
print(part_data)
print(reagent_data)
print(plate_position)
print(tcplate_position)





metadata = {
    'apiLevel': '2.3',
    'protocolName': 'Metclo Assembly - hardcoded with one assembly that cna change in size',
    'author': 'Daniella Matute <daniella.l.matute@gmail.com',
    'description':'OT-2 protocol that allows for methylase DNA assembly'
}

def run(protocol: protocol_api.ProtocolContext):

################################################################################
# LABWARE
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





    print(tcplate_position)
    print(*tcplate_position)
    print({*tcplate_position})
    print([*tcplate_position])
    print(type([*tcplate_position]))



################################################################################
# REAGENTS
################################################################################
    for i in range (len(tcplate_position)):
        p_20.distribute(2, part_plate['A1'], tc_plate.wells()[i])
        #globals()[plate_position[i]] = part_plate.wells_by_name()[i]
    #print(tc_plate.wells()[1])
    
    
        
    
    


    
    

    




    '''
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