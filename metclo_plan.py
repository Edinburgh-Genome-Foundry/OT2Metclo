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
    volume = round(30/(((ngul*1e-9)/((bp*617.69)+36.04))*1e15),3)
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

def __volumecheck__ (i, x):
    wellvolume = []
    plate = []
    count =0
    if x/200 < 1:
        plate.append(i)
        count +=1
        wellvolume.append(x)
    else:
        wells = math.ceil(x/200)
        for j in range (wells):
            if x-200 > 0:
                wellvolume.append(200) 
                x = x-200
            else:
                wellvolume.append(x)
        for t in range (wells):
            plate.append(i+ '.'+str(t+1))
            count +=1
    return plate, wellvolume, count

def __check_part_congruency__(parts_concentration_size, part_count, part_file_name, assembly_file_name):
# Checks if the parts in the assembly and part files are congruent
    irregular_parts = []
    irregular_assembly = {}
    _check = False
    for i in parts_concentration_size:
        try: 
            n=part_count[i[0]]
        except: 
            irregular_parts.append(i[0])
    for i in part_count:
        check_ = False
        for j in parts_concentration_size:
            if i == j[0]:
                check_ = True
        if check_ == False:
            irregular_assembly[i] = []
            for k in assemblies:
                irregular_assembly[i].append(k[0])

    if len(irregular_parts) != 0 :
        print(part_file_name, ' has parts that are not found in ', assembly_file_name, ':')
        for i in irregular_parts:
            print('\t',i)
        _check = True

    if len(irregular_assembly) != 0 :
        print(assembly_file_name, ' has assemblies with parts that are not found in ', part_file_name, ':')
        for i in irregular_assembly:
            print('\t',i,' found in assemblies ',irregular_assembly[i])
        _check = True

    if _check == True: sys.exit(1)

#Lists that will collect the .csv information and calculations
assemblies = []
uncompressed_parts = []
parts_concentration_size = []

#Input .csv files 
assembly_path = '/home/dany/Dropbox/EGF/Metclo/Metclo Simulation/DNA Files/oriFCam/finalassembly.csv'
part_path = '/home/dany/Dropbox/EGF/Metclo/Metclo Simulation/DNA Files/oriFCam/parts.csv'
#assembly_path = input('Input Full Pathway of Assembly (.csv):\n')
#part_path = input('Input Full Pathway of Parts (.csv):\n')
assembly_file_name = assembly_path.split("/")[-1]
part_file_name = part_path.split("/")[-1]



#Opening assembly document and extracts its information
#part_count collects the presence of a part within the all the assemblies
try:
    with open(assembly_path, newline='') as csvfile:
        assembly_row = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in assembly_row:
            list_row = [ele for ele in ((', '.join(row)).split(',')) if ele.strip()]
            assemblies.append(list_row)
            for j in list_row: 
                if list_row.index(j) > 1:
                    uncompressed_parts.append(j)
        part_count = __countinstances__(uncompressed_parts)
    # does not fit right because we dont know how mnay wells we need
    if len(part_count) > 96:
        print('Too many parts. Max number of parts = 96, given number of parts = '+ str(len(part_count)))
        sys.exit(1)
    if len(assemblies) > 96:
        print('Too many assemblies. Max number of assemblies = 96, ',assembly_file_name ,' assemblies = '+ str(len(assemblies)))
        sys.exit(1)
except:
    print(assembly_file_name, ' error.')
    sys.exit(1)

#Opening part document and extracts the information
try:
    with open(part_path, newline='') as csvfile:
        part_row = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in part_row:
            list_row = [ele for ele in ((', '.join(row)).split(',')) if ele.strip()]  
            parts_concentration_size.append(list_row)
except:
    print(part_file_name,' error.')
    sys.exit(1)

__check_part_congruency__(parts_concentration_size, part_count, part_file_name, assembly_file_name)

print('assemblies\n' , assemblies)
print('uncompressed_parts\n' ,uncompressed_parts)
#part count counts tyhe frags and the bp
print('part count\n' ,part_count)
print('parts_concentration_size' , parts_concentration_size)








#Making part dictionary
part_dictionary = {}
for i in part_count:
    for j in parts_concentration_size:
        if i == j[0]:
            #print((float(j[1]),float(j[2])))
            single_volume = __calcvolume__(float(j[1]),float(j[2]))
            #print(single_volume)
            total_volume = round(part_count[i]*single_volume*1.2,3)
            #######ERRASE#####
            if j[0] == 'pa':
                total_volume = 420
            ##################
            plate,wellvolume, count = __volumecheck__(j[0],total_volume)
            for q in range(len(plate)):
                part_dictionary[plate[q]] = [round(single_volume,3),round(wellvolume[q],3)]

print('PART DICTIONARY\n',part_dictionary)

#Making assembly dictionary
assembly_dictionary = {}
for i in assemblies:
    part_volume_sum = 0
    for j in i[2:]:
        count = 0
        for q in part_dictionary: 
            if j == q.split('.',1)[0]:
                count +=1
                volume =part_dictionary[q][0]
        if count == 1:
            part_volume_sum += round(volume,3)
        else:
            part_volume_sum += round(volume,3)
    part_volume_sum = round(part_volume_sum,3)
    bsai, water = __calcreagents__(int(i[1]),part_volume_sum)

    assembly_dictionary[i[0]] = [i[1],i[2:],2, 0.5,bsai, water]

print('ASSEMBLY DICTIONARY\n', assembly_dictionary)

#Making reagent dictionary
reagent_dictionary = {}
reagents = ['ligase_buffer', 'ligase', 'bsai', 'water']
assembly_count = len(assembly_dictionary) 
for i in reagents:
    total_volume=0
    if i == 'ligase_buffer':
        total_volume = 2*assembly_count
        total_volume = 450
        plate,wellvolume, count = __volumecheck__(i,total_volume)
    if i == 'ligase':
        total_volume = 0.5*assembly_count
        plate,wellvolume, count = __volumecheck__(i,total_volume)
    if i == 'bsai':
        for j in assembly_dictionary:
            total_volume += assembly_dictionary[j][2]
        plate,wellvolume, count = __volumecheck__(i,total_volume)
    if i == 'water':
        for j in assembly_dictionary:
            total_volume += assembly_dictionary[j][3]
        plate,wellvolume, count = __volumecheck__(i,total_volume)
    for q in range(len(plate)):
        reagent_dictionary[plate[q]] = [round(wellvolume[q],3)]

print('REAGENT DICTIONARY\n',reagent_dictionary)

'''
if (len(part_dictionary)+len(reagent_dictionary) > 96) == True:
    print(f'The sum of the parts and reagents {len(part_dictionary)+len(reagent_dictionary)}is greater than 96. The parts and reagents will not fit in the 96-well plate. Reduce the number of assemblies.')
    sys.exit(1)

header = [['assembly name','assembly size', 'parts', 'bsai','water'],['part name', 'single', 'sum'],['reagent', 'sum']]
doc = ['assembly_data.csv','part_data.csv','reagents_data.csv']
data = (assembly_dictionary, part_dictionary, reagent_dictionary)

for i in range (len(header)):
    __makecvs__(doc[i],header[i],data[i])


class PDF(FPDF):
    def header(self):
        self.set_font('helvetica','B',20)
        self.cell(0,10,'Automated MetClo Assembly Plan',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT, align='C' )
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
    for x in reagent_dictionary:
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
#for i in part_dictionary:
    print(i)
    pdf.cell(w5+10,10,i ,border = 1,new_x=XPos.RIGHT)
    pdf.cell(w5-10,10,parts_concentration_size[count][2],border = 1,new_x=XPos.RIGHT)
    pdf.cell(w5-10,10,parts_concentration_size[count][1],border = 1,new_x=XPos.RIGHT)
    #pdf.cell(w5,10,str(part_count[i]),border = 1,new_x=XPos.RIGHT) 
    pdf.cell(w5+5,10,str(part_dictionary[i][0]),border = 1,new_x=XPos.RIGHT)
    pdf.cell(w5+5,10,str(part_dictionary[i][1]),border = 1,new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    #count += 1

pdf.ln(15)
pdf.set_font('helvetica', 'BU', 16)
pdf.cell(0,10,'Reagents Total * 1.25',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT, align='C' )
pdf.set_font('helvetica','', 12)
for i in reagent_dictionary:
    pdf.cell(w4,8,i,border = True,new_x=XPos.RIGHT)
pdf.ln(8)
for i in reagent_dictionary:
    pdf.cell(w4,8,str(reagent_dictionary[i]),border = True,new_x=XPos.RIGHT)
#pdf.cell(0,15,'',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT)
pdf.add_page()

pdf.set_font('helvetica', 'BU', 16)
pdf.cell(0,10,'OT2 Set-Up Instructions',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT, align='C' )
pdf.set_font('helvetica','BU', 12)
pdf.cell(0,10,'Materials',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT )

try: 
    pdf.output('metclo_plan.pdf')
    print('metclo_plan.pdf written succesfully.')
except:
    print('metclo_plan.pdf not written')
    sys.exit(1)

'''