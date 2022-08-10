import os
import csv, math, string
import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Counts the instances a part is used throughout all assemblies
def _countinstances(uncompressed_parts):
    count_parts = {}
    for i in uncompressed_parts:
        count_parts[i] = uncompressed_parts.count(i)
    return count_parts


# Calculates the volume with 30fmol of parts.
def _calcvolume(ngul, bp):
    volume = round(30 / (((ngul * 1e-9) / ((bp * 617.69) + 36.04)) * 1e15), 3)
    return volume


# Provides the bsai and water volume unique to each assembly
def _calcreagents(assembly_size, part_volumes):
    ligase_buffer = 2.0
    ligase = 0.5
    bsai = 1.0 if assembly_size > 30000 else 0.5
    sum_parts = sum([ligase_buffer, ligase, bsai, part_volumes])
    water = round(20 - sum_parts, 3) if sum_parts < 20 else 0
    return bsai, water


# Makes .csv files, as inputs for the opentron protocol
def _makecvs(doc, header, data):
    with open(doc, "w") as f:
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
                row = [i, data[i]]
                writer.writerow(row)
    print(doc, " written succesfully.")


# The maximum volume within the reagent plate is 200ul.
# The method checks if the volume needed is over 200ul, if so, the volume is devided into different wells
def _volumecheck(i, x):
    wellvolume = []
    plate = []
    count = 0
    if x / 200 < 1:
        plate.append(i)
        count += 1
        wellvolume.append(x)
    else:
        wells = math.ceil(x / 200)
        for j in range(wells):
            if x - 200 > 0:
                wellvolume.append(200)
                x = x - 200
            else:
                wellvolume.append(x)
        for t in range(wells):
            plate.append(i + "." + str(t + 1))
            count += 1
    return plate, wellvolume, count


# Checks if the parts within the two files are congruent with eachother
def _check_part_congruency(
    parts_concentration_size, part_count, part_file_name, assembly_file_name
):
    irregular_parts = []
    irregular_assembly = {}
    _check = False
    for i in parts_concentration_size:
        try:
            n = part_count[i[0]]
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

    if len(irregular_parts) != 0:
        print(
            part_file_name, " has parts that are not found in ", assembly_file_name, ":"
        )
        for i in irregular_parts:
            print("\t", i)
        _check = True

    if len(irregular_assembly) != 0:
        print(
            assembly_file_name,
            " has assemblies with parts that are not found in ",
            part_file_name,
            ":",
        )
        for i in irregular_assembly:
            print("\t", i, " found in assemblies ", irregular_assembly[i])
        _check = True

    if _check == True:
        sys.exit(1)


# Creates a dictionary with the well-identifier as a key, and
def _plate_dictionary_creator(reagent_total, part_dictionary):
    alpha = list(string.ascii_uppercase)[:8]
    plate_dictionary = {}
    reagent_list = list(reagent_total.items())
    part_list = list(part_dictionary.items())
    count = 0
    for j in range(12):
        for i in range(8):
            plate_dictionary[alpha[i] + str(j + 1)] = ""
    for i in plate_dictionary:
        if count < len(reagent_list):
            plate_dictionary[i] = reagent_list[count]
            count += 1
    count = 0
    for i in plate_dictionary:
        if plate_dictionary[i] == "" and count < len(part_list):
            plate_dictionary[i] = part_list[count][0], part_list[count][1][1]
            count += 1
    return plate_dictionary


# Collect the .csv data and other calculations
assemblies = []
uncompressed_parts = []
parts_concentration_size = []

# Input .csv files
#######################################################
# Examples
# assembly_path = 'example/input_files/finalassembly.csv'
# part_path = 'example/input_files/parts.csv'
#######################################################
assembly_path = input("Input Full Pathway of Assembly (.csv):\n")
part_path = input("Input Full Pathway of Parts (.csv):\n")
assembly_file_name = assembly_path.split("/")[-1]
part_file_name = part_path.split("/")[-1]


# Opens assembly file and extracts its information
try:
    with open(assembly_path, newline="") as csvfile:
        assembly_row = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for row in assembly_row:
            list_row = [ele for ele in ((", ".join(row)).split(",")) if ele.strip()]
            assemblies.append(list_row)
            # A single part can be used in multiple assemblies, these are counted and stored.
            for j in list_row:
                if list_row.index(j) > 1:
                    uncompressed_parts.append(j)
        part_count = _countinstances(uncompressed_parts)
    # The number of assemblies is checked, as the plate is limited to 96 assemblies.
    if len(assemblies) > 96:
        print(
            "Too many assemblies. Max number of assemblies = 96, ",
            assembly_file_name,
            " assemblies = " + str(len(assemblies)),
        )
        sys.exit(1)
except:
    print(assembly_file_name, " error.")
    sys.exit(1)

# Opening part document and extracts its information
try:
    with open(part_path, newline="") as csvfile:
        part_row = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for row in part_row:
            list_row = [ele for ele in ((", ".join(row)).split(",")) if ele.strip()]
            parts_concentration_size.append(list_row)
except:
    print(part_file_name, " error.")
    sys.exit(1)

# checks that the parts within the assembly file are present in the partfile and vice versa
_check_part_congruency(
    parts_concentration_size, part_count, part_file_name, assembly_file_name
)

# Makes part dictionary containg the volume (30fmol) need for a single assembly and the total volume thoughtout all assemblues *1.2
# Makes a dictionary containing the parts that have over 200 ul. It includes the number of wells, a single (30fmol) volume and the total volume thoughtout all assemblues *1.2
part_dictionary = {}
many_wells_parts = {}
for i in part_count:
    for j in parts_concentration_size:
        if i == j[0]:
            single_volume = _calcvolume(float(j[1]), float(j[2]))
            total_volume = round(part_count[i] * single_volume * 1.2, 3)
            #############
            #############
            # if i == 'bq': total_volume = 690
            #############
            #############
            plate, wellvolume, count = _volumecheck(j[0], total_volume)
            if len(plate) > 1:
                many_wells_parts[j[0]] = [
                    len(plate),
                    round(single_volume, 3),
                    sum(wellvolume),
                ]
            for q in range(len(plate)):
                part_dictionary[plate[q]] = [
                    round(single_volume, 3),
                    round(wellvolume[q], 3),
                ]

# Making assembly dictionary containing the size of the assembly, assembly parts, and volumes of the reagents unique to the assembly
assembly_dictionary = {}
for i in assemblies:
    part_volume_sum = 0
    for j in i[2:]:
        count = 0
        for q in part_dictionary:
            if j == q.split(".", 1)[0]:
                count += 1
                volume = part_dictionary[q][0]
        if count == 1:
            part_volume_sum += round(volume, 3)
        else:
            part_volume_sum += round(volume, 3)
    part_volume_sum = round(part_volume_sum, 3)
    bsai, water = _calcreagents(int(i[1]), part_volume_sum)
    assembly_dictionary[i[0]] = [i[1], i[2:], 2, 0.5, bsai, water]

# Making reagent dictionary containing the total volume needed for all the assemblies *1.2
reagents = ["ligase_buffer", "ligase", "bsai", "water"]
reagent_total = dict.fromkeys(reagents, 0.0)
reagent_dictionary = {}
many_wells_reagents = {}
for i in assembly_dictionary:
    reagent_total["ligase_buffer"] += assembly_dictionary[i][2]
    reagent_total["ligase"] += assembly_dictionary[i][3]
    reagent_total["bsai"] += assembly_dictionary[i][4]
    reagent_total["water"] += assembly_dictionary[i][5]
for i in reagent_total:
    reagent_total[i] = round(reagent_total[i] * 1.2, 3)
    #############
    #############
    # if i =='bsai': reagent_total[i] = 1700
    #############
    #############
    plate, wellvolume, count = _volumecheck(i, reagent_total[i])

    for q in range(len(plate)):
        reagent_dictionary[plate[q]] = round(wellvolume[q], 3)

# the number of wells needed for the parts and the reagents need to be less than 96
if (len(part_dictionary) + len(reagent_total) > 96) == True:
    print(
        f"The sum of the parts and reagents wells needed {len(part_dictionary)+len(reagent_total)}is greater than 96. The parts and reagents will not fit in the 96-well plate. Reduce the number of assemblies."
    )
    sys.exit(1)
else:
    # creates a dictionary that allocates a well to the reagents and parts
    plate_dictionary = _plate_dictionary_creator(reagent_dictionary, part_dictionary)

header = [
    [
        "assembly name",
        "assembly size",
        "parts",
        "ligase buffer",
        "DNA ligase",
        "bsai",
        "water",
    ],
    ["part name", "volume with 30fmol", "sum*1.2"],
    ["reagent", "sum*1.2"],
    ["position", "solution", "well volume"],
]

try:
    os.mkdir("metclo_plan_files")
except:
    pass

doc = [
    "metclo_plan_files/assembly_data.csv",
    "metclo_plan_files/part_data.csv",
    "metclo_plan_files/reagents_data.csv",
    "metclo_plan_files/position_data.csv",
]
data = (assembly_dictionary, part_dictionary, reagent_dictionary, plate_dictionary)

# makes the .csv input for the opentrons protocol
for i in range(len(header)):
    _makecvs(doc[i], header[i], data[i])


# class PDF(FPDF):
#     def header(self):
#         self.set_font("helvetica", "B", 20)
#         self.cell(
#             0,
#             10,
#             "Automated MetClo Assembly Plan",
#             border=False,
#             new_x=XPos.LMARGIN,
#             new_y=YPos.NEXT,
#             align="C",
#         )
#         self.ln(10)

#     def footer(self):
#         self.set_y(-15)
#         self.set_font("helvetica", "I", 10)
#         self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


# def __PDFtitle__(title):
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("helvetica", "BU", 16)
#     pdf.cell(0, 10, title, border=False, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
#     pdf.set_font("helvetica", "B", 12)


# def __PDFsubtitle__(title):
#     pdf.add_page()
#     pdf.set_font("helvetica", "B", 12)
#     pdf.cell(0, 10, title, border=False, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


# def __PDFassembly__(i):
#     w4 = (pdf.w) / 4.4
#     pdf.set_font("helvetica", "B", 14)
#     pdf.cell(
#         w4, 8, f"Assembly Name: {i}", border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT
#     )
#     pdf.set_font("helvetica", "", 12)
#     pdf.cell(
#         w4,
#         6,
#         f'Assembly Size: {str("{:,}".format(int(assembly_dictionary[i][0])))}',
#         border=0,
#         new_x=XPos.RIGHT,
#     )
#     if int(assembly_dictionary[i][0]) > 10000:
#         protocol = "Electroporation"
#     else:
#         protocol = "Heat Shock"
#     pdf.cell(
#         w4, 6, f"(Recomend: {protocol})", border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT
#     )
#     pdf.set_font("helvetica", "B", 12)
#     pdf.cell(
#         0,
#         6,
#         f"{len(assembly_dictionary[i][1])} Parts",
#         border=False,
#         new_x=XPos.LMARGIN,
#         new_y=YPos.NEXT,
#     )
#     pdf.set_font("helvetica", "", 12)
#     count = 0
#     for j in assembly_dictionary[i][1]:
#         if count < 3:
#             pdf.cell(w4, 6, j, border=True, new_x=XPos.RIGHT)
#             count += 1
#         else:
#             pdf.cell(w4, 6, j, border=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
#             count = 0
#     if len(assembly_dictionary[i][1]) != 4:
#         pdf.cell(0, 5, "", border=False, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
#     pdf.set_font("helvetica", "B", 12)
#     pdf.cell(0, 8, "Reagents (ul)", border=False, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
#     pdf.set_font("helvetica", "", 12)
#     for x in reagent_total:
#         pdf.cell(w4, 6, x, border=True, new_x=XPos.RIGHT)
#     pdf.cell(0, 6, "", border=False, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
#     for j in assembly_dictionary[i][-4:]:
#         pdf.cell(w4, 6, str(j), border=True, new_x=XPos.RIGHT)
#     pdf.cell(0, 12, "", border=False, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


# def __PDFparts__(part_dictionary, parts_concentration_size, part_count):
#     w5 = (pdf.w) / 6.6
#     pdf.cell(w5 + 10, 10, "Part Name", border=1, new_x=XPos.RIGHT)
#     pdf.cell(w5 - 10, 10, "Size", border=1, new_x=XPos.RIGHT)
#     pdf.cell(w5 - 10, 10, "Conc.", border=1, new_x=XPos.RIGHT)
#     pdf.cell(w5, 10, "Times Used", border=1, new_x=XPos.RIGHT)
#     pdf.cell(w5 + 5, 10, "30fmol (ul)", border=1, new_x=XPos.RIGHT)
#     pdf.cell(w5 + 5, 10, "Total Volume", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
#     count = 0
#     pdf.set_font("helvetica", "", 12)
#     for i in part_count:
#         pdf.cell(w5 + 10, 10, i, border=1, new_x=XPos.RIGHT)
#         for j in parts_concentration_size:
#             if i == j[0]:
#                 pdf.cell(w5 - 10, 10, j[2], border=1, new_x=XPos.RIGHT)
#                 pdf.cell(w5 - 10, 10, j[1], border=1, new_x=XPos.RIGHT)
#                 pdf.cell(w5, 10, str(part_count[i]), border=1, new_x=XPos.RIGHT)
#                 if i in many_wells_parts:
#                     pdf.cell(
#                         w5 + 5,
#                         10,
#                         str(many_wells_parts[i][1]),
#                         border=1,
#                         new_x=XPos.RIGHT,
#                     )
#                     pdf.cell(
#                         w5 + 5,
#                         10,
#                         str(many_wells_parts[i][2]),
#                         border=1,
#                         new_x=XPos.LMARGIN,
#                         new_y=YPos.NEXT,
#                     )
#                 else:
#                     pdf.cell(
#                         w5 + 5,
#                         10,
#                         str(part_dictionary[i][0]),
#                         border=1,
#                         new_x=XPos.RIGHT,
#                     )
#                     pdf.cell(
#                         w5 + 5,
#                         10,
#                         str(part_dictionary[i][1]),
#                         border=1,
#                         new_x=XPos.LMARGIN,
#                         new_y=YPos.NEXT,
#                     )


# def __PDFreagents__(reagent_total):
#     w4 = (pdf.w) / 4.4
#     for i in reagent_total:
#         pdf.cell(w4, 8, i, border=True, new_x=XPos.RIGHT)
#     pdf.ln(8)
#     for i in reagent_total:
#         pdf.cell(w4, 8, str(reagent_total[i]), border=True, new_x=XPos.RIGHT)


# def __PDFreagent_partplate__(plate_dictionary):
#     w4 = (pdf.w) / 4.4
#     count = 0
#     pdf.set_font("helvetica", "", 8)
#     for i in plate_dictionary:
#         if (
#             list(i)[0] == "A"
#             or list(i)[0] == "B"
#             or list(i)[0] == "C"
#             or list(i)[0] == "D"
#         ):
#             if count < 3:
#                 pdf.cell(
#                     w4,
#                     6,
#                     i + "  " + str(plate_dictionary[i]),
#                     border=True,
#                     new_x=XPos.RIGHT,
#                 )
#                 count += 1
#             else:
#                 pdf.cell(
#                     w4,
#                     6,
#                     i + "  " + str(plate_dictionary[i]),
#                     border=True,
#                     new_x=XPos.LMARGIN,
#                     new_y=YPos.NEXT,
#                 )
#                 count = 0
#     pdf.cell(0, 10, "", border=False, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
#     for i in plate_dictionary:
#         if (
#             list(i)[0] == "E"
#             or list(i)[0] == "F"
#             or list(i)[0] == "G"
#             or list(i)[0] == "H"
#         ):
#             if count < 3:
#                 pdf.cell(
#                     w4,
#                     6,
#                     i + "  " + str(plate_dictionary[i]),
#                     border=True,
#                     new_x=XPos.RIGHT,
#                 )
#                 count += 1
#             else:
#                 pdf.cell(
#                     w4,
#                     6,
#                     i + "  " + str(plate_dictionary[i]),
#                     border=True,
#                     new_x=XPos.LMARGIN,
#                     new_y=YPos.NEXT,
#                 )
#                 count = 0


# def __PDFtmcplate__(assembly_dictionary):
#     plate_dictionary = {}
#     alpha = list(string.ascii_uppercase)[:8]
#     keysList = list(assembly_dictionary.keys())
#     count = 0
#     for j in range(12):
#         for i in range(8):
#             plate_dictionary[alpha[i] + str(j + 1)] = ""
#     for i in plate_dictionary:
#         if count < len(keysList):
#             plate_dictionary[i] = keysList[count]
#             count += 1
#     count = 0
#     w4 = (pdf.w) / 4.4
#     pdf.set_font("helvetica", "", 8)
#     for i in plate_dictionary:
#         if (
#             list(i)[0] == "A"
#             or list(i)[0] == "B"
#             or list(i)[0] == "C"
#             or list(i)[0] == "D"
#         ):
#             if count < 3:
#                 pdf.cell(
#                     w4, 6, i + "  " + plate_dictionary[i], border=True, new_x=XPos.RIGHT
#                 )
#                 count += 1
#             else:
#                 pdf.cell(
#                     w4,
#                     6,
#                     i + "  " + plate_dictionary[i],
#                     border=True,
#                     new_x=XPos.LMARGIN,
#                     new_y=YPos.NEXT,
#                 )
#                 count = 0
#     pdf.cell(0, 10, "", border=False, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
#     for i in plate_dictionary:
#         if (
#             list(i)[0] == "E"
#             or list(i)[0] == "F"
#             or list(i)[0] == "G"
#             or list(i)[0] == "H"
#         ):
#             if count < 3:
#                 pdf.cell(
#                     w4, 6, i + "  " + plate_dictionary[i], border=True, new_x=XPos.RIGHT
#                 )
#                 count += 1
#             else:
#                 pdf.cell(
#                     w4,
#                     6,
#                     i + "  " + plate_dictionary[i],
#                     border=True,
#                     new_x=XPos.LMARGIN,
#                     new_y=YPos.NEXT,
#                 )
#                 count = 0


# pdf = PDF("P", "mm", "Letter")
# __PDFtitle__(f"OT2 Set-Up Instructions")
# pdf.set_font("helvetica", "", 10)
# with open("doc/ins.txt", "r") as f:
#     for i in f:
#         pdf.multi_cell(0, 3, i)

# __PDFsubtitle__("OT2 Layout")
# pdf.image("doc/OT2bench.JPG", 45, 50, 150)
# __PDFsubtitle__("Reagent Plate Layout (ul)")
# __PDFreagent_partplate__(plate_dictionary)
# __PDFsubtitle__("Thermocycler Plate with Assemblies")
# __PDFtmcplate__(assembly_dictionary)
# __PDFtitle__(f"{str(len(assembly_dictionary))} Assemblies")
# for i in assembly_dictionary:
#     __PDFassembly__(i)
# __PDFtitle__(f"{str(len(part_dictionary))} Parts")
# __PDFparts__(part_dictionary, parts_concentration_size, part_count)
# __PDFtitle__(f"Total Reagents Volumes Required (ul) *1.2")
# __PDFreagents__(reagent_total)

# try:
#     pdf.output("metclo_plan_files/metclo_plan.pdf")
#     print("metclo_plan.pdf written succesfully.")
# except:
#     print("metclo_plan.pdf not written")
#     sys.exit(1)

