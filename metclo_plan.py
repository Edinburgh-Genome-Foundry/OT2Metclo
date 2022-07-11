import csv
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def __countinstances__(uncompressed_parts):
    count_parts = {}
    for i in uncompressed_parts:
        count_parts[i] = uncompressed_parts.count(i)
    return count_parts

def __calcvolume__ (ngul, bp):
    'takes the concentration in ng/ul and sequence lenght of the sample and finds the volume needed containing 30fmol'
    volume = round(30/((ngul/(1e-6))/(bp*617.96+ 36.04)),3)
    return volume

def __calcreagents__ (assembly_size, part_volumes):
    ligase_buffer = 2.0
    ligase = 0.5
    bsai = 1.0 if assembly_size > 30000 else 0.5
    sum_parts = sum([ligase_buffer,ligase, bsai, part_volumes])
    water = round(20 - sum_parts,3) if sum_parts < 20 else 0
    reagents = {}
    for v in ['ligase_buffer','ligase','bsai','water']:
        reagents[v] = eval(v) 
    return(reagents)

def __fillplate__(items):
    pass
def __fillfalcon__(items):
    pass

assemblies = []
uncompressed_parts = []

with open('/home/dany/Dropbox/EGF/Metclo/Metclo Simulation/DNA Files/oriFCam/finalassembly.csv', newline='') as csvfile:
    assembly_row = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in assembly_row:
        list_row = [ele for ele in ((', '.join(row)).split(',')) if ele.strip()]
        assemblies.append(list_row)
        for j in list_row:
            uncompressed_parts.append(j)

parts_con_bp = []
with open('/home/dany/Dropbox/EGF/Metclo/Metclo Simulation/DNA Files/oriFCam/parts.csv', newline='') as csvfile:
    part_row = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in part_row:
        list_row = [ele for ele in ((', '.join(row)).split(',')) if ele.strip()]  
        parts_con_bp.append(list_row)

part_count = __countinstances__(uncompressed_parts)

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
    #print(i[1])
    assembly_dictionary[i[0]] = [i[1],i[2:],__calcreagents__(int(i[1]),part_volume_sum)]

for i in reagent_sum:
    for j in assembly_dictionary:
        original = reagent_sum[i]
        reagent_sum[i] = original + ((assembly_dictionary[j])[2][i]*0.25)

def form(path):
        my_canvas = canvas.Canvas(path, pagesize=letter)
        my_canvas.setLineWidth(.3)
        my_canvas.setFont('Helvetica', 15)
        my_canvas.drawString(30, 750, 'INSTRUCTIONS')
        my_canvas.drawString(30, 750, 'ASSEMBLIES')
        my_canvas.drawString(30, 735, 'PARTS')
        my_canvas.drawString(30, 720, 'ASSEMBLY PLAN')
        my_canvas.drawString(30, 705, 'MAP')
        my_canvas.setFont('Helvetica', 11)
        my_canvas.drawString(40, 690, 'OT2 BENCH LAYOUT')
        my_canvas.drawString(40, 675, 'PART & REAGENT 96-WELL-PLATE')
        my_canvas.drawString(40, 660, 'FALCON TUBES')
        my_canvas.drawString(40, 645, 'ASSEMBLY PLATE 96-WELL-PLATE')
        my_canvas.save()

#if __name__ == '__main__':
 #   form('metclo_plan.pdf')


