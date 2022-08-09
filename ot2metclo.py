import profile, string, csv, sys, math
from opentrons import protocol_api


def __openfile__(file):
    try:
        with open(file, newline="") as csvfile:
            rows = csv.reader(csvfile)
            header = next(rows)
            if header != None:
                data = []
                for j in rows:
                    data.append(j)
                return data
    except:
        print("File error.", file)
        sys.exit(1)


def __volumecheck__(i, x, count, plate):
    if x / 200 < 1:
        plate[count] = [i[0], float(i[1])]
        count += 1
    else:
        wells = math.ceil(x / 200)
        for t in range(wells):
            plate[count] = [i[0] + "." + str(t + 1), float(i[1])]

            count += 1
    return plate, count


def __makeplate__():
    plate_dictionary = {}
    alpha = list(string.ascii_uppercase)[:8]
    for j in range(12):
        for i in range(8):
            plate_dictionary[alpha[i] + str(j + 1)] = ""
    return plate_dictionary


assembly_data = __openfile__("metclo_plan_files/assembly_data.csv")
part_data = __openfile__("metclo_plan_files/part_data.csv")
reagent_data = __openfile__("metclo_plan_files/reagents_data.csv")
position_data = __openfile__("metclo_plan_files/position_data.csv")
# print('ASSEMBLY DATA\n', assembly_data)
# print('\nPART DATA\n', part_data)
# print('\nREAGENT DATA\n', reagent_data)


reagent_part_plate2 = {}
assembly_plate = {}
count = 0
for i in position_data:
    if len(i) == 3:
        reagent_part_plate2[i[1]] = [i[0], float(i[2])]
    try:
        assembly_plate[i[0]] = [assembly_data[count][0], 0]
        count += 1
    except:
        assembly_plate[i[0]] = ["", 0]

assembly_dictionary = {}
for i in assembly_data:
    parts_ = []
    for t in (i[2][1:-1]).split(","):
        t = (t.strip(" "))[1:-1]
        parts_.append(t)
    reagents_ = []
    for j in i[3:]:
        reagents_.append(float(j))
    assembly_dictionary[i[0]] = parts_, reagents_

part_dictionary = {}
for i in part_data:
    part_dictionary[i[0]] = float(i[1])


# print('ASSEMBLY_DICTIONARY' , assembly_dictionary)
# print('PART_DICTIONARY' , part_dictionary)
# print('\nREAGENT_PART_PLATE2\n',reagent_part_plate2, '\n')
# print('\nASSEMBLY_PLATE\n',assembly_plate)

reagents = ["ligase_buffer", "ligase", "bsai", "water"]


metadata = {
    "apiLevel": "2.3",
    "protocolName": "Metclo Assembly - hardcoded with one assembly that cna change in size",
    "author": "Daniella Matute <daniella.l.matute@gmail.com",
    "description": "OT-2 protocol that allows for methylase DNA assembly",
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
    tr_20 = protocol.load_labware("opentrons_96_tiprack_20ul", 9)
    part_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 6)
    tc_plate = tc_mod.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")

    # Instrument
    p_20 = protocol.load_instrument("p20_single_gen2", "left", tip_racks=[tr_20])

    ################################################################################
    # PROTOCOL
    ################################################################################
    tc_mod.set_lid_temperature(4)
    tc_mod.set_block_temperature(4)
    tc_mod.open_lid()

    for i in assembly_plate:
        if assembly_plate[i][0] != "":
            assembly_name = assembly_plate[i][0]
            parts = assembly_dictionary[assembly_name][0]
            reagent_dictionary = {}
            for j in range(len(assembly_dictionary[assembly_name][1])):
                reagent_dictionary[reagents[j]] = assembly_dictionary[assembly_name][1][
                    j
                ]
            # print('\nASSEMBLY_NAME', assembly_name)
            # print('PARTS',parts)
            # print('REAGENT_DICTIONARY', reagent_dictionary,'\n')
            for j in reagent_dictionary:
                if j in reagent_part_plate2:
                    if (
                        reagent_part_plate2[j][1] != 0
                        and reagent_part_plate2[j][1] > reagent_dictionary[j]
                    ):
                        # print('transfer', reagent_dictionary[j],j, ' from ', reagent_part_plate2[j][0],'[',reagent_part_plate2[j][1], '] to', i , 'on assembly plate' )
                        p_20.transfer(
                            reagent_dictionary[j],
                            part_plate[reagent_part_plate2[j][0]],
                            tc_plate[i],
                        )
                        reagent_part_plate2[j][1] = round(
                            reagent_part_plate2[j][1] - reagent_dictionary[j], 3
                        )

                else:
                    check = False
                    for k in reagent_part_plate2:
                        if check == False:
                            val = reagent_part_plate2[k]
                            k_ = k.split(".")[0]
                            if (
                                k_ == j
                                and val != 0
                                and check == False
                                and reagent_dictionary[k_] != 0
                                and reagent_part_plate2[k][1] > reagent_dictionary[j]
                            ):
                                # print('transfer', reagent_dictionary[j],j, ' from ', reagent_part_plate2[k][0],'[',reagent_part_plate2[k][1], '] to', i , 'on assembly plate' )
                                p_20.transfer(
                                    reagent_dictionary[j],
                                    part_plate[reagent_part_plate2[k][0]],
                                    tc_plate[i],
                                )
                                reagent_part_plate2[k][1] = round(
                                    reagent_part_plate2[k][1] - reagent_dictionary[j], 3
                                )
                                check = True
            for j in parts:
                if j in part_dictionary:
                    # print('transfer', part_dictionary[j],j, ' from ', reagent_part_plate2[j][0],'[',reagent_part_plate2[j][1], '] to', i , 'on assembly plate' )
                    p_20.transfer(
                        part_dictionary[j],
                        part_plate[reagent_part_plate2[j][0]],
                        tc_plate[i],
                    )
                    reagent_part_plate2[j][1] = round(
                        reagent_part_plate2[j][1] - part_dictionary[j], 3
                    )
                else:
                    check = False
                    for k in part_dictionary:
                        if check == False:
                            k_ = k.split(".")[0]
                            val = part_dictionary[k]
                            total = reagent_part_plate2[k][1]
                            if k_ == j and check == False and val != 0 and total > val:
                                # print('transfer', val,j, ' from ', reagent_part_plate2[k][0],'[',reagent_part_plate2[k][1], '] to', i , 'on assembly plate' )
                                p_20.transfer(
                                    val,
                                    part_plate[reagent_part_plate2[k][0]],
                                    tc_plate[i],
                                )
                                reagent_part_plate2[k][1] = round(
                                    reagent_part_plate2[k][1] - val, 3
                                )
                                check = True

    # Thermocycler
    protocol.comment("Assembly reaction ongoing")
    tc_mod.set_lid_temperature(85)
    tc_mod.set_block_temperature(37, hold_time_minutes=15, block_max_volume=20)
    tc_mod.close_lid()
    profile = [
        {"temperature": 37, "hold_time_minutes": 2},
        {"temperature": 16, "hold_time_minutes": 5},
        {"temperature": 37, "hold_time_minutes": 20},
        {"temperature": 80, "hold_time_minutes": 5},
    ]
    tc_mod.execute_profile(steps=profile, repetitions=45, block_max_volume=20)
    tc_mod.set_lid_temperature(4)
    tc_mod.set_block_temperature(4)
    protocol.comment(
        "Metclo assembly done. Assembly is incubating at 4 degrees Celsius."
    )

