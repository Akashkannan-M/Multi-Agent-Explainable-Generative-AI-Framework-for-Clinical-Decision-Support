from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class ReportAgent:

    def generate_report(
        self,
        name,
        age,
        gender,
        disease,
        confidence,
        recommendations,
        image_result
    ):

        file_name = f"{name}_Report.pdf"

        document = SimpleDocTemplate(file_name)

        styles = getSampleStyleSheet()

        story = []

        story.append(Paragraph("<b>Clinical Decision Support Report</b>", styles["Title"]))

        story.append(Paragraph(f"<b>Patient Name:</b> {name}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Age:</b> {age}", styles["BodyText"]))
        story.append(Paragraph(f"<b>Gender:</b> {gender}", styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph(f"<b>Predicted Disease:</b> {disease}", styles["BodyText"]))

        story.append(Paragraph(f"<b>Confidence Score:</b> {confidence}%", styles["BodyText"]))

        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(Paragraph("<b>Recommendations</b>", styles["Heading2"]))

        for item in recommendations:
            story.append(
                Paragraph(f"• {item}", styles["BodyText"])
            )
        
        story.append(Paragraph("<br/>", styles["BodyText"]))

        story.append(
            Paragraph(
                "<b>Medical Image Analysis</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(image_result, styles["BodyText"])
        )
        
        document.build(story)

        return file_name