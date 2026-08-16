from fpdf import FPDF
from fpdf.enums import Align


def main():
    name = input("Name: ")
    create_pdf(name)

def create_pdf(name):
    pdf = FPDF(orientation="P", unit = "mm", format="A4")
    pdf.add_page()
    pdf.set_font('Times', style='B', size=32)
    pdf.cell(w = 0, h = 60, text = "CS50 Shirtificate",align="C")

    pdf.image("https://cs50.harvard.edu/python/2022/psets/8/shirtificate/shirtificate.png", x=Align.C, y=80, w=180)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(10, 120)
    pdf.set_font('Times', style='B', size=32)
    pdf.cell(w = 0, h = 20, text = f"{name} took CS50", align="C")
    pdf.output("shirtificate.pdf")
    pdf.set_auto_page_break(False, 2)



if __name__ == "__main__":
    main()



