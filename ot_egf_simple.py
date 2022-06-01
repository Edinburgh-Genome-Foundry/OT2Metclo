import json

from opentrons import protocol_api


def get_values(*names):
    _all_values = json.loads(
        """{
        "p20":"p20_single_gen2",
        "p20_mount":"right",
        "p300_single_gen2":"p300_single_gen2",
        "p300_mount":"left",
        "destination_plate":"thermo_96_well",
        "source_plate":"usascientific_12_reservoir_22ml"}
        """
    )
    return [_all_values[n] for n in names]

print('test to push to github')
# metadata
metadata = {
    "protocolName": "EGF base protocol",
    "author": "Peter Vegh <egf-software@ed.ac.uk>",
    "description": "Simple protocol to get started using the OT-2",
}


def run(protocol: protocol_api.ProtocolContext):
    pip_model, pip_mount, destination_plate, source_plate = get_values(  # noqa: F821
        "pip_model", "pip_mount", "destination_plate", "source_plate"
    )

    # SETUP
    # Load a Temperature Module GEN1 in deck slot.
    temperature_module = protocol.load_module("temperature module", 1)
    # Load a Magnetic Module GEN2 in deck slot.
    magnetic_module = protocol.load_module("magnetic module gen2", 4)
    # Thermocycler module:
    tc_mod = protocol.load_module("thermocycler module")

    # LABWARE
    tiprack = protocol.load_labware("opentrons_96_tiprack_300ul", location="2")
    source_plate = protocol.load_labware(source_plate, location="3")
    destination_plate = protocol.load_labware(destination_plate, location="6")

    p300 = protocol.load_instrument(p300_single_gen2, p300_mount, tip_racks=[tiprack])

    # OPERATIONS
    tc_mod.open_lid()
    tc_mod.close_lid()

    p300.pick_up_tip()
    p300.aspirate(50, source_plate["A1"])
    p300.dispense(50, destination_plate["A1"])
    p300.drop_tip()
