# MetCloOT2 : Automated MetClo assembly on Opentron OT2 liquid handeling robot

The University of Edinburgh - MSc Synthetic Biology and Biotechnology Dissertation

by Daniella Matute 

# H1 About MetCloOT2

Welcome to MetCloOT2. This program is designed to accept information about metclo based assemblies and design a custom Opentron protocol capable of being run on OpenTrons' OT2 liquid handeling machine

# H1 How too.
1. Prior to using  MetCloOT2, assure the quality of the assembly and simulate the assembly using computational tools, such as those found in the EGF's Cuba suite. 
2. Create 2 .csv files, one containing informations of the assemblies and the other infomration about the parts. *Under /example 2 files are provided depicting the layout of the .csv files.* The assembly file, will look very similar to the assembly plan used in [Simulate Golden Gate Assemblies](https://cuba.genomefoundry.org/simulate_gg_assemblies) with the exception that a assembly size columb in added. 
3. Clone this MetcloOT2 repository from GitHub
4. Run the metclo_plan.py file and follow the instructions that appear in the terminal. 
5. The the protocol will generate 4 files:
- metclo_plant.pdf
- assembly_data.csv
- part_data.csv
- position_data.csv

![image](https://user-images.githubusercontent.com/101208454/172651289-0fbeaba1-21f0-4c2b-bf4f-d792a6ca38dc.png)

p# -plasmids with part

V- Assrembly vector that will accept the parts

Assembly - tube where the assembly will occure
