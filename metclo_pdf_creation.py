from fpdf import FPDF
from fpdf.enums import XPos, YPos

class PDF(FPDF):
    def header(self):
        #logo
        self.image('96well.jpg', 10,8,25)
        #font
        self.set_font('helvetica','B',20)
        #title
        self.cell(0,10,'Automated MetClo Assembply Plan',border = False,new_x=XPos.LMARGIN,new_y=YPos.NEXT, align='C' )
        #linebreak
        self.ln(20)
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica','I',10)
        self.cell(0,10,f'Page {self.page_no()}/{{nb}}', align ='C')
# create FPDF object
#Layout('P','L')
#unit
#format
pdf = PDF('P','mm','Letter')
pdf.set_auto_page_break(auto =True, margin =15)

#Add a page
pdf.add_page()

pdf.set_font('helvetica', 'BU', 16)
#add text cell or multicell
#(width, height)
for i in range(1,41):
    pdf.cell(0,10,f'This is line {i}:D', border =True, align = 'C')
    pdf.cell(0,10,f'This is line {i}:D' ,new_x=XPos.LMARGIN,new_y=YPos.NEXT, border =True)

pdf.output('pdf_1.pdf')
