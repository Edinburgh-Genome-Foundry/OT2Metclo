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

def __makeplate__ ():
    plate_dictionary = {}
    alpha = list(string.ascii_uppercase)[:8]
    for j in range(12):
        for i in range(8):
            plate_dictionary[alpha[i]+str(j+1)]= ''
    return plate_dictionary



assembly_data =  __openfile__('assembly_data.csv')
part_data = __openfile__('part_data.csv')
reagent_data = __openfile__('reagents_data.csv')
print('ASSEMBLY DATA\n', assembly_data)
print('PART DATA\n', part_data)
print('REAGENT DATA\n', reagent_data)



plate_position = {}
count = 0
for i in reagent_data:
    plate_position, count = __volumecheck__(i[0],float(i[1]),count, plate_position)
for i in part_data:
    plate_position, count = __volumecheck__(i[0],float(i[1]),count, plate_position)

parts_plate = reagent_data + part_data

partsplate_tvolume= {}
count = 0
for i in parts_plate:
    if len(i) == 2:
        partsplate_tvolume[i[1]] = count
        count += 1
    if len(i) > 2:
        partsplate_tvolume[i[2]] = count
        count += 1





tcplate_position = {}
for i in range (len(assembly_data)):
    tcplate_position[assembly_data[i][0]] = i




print('PLATE POSITION\n', plate_position)
print(partsplate_tvolume)
print('££tc plate',tcplate_position)


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
    tc_plate = tc_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    falcon = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical',5)
    
    # Instrument
    p_20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tr_20])
    p_300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tr_300])

    for i in assembly_data:
        #ligasebuffer
        p_20.transfer(int(i[3]),  )
        p_20.transfer(5, part_plate.wells()[i],tc_plate.wells()[i])

################################################################################
# REAGENTS
################################################################################


    '''
    for i in plate_position:
        a= plate_position[i]
        print(a)
        if a == reagent_data[0][0]: #ligase_buffer
            p_20.distribute(2,part_plate.wells()[i], [tc_plate.wells()[w] for w in list(tcplate_position.keys())])
            print('reagent')
        if a.startswith('ligase') == True:
            p_20.distribute(0.5,part_plate.wells()[i], [tc_plate.wells()[w] for w in list(tcplate_position.keys())])


    for key,v in parts_plate.items():
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