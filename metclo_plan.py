import csv, math
from sre_constants import SUCCESS
import numpy as np
import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos


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
print(parts_con_bp)
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

if (len(part_dictionary)+len(reagent_sum) <= 96) == True:
    plate = {}
    count = 0
    for i in reagent_sum:
        plate, count = __volumecheck__(i, reagent_sum[i], count, plate)
    for i in part_dictionary:
        plate, count = __volumecheck__(i,part_dictionary[i][1], count, plate)
else:
    print('The sum of the parts and reagents is greater than 96. The parts and reagents will not fit in the 96-well plate. Reduce the number of assemblies.')
    sys.exit(1)




class PDF(FPDF):
    def header(self):
        self.set_font('helvetica','B',20)
        self.cell(0,10,'Automated MetClo Assembply Plan',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT, align='C' )
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica','I',10)
        self.cell(0,10,f'Page {self.page_no()}/{{nb}}', align ='C')


pdf = PDF('P','mm','Letter')
pdf.set_auto_page_break(auto =True, margin =15)
pdf.add_page()
pdf.set_font('helvetica', 'BU', 16)
pdf.cell(0,10,f'{str(len(assembly_dictionary))} Assemblies',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT, align='C' )
pdf.set_font('helvetica','B', 12)
w4 = (pdf.w)/4.4
for i in assembly_dictionary:
    pdf.set_font('helvetica','B', 12)
    pdf.cell(w4,10,f'Assembly Name: {i}',border = 0,new_x=XPos.RIGHT)
    pdf.set_font('helvetica','', 12)
    pdf.cell(w4,10,f'Assembly Size: {str("{:,}".format(int(assembly_dictionary[i][0])))}',border = 0,new_x=XPos.RIGHT)
    if int(assembly_dictionary[i][0]) > 10000:
        pdf.cell(w4,10,'(Recommend: Electroporation)',border = 0,new_x=XPos.LMARGIN,new_y=YPos.NEXT)
    else:
        pdf.cell(w4,10,'(Recomend: Heat Shock)',border = 0,new_x=XPos.LMARGIN,new_y=YPos.NEXT)
    pdf.cell(0,10,f'{len(assembly_dictionary[i][1])} Parts',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT)
    count = 0
    for j in assembly_dictionary[i][1]:
        if count <3:
            pdf.cell(w4,8,j,border = True,new_x=XPos.RIGHT)
            count +=1
        else:
            pdf.cell(w4,8,j,border = True,new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            count = 0
    pdf.cell(0,8,'',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT)
    pdf.cell(0,10,'Reagents',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT)
    for x in reagent_sum:
        pdf.cell(w4,8,x,border = True,new_x=XPos.RIGHT)
    pdf.cell(0,8,'',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT)
    pdf.cell(w4,10,'2.0',border = True,new_x=XPos.RIGHT)
    pdf.cell(w4,10,'0.5',border = True,new_x=XPos.RIGHT)
    for j in assembly_dictionary[i][-2:]:
        pdf.cell(w4,10,str(j),border = True,new_x=XPos.RIGHT)
    pdf.cell(0,15,'',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT)
pdf.add_page()
pdf.set_font('helvetica', 'BU', 16)
pdf.cell(0,10,f'{str(len(part_dictionary))} Parts',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT, align='C' )
pdf.set_font('helvetica','', 12)
w5 = (pdf.w)/6.6
pdf.cell(w5+10,10,'Part Name',border = 1,new_x=XPos.RIGHT)
pdf.cell(w5-10,10,'Size',border = 1,new_x=XPos.RIGHT)
pdf.cell(w5-10,10,'Conc.',border = 1,new_x=XPos.RIGHT)
pdf.cell(w5,10,'Times Used',border = 1,new_x=XPos.RIGHT)
pdf.cell(w5+5,10,'Volume(30fmol)',border = 1,new_x=XPos.RIGHT)
pdf.cell(w5+5,10,'Total Volume*1.2',border = 1,new_x=XPos.LMARGIN, new_y=YPos.NEXT)
count = 0
for i in part_dictionary:
    pdf.cell(w5+10,10,i ,border = 1,new_x=XPos.RIGHT)
    pdf.cell(w5-10,10,parts_con_bp[count][2],border = 1,new_x=XPos.RIGHT)
    pdf.cell(w5-10,10,parts_con_bp[count][1],border = 1,new_x=XPos.RIGHT)
    pdf.cell(w5,10,str(part_count[i]),border = 1,new_x=XPos.RIGHT) 
    pdf.cell(w5+5,10,str(part_dictionary[i][0]),border = 1,new_x=XPos.RIGHT)
    pdf.cell(w5+5,10,str(part_dictionary[i][1]),border = 1,new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    count += 1

pdf.ln(15)
pdf.set_font('helvetica', 'BU', 16)
pdf.cell(0,10,'Reagents Total * 1.25',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT, align='C' )
pdf.set_font('helvetica','', 12)
for i in reagent_sum:
    pdf.cell(w4,8,i,border = True,new_x=XPos.RIGHT)
pdf.ln(8)
for i in reagent_sum:
    pdf.cell(w4,8,str(reagent_sum[i]),border = True,new_x=XPos.RIGHT)
#pdf.cell(0,15,'',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT)
pdf.add_page()

pdf.set_font('helvetica', 'BU', 16)
pdf.cell(0,10,'OT2 Set-Up Instructions',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT, align='C' )
pdf.set_font('helvetica','BU', 12)
pdf.cell(0,10,'Materials',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT )


pdf.output('pdf_1.pdf')

