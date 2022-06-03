'''Input your assembly plan in an excel format, checks file. It makes a plan for the OT2 labware set-up specifically for this assembly 
and provides it to the user. The user then can populate the OT2 labware with the appropriate solutions. The OT2 labware plan is then provided 
to the the OT2 protocol. 
INPUT: excel document with insert and assembly vector 
(1) size of each plasmid
(2) miniprep ug/ul contration of each plasmid 
(3) final assembly size
PROCESS:
(1) check file 
(2) retraive data from file
(3) calculate valumes needed for the assembly from the data
(4) make a labware plan allocating position and quantity of the solutions for user and OT2 protocol
'''
