from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

BRAND_COLOR = colors.HexColor("#4F46E5")     

styles = getSampleStyleSheet()
body = styles["BodyText"]
title_style = ParagraphStyle("BrandTitle", parent=styles["Title"], textColor=BRAND_COLOR)
heading = ParagraphStyle("BrandHeading", parent=styles["Heading2"], textColor=BRAND_COLOR)
header_cell = ParagraphStyle("HeaderCell", parent=body, textColor=colors.white)


def to_json(result) -> str:
    
    return result.model_dump_json(indent=2)


def make_table(header, rows, widths):
    data = [[Paragraph(f"<b>{h}</b>", header_cell) for h in header]]
    for row in rows:
        data.append([Paragraph(escape(str(cell or "-")), body) for cell in row])

    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLOR),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return table


def add_section(story, name, header, rows, widths):
    story.append(Paragraph(name, heading))
    if rows:
        story.append(make_table(header, rows, widths))
    else:
        story.append(Paragraph("None found.", body))


def create_pdf(result, usage=None) -> bytes:
   
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=2 * cm,
                            rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm)

    story = [
        Paragraph("DocuSummarizer", title_style),
        Paragraph("AI Meeting Intelligence Report", body),
        Spacer(1, 12),
        Paragraph("Executive Summary", heading),
        Paragraph(escape(result.summary), body),
    ]

    add_section(story, "Key Decisions", ["Decision", "Made by"],
                [[d.decision, d.made_by] for d in result.decisions], [11 * cm, 6 * cm])

    add_section(story, "Action Items", ["Task", "Owner", "Deadline"],
                [[a.task, a.owner, a.deadline] for a in result.action_items],
                [8 * cm, 4.5 * cm, 4.5 * cm])

    add_section(story, "Risks", ["Risk", "Severity"],
                [[r.risk, r.severity] for r in result.risks], [13 * cm, 4 * cm])

    story.append(Paragraph("Topics", heading))
    for topic in result.topics:
        story.append(Paragraph(f"<b>{escape(topic.name)}</b>", body))
        for point in topic.points:
            story.append(Paragraph("• " + escape(point), body))

    if usage:
        story.append(Spacer(1, 12))
        story.append(Paragraph(
            f"Tokens used: {usage['input_tokens'] + usage['output_tokens']} | "
            f"Estimated cost: ${usage['estimated_cost_usd']}", body))

    doc.build(story)
    return buffer.getvalue()