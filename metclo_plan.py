import csv
from sre_constants import SUCCESS
import numpy as np
import sys

def __countinstances__(uncompressed_parts):
    count_parts = {}
    for i in uncompressed_parts:
        count_parts[i] = uncompressed_parts.count(i)
    return count_parts

def __calcvolume__(ngul, bp):
    'takes the concentration in ng/ul and sequence lenght of the sample and finds the volume needed containing 30fmol'
    volume = round(30/((ngul/(1e-6))/(bp*617.96+ 36.04)),3)
    return volume

def __calcreagents__(assembly_size, part_volumes):
    ligase_buffer = 2.0
    ligase = 0.5
    bsai = 1.0 if assembly_size > 30000 else 0.5
    sum_parts = sum([ligase_buffer,ligase, bsai, part_volumes])
    water = round(20 - sum_parts,3) if sum_parts < 20 else 0 
    return bsai, water

def __makecvs__(doc, header, data):
    with open(doc,'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        try:
            for i in data:
                row = [i]
                for j in data[i]:
                    row.append(j)
                writer.writerow(row)
        except: 
            for i in data:
                row = [i, reagent_sum[i]]
                writer.writerow(row)
    print(doc,' written succesfully.')

assemblies = []
uncompressed_parts = []
assembly_path = '/home/dany/Dropbox/EGF/Metclo/Metclo Simulation/DNA Files/oriFCam/finalassembly.csv'
part_path = '/home/dany/Dropbox/EGF/Metclo/Metclo Simulation/DNA Files/oriFCam/parts.csv'
#assembly_path = input('Input Full Pathway of Assembly (.csv):\n')
#part_path = input('Input Full Pathway of Parts (.csv):\n')
try:
    with open(assembly_path, newline='') as csvfile:
        assembly_row = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in assembly_row:
            list_row = [ele for ele in ((', '.join(row)).split(',')) if ele.strip()]
            assemblies.append(list_row)
            for j in list_row:
                uncompressed_parts.append(j)
    if len(assemblies) > 96:
        print('Too manny assemblies. Max number of assemblies = 96, <assembly_plan>.csv assemblies = '+ str(len(assemblies)))
        sys.exit(1)
except:
    print('Assembly file error.')
    sys.exit(1)

parts_con_bp = []
try:
    with open(part_path, newline='') as csvfile:
        part_row = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in part_row:
            list_row = [ele for ele in ((', '.join(row)).split(',')) if ele.strip()]  
            parts_con_bp.append(list_row)
except:
    print('Part file error.')
    sys.exit(1)

part_count = __countinstances__(uncompressed_parts)
if len(part_count) > 96:
    print('Too manny parts. Max number of parts = 96, given number of parts = '+ str(len(part_count)))
    sys.exit(1)

part_dictionary = {}
for i in part_count:
    for j in parts_con_bp:
        if i == j[0]:
            single_volume = __calcvolume__(float(j[1]),float(j[2]))
            part_dictionary[i] = [round(single_volume,3),round(part_count[i]*single_volume*1.2,3)]

assembly_dictionary = {}
reagent_sum = {'ligase_buffer': 0.0, 'ligase': 0.0, 'bsai': 0.0, 'water': 0.0}
for i in assemblies:
    part_volume_sum = 0
    for j in i[2:]:
        part_volume_sum += round(part_dictionary[j][0],3)
    bsai, water = __calcreagents__(int(i[1]),part_volume_sum)
    assembly_dictionary[i[0]] = [i[1],i[2:],bsai, water]
    reagent_sum['ligase_buffer'] += 2*1.25
    reagent_sum['ligase'] += 0.5*1.25
    reagent_sum['bsai'] += bsai*1.25
    reagent_sum['water'] += water*1.25

header = [['assembly name','assembly size', 'parts', 'bsai','water','heat shock'],['part name', 'single', 'sum'],['reagent', 'sum']]
doc = ['assembly_data.csv','part_data.csv','reagents_data.csv']
data = (assembly_dictionary, part_dictionary, reagent_sum)

for i in range (len(header)):
    __makecvs__(doc[i],header[i],data[i])
