from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
import os, tempfile
from datetime import datetime


def _f(v):
    try:
        return float(v)
    except:
        return 0.0


def _fmt(v):
    try:
        return f"{float(v):.2f}"
    except:
        return str(v or "")


def _logo_path():
    return os.path.join(os.path.dirname(__file__), "static", "logo.png")


# HEADER FOR PAGE 1 --------------------------------------------------------------------------------
def draw_header_page1(canvas, doc, title_text):
    w, h = A4
    canvas.setFillColor(colors.white)
    canvas.rect(0, h - 130, w, 130, stroke=0, fill=1)

    logo = _logo_path()
    if os.path.exists(logo):
        try:
            logo_h = 45
            logo_w = logo_h * 2.5
            canvas.drawImage(
                logo,
                (w - logo_w) / 2,
                h - 120,
                width=logo_w,
                height=logo_h,
                preserveAspectRatio=True,
                mask="auto",
            )
        except:
            pass

    canvas.setFont("Helvetica-Bold", 16)
    canvas.setFillColor(colors.black)
    canvas.drawCentredString(w / 2, h - 140, title_text)

    canvas.setFont("Helvetica-Oblique", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(w / 2, 30, "Thank you for booking with us!")


# FOOTER + SIGNATURES PAGE 2 -----------------------------------------------------------------------
def draw_footer_and_signatures_page2(canvas, doc):
    w, h = A4
    y = 90  # signature position

    canvas.line(60, y, 240, y)
    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(150, y - 14, "Customer Signature")

    canvas.line(w - 240, y, w - 60, y)
    canvas.drawCentredString(w - 150, y - 14, "Hotel Management Signature")

    footer = (
        "AA Residency A/C | Contact: 8790057559 | "
        "22-11-246/1, Gollavani Gunta, Renigunta Rd, AutoNagar, "
        "Tirupati, Andhra Pradesh 517501"
    )
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(w / 2, 35, footer)


# MAIN GENERATOR -----------------------------------------------------------------------------------
def generate_bill(data):

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    filepath = tmp.name
    tmp.close()

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=170,
        bottomMargin=100,
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    normal.fontSize = 10
    normal.leading = 14

    header_style = ParagraphStyle(
        "SectionHeader",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=12,
        spaceAfter=4,
        spaceBefore=8,
    )

    story = []

    advance_amt = _f(data.get("advance"))
    advance_mode = data.get("advance_mode") or ""  # FIXED

    title_text = (
        "Function Hall Booking Details"
        if advance_amt > 0
        else "Function Hall Booking Quotation"
    )

    now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    timestamp = (
        f"Booking confirmed on: {now}"
        if advance_amt > 0
        else f"Booking inquiry made on: {now}"
    )

    story.append(
        Paragraph(
            f'<para alignment="right"><font size=9>{timestamp}</font></para>',
            normal,
        )
    )
    story.append(Spacer(1, 4))

    # ---------------- Guest Details ------------------------------------------------------
    story.append(Paragraph("Guest Details:", header_style))

    guest_table_data = [
        ["Field", "Details"],
        ["Name", data.get("name") or ""],
        ["Pax", data.get("pax") or ""],
        ["Mobile", data.get("mobile") or ""],
        ["Event Type", data.get("event_type") or ""],
        ["Function Check-in", data.get("checkin") or ""],
        ["Function Check-out", data.get("checkout") or ""],
    ]

    guest_tbl = Table(
        guest_table_data,
        colWidths=[doc.width * 0.30, doc.width * 0.70],
    )

    guest_tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9f0ff")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0b5ed7")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, 0), "LEFT"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                ("ALIGN", (0, 1), (1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    story.append(guest_tbl)
    story.append(Spacer(1, 8))

    # ---------------- Room Details -------------------------------------------------------
    story.append(Paragraph("Room Details:", header_style))

    room_data = [
        ["Room Type", "No. of Rooms", "Extra Bed/Room", "AC/Non-AC", "Rent (Per Room)"],
        [
            "Double",
            data.get("double_rooms") or "",
            data.get("double_extra") or "",
            data.get("double_ac") or "",
            _fmt(data.get("double_rent")),
        ],
        [
            "Triple",
            data.get("triple_rooms") or "",
            data.get("triple_extra_bed") or "",
            data.get("triple_ac") or "",
            _fmt(data.get("triple_rent_per_room")),
        ],
    ]

    room_tbl = Table(
        room_data,
        colWidths=[
            doc.width * 0.25,
            doc.width * 0.18,
            doc.width * 0.18,
            doc.width * 0.19,
            doc.width * 0.20,
        ],
    )

    room_tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9f0ff")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0b5ed7")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]
        )
    )

    story.append(room_tbl)
    story.append(Spacer(1, 8))

    # ---------------- Payment Summary -------------------------------------------------------
    story.append(Paragraph("Payment Summary:", header_style))

    room_needed = data.get("room_needed") == "on"

    d_r = _f(data.get("double_rent"))
    d_n = _f(data.get("double_rooms"))
    t_r = _f(data.get("triple_rent_per_room"))
    t_n = _f(data.get("triple_rooms"))

    room_total = (d_r * d_n) + (t_r * t_n) if room_needed else 0
    f_rent = _f(data.get("function_rent"))
    clean = _f(data.get("cleaning_charges"))
    sec = _f(data.get("security_charges"))
    elec = _f(data.get("electricity_charges"))

    try:
        dt1 = datetime.strptime(data.get("checkin"), "%Y-%m-%dT%H:%M")
        dt2 = datetime.strptime(data.get("checkout"), "%Y-%m-%dT%H:%M")
        days = max(1, (dt2 - dt1).days)
    except:
        days = 1

    per_day_total = room_total + f_rent + clean + sec + elec
    total_rent = per_day_total * days
    balance = total_rent - advance_amt

    pay_data = [
        ["Description", "Value"],
        ["Room Rent (per day)", _fmt(room_total)],
        ["Function Hall Rent (per day)", _fmt(f_rent)],
        ["Cleaning (per day)", _fmt(clean)],
        ["Security (per day)", _fmt(sec)],
        ["Electricity (per day)", _fmt(elec)],
        ["Number of Days", str(days)],
        ["Total Rent", _fmt(total_rent)],
    ]

    if advance_amt > 0:
        pay_data.append(["Advance Paid", _fmt(advance_amt)])
        pay_data.append(["Advance Payment Mode", data.get("advance_mode", "")])  # FIXED
        pay_data.append(["Balance", _fmt(balance)])
    else:
        pay_data.append(["Balance", _fmt(total_rent)])

    pay_tbl = Table(
        pay_data,
        colWidths=[doc.width * 0.65, doc.width * 0.35],
    )

    pay_tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f6ff")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0b5ed7")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (0, 1), (-1, -1), "LEFT"),
            ]
        )
    )

    story.append(pay_tbl)
    story.append(Spacer(1, 8))

    # ---------------- Remarks -------------------------------------------------------------
    remarks = data.get("remarks") or ""
    if remarks.strip():
        story.append(Paragraph("Remarks:", header_style))
        for line in remarks.splitlines():
            story.append(Paragraph(line, normal))

    # ---------------- PAGE 2 -------------------------------------------------------------
    story.append(PageBreak())
    story.append(Spacer(1, 4))
    story.append(Paragraph("Important Terms & Conditions:", header_style))

    if advance_amt > 0:
        terms = [
            "1. Event date once booked cannot be changed; advance amount paid is non-refundable.",
            "2. Management is not responsible for loss or damage to guests’ personal belongings.",
            "3. The function hall will be handed over 4 hours before the scheduled event time.",
            "4. Guests will be held responsible for any damage or missing items belonging to the hall.",
            "5. Power-backup charges (2,500 per hour) apply only if the generator is used.",
            "6. Balance must be paid as soon as the event concludes.",
            "7. Electricity meter reading starts when the hall is given to the decoration team.",
            "8. Live cooking counter is not allowed inside the hall.",
        ]
    else:
        terms = [
            "1. Quotation valid for 7 days only. Booking confirmed only after advance payment.",
            "2. Event date once booked cannot be changed; advance amount is non-refundable.",
            "3. Management is not responsible for loss or damage to guests’ personal belongings.",
            "4. The function hall will be handed over 4 hours before the scheduled event time.",
            "5. Guests are responsible for any damage or missing items belonging to the hall.",
            "6. Power-backup charges (2,500 per hour) apply only if the generator is used.",
            "7. Balance must be paid as soon as the event concludes.",
            "8. Electricity meter reading starts when the hall is given to the decoration team.",
            "9. Live cooking counter is not allowed inside the hall.",
        ]

    for t in terms:
        story.append(Paragraph(t, normal))

    # BUILD PDF -------------------------------------------------------
    def on_first(canvas, doc):
        draw_header_page1(canvas, doc, title_text)

    def on_later(canvas, doc):
        draw_footer_and_signatures_page2(canvas, doc)

    doc.build(story, onFirstPage=on_first, onLaterPages=on_later)

    return filepath
