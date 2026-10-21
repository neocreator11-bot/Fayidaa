from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def create_development_receipt(reference: str = "NOT-VERIFIED") -> BytesIO:
    """Create a clearly marked development sample; never represents Fayda verification."""
    output = BytesIO()
    pdf = canvas.Canvas(output, pagesize=A4)
    width, height = A4
    pdf.setTitle("Development Sample - Not a Fayda Verification")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(25 * mm, height - 30 * mm, "Development Sample Receipt")
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(25 * mm, height - 48 * mm, "NOT A FAYDA VERIFICATION")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(25 * mm, height - 62 * mm, f"Reference: {reference}")
    pdf.drawString(25 * mm, height - 72 * mm, "No identity authentication was performed.")
    pdf.drawString(25 * mm, height - 82 * mm, "This sample must not be used as an official identity document.")
    pdf.showPage()
    pdf.save()
    output.seek(0)
    return output
