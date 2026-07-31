from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class InvoiceAgent:

    def generate_invoice(
        self,
        patient_name,
        consultation_fee,
        medicine_charge,
        lab_charge,
        total_amount,
        bill_date
    ):

        file_name = f"{patient_name}_Invoice.pdf"

        document = SimpleDocTemplate(file_name)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph("<b>Hospital Invoice</b>", styles["Title"])
        )

        story.append(
            Paragraph(f"<b>Patient Name:</b> {patient_name}", styles["BodyText"])
        )

        story.append(
            Paragraph(f"<b>Bill Date:</b> {bill_date}", styles["BodyText"])
        )

        story.append(
            Paragraph("<br/>", styles["BodyText"])
        )

        story.append(
            Paragraph(f"Consultation Fee : ₹{consultation_fee:.2f}", styles["BodyText"])
        )

        story.append(
            Paragraph(f"Medicine Charge : ₹{medicine_charge:.2f}", styles["BodyText"])
        )

        story.append(
            Paragraph(f"Lab Charge : ₹{lab_charge:.2f}", styles["BodyText"])
        )

        story.append(
            Paragraph("<br/>", styles["BodyText"])
        )

        story.append(
            Paragraph(f"<b>Total Amount : ₹{total_amount:.2f}</b>", styles["Heading2"])
        )

        document.build(story)

        return file_name