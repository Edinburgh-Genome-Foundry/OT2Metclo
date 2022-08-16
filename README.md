# MetCloOT2: Automated MetClo assembly on OpenTrons OT-2 liquid handling robot

## About MetCloOT2

Welcome to MetCloOT2. The purpose of this repository is to enable the automation of MetClo based assemblies within the Opentrons OT2 liquid handling robot. The program is based on [Lin & O’Callaghan (2018)](https://doi.org/10.1093/nar/gky596) and [Lin & O'Callaghan (2020)](http://link.springer.com/10.1007/978-1-0716-0908-8_9). Reading these two papers prior to OT2Metclo implementation is highly recommended.

This repository is part of a dissertation project necessary to fulfil the requirements of the MSc Synthetic Biology and Biotechnology programme at the University of Edinburgh.

## How to

1. Prior to using MetCloOT2, assure the quality of the assembly by means of computer aided designs and simulations, such tool can be found at the [EGF's Cuba suite](https://cuba.genomefoundry.org/home) or at [Edinburgh Genome Foundry’s]( https://github.com/Edinburgh-Genome-Foundry) GitHub page.
2. Create 2 input .csv files, one containing information of the assemblies, and the other information about the part plasmids and assembly vector. Within the *example/* folder there are two sample files depicting the expected layout of the .csv files.
If [Simulate Golden Gate Assemblies](https://cuba.genomefoundry.org/simulate_gg_assemblies) was used to simulate the assemblies (as recommended in step 1), the assembly plan can be used as the assembly.csv in MetCloOT2 with a slight modification. OT2Metclo requires an assembly-size column to be added to the assembly plan.
3. Assure that the volume of 30fmol of all part plasmids and assembly vectors is at least 1μl.
    Use the following formula:
    <p align="center">
    <img src="doc/formula.JPG" alt="drawing" width="350" align="center" class="center">
    </p>
    Or copy this formula into excel:

    *=round((18530.7 * [part length (bp)]  + 1081.2) / ( [part concentration (ng/ul)] * 10^6) ,3)*

    If the volume is lower than 1μl, then dilute the plasmid. If the volume is equal to or greater than 1μl, no dilution is necessary.

4. Install or check for the presence of the following packages: csv, math, string, sys, fpdf, opentrons, string and sys.
Confirm that Python 3 is installed.
Confirm that OT2 APP is downloaded and UpToDate.

5. Clone this MetcloOT2 repository from GitHub.

6. Open the terminal, navigate to the location of the cloned repository. Run **metclo_plan.py** by typing `python metclo_plan.py` in the terminal. Follow the instructions that appear in the terminal.

7. The protocol will generate 5 files:

    - metclo_plan.pdf
    - assembly_data.csv
    - part_data.csv
    - position_data.csv
    - reagents_data.csv

8. Read and confirm the assembly and part information in **`metclo_plan.pdf`**.
9. Follow the instructions found in `metclo_plan.pdf`.

### Supervisor

[Peter Vegh](https://github.com/veghp)

### Author

[Daniella Matute](https://github.com/DanyMatute)
