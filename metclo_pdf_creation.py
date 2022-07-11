from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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

if __name__ == '__main__':
    form('metclo_plan.pdf')