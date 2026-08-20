"""Screening PDF: explanatory, clickable contents, images kept inside the page."""
from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    CondPageBreak,
    Flowable,
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "report" / "OsdagBridge_Testing_Report.pdf"
LOGO = ROOT / "report" / "assets" / "osdag_logo.png"
EVID = ROOT / "evidence"
OVERVIEW = EVID / "logs" / "test_overview.json"
SHOT = EVID / "screenshots"
GUI = SHOT / "gui_screencast"
PLOTS = SHOT / "plots"
CAD3D = SHOT / "cad_3d"
DICT = EVID / "dictionaries"
LOGS = EVID / "logs"

AUTHOR = "Harshdeep Singh"
COLLEGE = "Jaypee Institute of Information Technology (JIIT), Noida"
DEGREE = "B.Tech. Computer Science"
GITHUB = "Harshdeep-creator"

NAVY = colors.HexColor("#1f3a5f")
HEAD_BG = colors.HexColor("#d6e4f0")
HEAD_FG = colors.HexColor("#102a43")
RULE = colors.HexColor("#b0bec5")
GREEN = colors.HexColor("#558b2f")
STRIPE = colors.HexColor("#f4f7fa")
PAGE_W, PAGE_H = A4
LEFT_M = 18 * mm
RIGHT_M = 18 * mm
USABLE = PAGE_W - LEFT_M - RIGHT_M  # ~174 mm


class Dest(Flowable):
    """Named destination so Contents links and PDF bookmarks work."""

    def __init__(self, key: str, title: str, level: int = 0):
        super().__init__()
        self.key = key
        self.title = title
        self.level = level
        self.width = 0
        self.height = 1

    def draw(self):
        self.canv.bookmarkPage(self.key)
        try:
            self.canv.addOutlineEntry(self.title, self.key, self.level, closed=False)
        except Exception:
            pass


def load_json(path: Path, default=None):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default if default is not None else {}


def P(text, style):
    return Paragraph(str(text).replace("\n", "<br/>"), style)


def fitted_image(path: Path, max_w, max_h):
    """Scale by aspect ratio only. Never wider/taller than the box."""
    if not path.exists():
        return None
    try:
        img = Image(str(path))
    except Exception:
        return None
    iw = float(img.imageWidth or 1)
    ih = float(img.imageHeight or 1)
    aspect = ih / iw
    w = min(float(max_w), USABLE)
    h = w * aspect
    if h > float(max_h):
        h = float(max_h)
        w = h / aspect
    if w > USABLE:
        w = USABLE
        h = w * aspect
        if h > float(max_h):
            h = float(max_h)
            w = h / aspect
    img.drawWidth = w
    img.drawHeight = h
    img.hAlign = "CENTER"
    return img


def styled_table(data, col_widths, head_style, cell_style=None):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.hAlign = "LEFT"
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
                ("TEXTCOLOR", (0, 0), (-1, 0), HEAD_FG),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.4, RULE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, STRIPE]),
            ]
        )
    )
    return t


def header_footer(canvas, doc):
    if doc.page == 1:
        return
    canvas.saveState()
    canvas.setStrokeColor(GREEN)
    canvas.setLineWidth(1.0)
    canvas.line(LEFT_M, PAGE_H - 12 * mm, PAGE_W - RIGHT_M, PAGE_H - 12 * mm)
    canvas.setFont("Times-Roman", 8)
    canvas.setFillColor(NAVY)
    canvas.drawString(LEFT_M, PAGE_H - 10 * mm, "OsdagBridge short-span steel girder - testing report")
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.4)
    canvas.line(LEFT_M, 12 * mm, PAGE_W - RIGHT_M, 12 * mm)
    canvas.setFillColor(colors.HexColor("#455a64"))
    canvas.drawString(LEFT_M, 7 * mm, AUTHOR)
    canvas.drawRightString(PAGE_W - RIGHT_M, 7 * mm, f"Page {doc.page - 1}")
    canvas.restoreState()


def h2(story, styles, key, title):
    story.append(CondPageBreak(36 * mm))
    story.append(Dest(key, title, 0))
    story.append(P(f'<a name="{key}"/>{title}', styles["H2c"]))


def h3(story, styles, title):
    story.append(P(title, styles["H3c"]))


def figure_one(styles, path: Path, caption: str, max_h=2.45 * inch):
    img = fitted_image(path, USABLE, max_h)
    if not img:
        return None
    cap = P(caption, styles["FigCap"])
    block = Table([[img], [cap]], colWidths=[USABLE])
    block.hAlign = "CENTER"
    block.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, 0), 2),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
            ]
        )
    )
    return KeepTogether([block])


def compact_compare(story, styles, fname, caption, keys=None):
    rows = load_json(DICT / fname, [])
    if not rows:
        return
    if keys:
        rows = [r for r in rows if r.get("key") in keys]
    head = [
        P("<b>Key</b>", styles["CellHead"]),
        P("<b>I entered</b>", styles["CellHead"]),
        P("<b>Input dict</b>", styles["CellHead"]),
        P("<b>Output dict</b>", styles["CellHead"]),
        P("<b>Match</b>", styles["CellHead"]),
    ]
    table = [head]
    for r in rows:
        inn, out = r.get("input_matches_ui"), r.get("output_matches_ui")
        if inn and out:
            match = "Yes"
        elif inn and out is None:
            match = "Input only"
        elif inn is False:
            match = "No"
        else:
            match = "-"
        ov = r.get("output_dict")
        table.append(
            [
                P(f"<font face='Courier' size='7'>{r.get('key')}</font>", styles["Cell"]),
                P(str(r.get("planned_ui")), styles["Cell"]),
                P(str(r.get("input_dict")), styles["Cell"]),
                P("-" if ov is None else str(ov)[:42], styles["Cell"]),
                P(match, styles["Cell"]),
            ]
        )
    story.append(P(caption, styles["H3c"]))
    story.append(
        styled_table(
            table,
            [1.85 * inch, 1.15 * inch, 1.25 * inch, 1.45 * inch, 0.85 * inch],
            styles["CellHead"],
        )
    )
    story.append(Spacer(1, 8))


def toc_link(styles, key, label):
    return P(
        f'<a href="#{key}" color="#1f3a5f"><u>{label}</u></a>',
        styles["TOC"],
    )


def cover_flowables(styles):
    bits = [Spacer(1, 16 * mm)]
    if LOGO.exists():
        logo = fitted_image(LOGO, 3.9 * inch, 1.45 * inch)
        if logo:
            wrap = Table([[logo]], colWidths=[USABLE])
            wrap.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
            bits += [wrap, Spacer(1, 8 * mm)]
    bits += [
        HRFlowable(width="80%", thickness=1.2, color=GREEN, spaceBefore=2, spaceAfter=10, hAlign="CENTER"),
        P("Software Testing Report", styles["CoverH"]),
        P("Short-span steel girder module in OsdagBridge", styles["CoverSub"]),
        Spacer(1, 10 * mm),
    ]
    meta = [
        [P("<b>Name</b>", styles["CoverMeta"]), P(AUTHOR, styles["CoverMeta"])],
        [P("<b>College</b>", styles["CoverMeta"]), P(COLLEGE, styles["CoverMeta"])],
        [P("<b>Programme</b>", styles["CoverMeta"]), P(DEGREE, styles["CoverMeta"])],
        [P("<b>GitHub</b>", styles["CoverMeta"]), P(GITHUB, styles["CoverMeta"])],
        [P("<b>Build tested</b>", styles["CoverMeta"]),
         P("Windows 11, conda env osdagbridge-env, branch dev", styles["CoverMeta"])],
    ]
    mt = Table(meta, colWidths=[1.6 * inch, 4.9 * inch])
    mt.hAlign = "CENTER"
    mt.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, RULE),
            ]
        )
    )
    bits += [mt, PageBreak()]
    return bits


def main():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CoverH", fontName="Times-Bold", fontSize=20, leading=24, alignment=TA_CENTER, textColor=NAVY, spaceAfter=6))
    styles.add(ParagraphStyle(name="CoverSub", fontName="Times-Italic", fontSize=12, leading=16, alignment=TA_CENTER, textColor=NAVY, spaceAfter=4))
    styles.add(ParagraphStyle(name="CoverMeta", fontName="Times-Roman", fontSize=11, leading=14, textColor=colors.HexColor("#263238")))
    styles.add(ParagraphStyle(name="H2c", parent=styles["Heading2"], fontName="Times-Bold", textColor=NAVY, fontSize=13, spaceBefore=2, spaceAfter=8, leading=16, keepWithNext=True))
    styles.add(ParagraphStyle(name="H3c", parent=styles["Heading3"], fontName="Times-Bold", textColor=NAVY, fontSize=10.5, spaceBefore=8, spaceAfter=5, leading=13, keepWithNext=True))
    styles.add(ParagraphStyle(name="Bodyc", parent=styles["BodyText"], fontName="Times-Roman", alignment=TA_JUSTIFY, spaceAfter=8, leading=14, fontSize=10, textColor=colors.black))
    styles.add(ParagraphStyle(name="Cell", parent=styles["BodyText"], fontName="Times-Roman", fontSize=7.5, leading=10, textColor=colors.black))
    styles.add(ParagraphStyle(name="CellHead", fontName="Times-Bold", fontSize=8, leading=10.5, textColor=HEAD_FG))
    styles.add(ParagraphStyle(name="FigCap", fontName="Times-Italic", fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=colors.HexColor("#37474f"), spaceBefore=2, spaceAfter=2))
    styles.add(ParagraphStyle(name="TOC", fontName="Times-Roman", fontSize=11, leading=18, leftIndent=4, textColor=NAVY))

    ov = load_json(OVERVIEW, {"cases": [], "passed": 0, "failed": 0, "total": 0})
    tc02 = load_json(LOGS / "TC02_custom_materials_result.json")
    tc06 = load_json(LOGS / "TC06_additional_inputs_result.json")
    tc07 = load_json(LOGS / "TC07_distinct_cb_ed_materials_result.json")
    multi = load_json(LOGS / "TC_MULTI_01_result.json")
    deck = load_json(DICT / "TC02_custom_materials_deck_report_values.json") or load_json(DICT / "TC02_deck_report_values.json")
    slim02 = load_json(DICT / "TC02_custom_materials_output_slim.json", {})

    show_keys = [
        "geometry.span",
        "geometry.carriageway_width",
        "geometry.skew_angle",
        "material.girder",
        "material.cross_bracing",
        "material.end_diaphragm",
        "material.deck",
        "material.girder.fy",
        "material.girder.density",
        "material.deck.density",
        "typical_section.deck_thickness",
        "typical_section.wearing_course.density",
        "design_options.shear_studs.diameter",
        "design_options_cont.partial_factor.yielding_and_buckling.gamma_m0",
    ]

    story = []
    story.extend(cover_flowables(styles))

    story.append(Dest("contents", "Contents", 0))
    story.append(P('<a name="contents"/>Contents', styles["H2c"]))
    story.append(P("Click a heading to jump to that section.", styles["Bodyc"]))
    for key, label in [
        ("s1", "1. What I tested and why"),
        ("s2", "2. How this maps to the screening task"),
        ("s3", "3. How I ran the tests"),
        ("s4", "4. Result of every case"),
        ("s5", "5. Exact parameters I used"),
        ("s6", "6. UI values vs input dictionary vs output dictionary"),
        ("s7", "7. Steel members and the deck"),
        ("s8", "8. Three designs in a row after Unlock"),
        ("s9", "9. What the desktop window actually showed"),
        ("s10", "10. Bugs I found, and the files that should change"),
        ("s11", "11. Video"),
        ("s12", "12. What I take away"),
    ]:
        story.append(toc_link(styles, key, label))
    story.append(Spacer(1, 6))

    h2(story, styles, "s1", "1. What I tested and why")
    story.append(P(
        "OsdagBridge has a module for short-span steel girder (plate girder) highway bridges. "
        "The screening task asked for more than a single happy-path click of Design. I had to "
        "change basic geometry, additional section data, and custom steel and deck properties; "
        "run at least three designs after Unlock; check 3D CAD and plots; and compare what I "
        "typed with the internal input and output dictionaries.",
        styles["Bodyc"],
    ))
    story.append(P(
        "I cloned the project, created the conda environment, and ran the desktop app "
        "(python -m osdagbridge.desktop). I also wrote a runner that calls the same backend "
        "the GUI uses: PlateGirderBridge.set_input, design, get_results, and reset "
        "(that last call is what Unlock does). Failed cases were left as failures. I did not "
        "patch the product to make the log look clean.",
        styles["Bodyc"],
    ))
    story.append(P(
        "This PDF is the write-up of that work. The numbered tables and the screenshots are "
        "from the executed test suite (see evidence/logs/test_overview.json). Full side-by-side "
        "dictionary files are in test_cases/DICTIONARY_COMPARISON.md and evidence/dictionaries/.",
        styles["Bodyc"],
    ))

    h2(story, styles, "s2", "2. How this maps to the screening task")
    story.append(P(
        "The table below is the checklist I used. Every row is something the task asked for, "
        "and the right column is where the evidence sits in this report or in the ZIP.",
        styles["Bodyc"],
    ))
    map_data = [
        [P("<b>Task asked for</b>", styles["CellHead"]),
         P("<b>What I did</b>", styles["CellHead"])],
        [P("Basic geometry (span, width, skew, median, footpath)", styles["Cell"]),
         P("TC01 and TC08 at 30 m; TC03 with 12 deg skew, both footpaths and a median; TC04 at 20 m; TC05 at 45 m. Section 5.", styles["Cell"])],
        [P("Additional inputs (deck, wearing course, studs, factors)", styles["Cell"]),
         P("TC06: deck 280 mm, wearing 22 kN/m3 x 80 mm, covers 40/45, stud 22 x 125, gamma_m0 = 1.15. Sections 5-7.", styles["Cell"])],
        [P("Custom steel and custom deck, not only defaults", styles["Cell"]),
         P("TC02, TC07, TC09. Dictionaries keep the numbers. Analysis does not always use density. Sections 6 and 10.", styles["Cell"])],
        [P("At least 3 consecutive designs after Unlock", styles["Cell"]),
         P("TC_MULTI_01: 25 m, then 30 m, then 35 m after reset(). Same sequence on the live window and in the video. Sections 8-9.", styles["Cell"])],
        [P("3D CAD and structural plots", styles["Cell"]),
         P("Live OCC viewer + Plots dock (Section 9), exported OCC PNGs under evidence/screenshots/cad_3d/, and the video.", styles["Cell"])],
        [P("UI vs input dictionary vs output dictionary", styles["Cell"]),
         P("Section 6 tables. Full dumps in DICTIONARY_COMPARISON.md.", styles["Cell"])],
        [P("Steel components and the deck", styles["Cell"]),
         P("util.* , steeldesign.details.* , deck.report.* from TC02. Section 7.", styles["Cell"])],
        [P("Pass and fail log with exact parameters", styles["Cell"]),
         P("Sections 4-5. Two E 350A failures are kept on purpose.", styles["Cell"])],
        [P("Code-level GitHub issues", styles["Cell"]),
         P("Seven live issues on Nidhikhare12/OsdagBridge: #19, #20, #41-#45. Links in Section 10 and issues/ISSUE_LINKS.md.", styles["Cell"])],
        [P("Silent video of the workflow", styles["Cell"]),
         P("OsdagBridge_Testing_Demo.mp4. Section 11.", styles["Cell"])],
    ]
    story.append(styled_table(map_data, [2.35 * inch, 4.3 * inch], styles["CellHead"]))

    h2(story, styles, "s3", "3. How I ran the tests")
    story.append(P(
        "Each automated case does the same three steps the GUI does. First set_input writes "
        "the planned values onto the backend. Then design() runs analysis and member design. "
        "Then get_results() is the output dictionary that fills the Output dock and the design report.",
        styles["Bodyc"],
    ))
    story.append(P(
        "After a successful design I also asked for CAD through get_3d_cad_parameters (the OCC "
        "3D view is built from that object) and I built the structural plots with the same "
        "matplotlib helpers the Plots dock uses. For the three-run case I called reset() "
        "between designs, which is the function Unlock calls from input_dock.",
        styles["Bodyc"],
    ))
    story.append(P(
        "The screenshots in Section 9 are not drawings I generated for the report. They are "
        "window captures of the OsdagBridge desktop, maximised, with Basic Inputs on the left "
        "and CAD or plots on the right. I used those same frames for the silent video.",
        styles["Bodyc"],
    ))

    h2(story, styles, "s4", "4. Result of every case")
    story.append(P(
        f"I ran {ov.get('total', 0)} scenarios. "
        f"<b>{ov.get('passed', 0)} passed</b> (including pass-with-warnings) and "
        f"<b>{ov.get('failed', 0)} failed</b>.",
        styles["Bodyc"],
    ))
    story.append(P(
        "The two hard failures are TC01 and TC04. Both use the default database grade E 350A. "
        "Design stops because Gs (shear modulus) is not on input_dict. That is a product bug, "
        "not a bad test. TC08 is the same 30 m geometry after I wrote Gs and the deck fck / fctm / Ecm "
        "keys the material dialog would have written. TC08 finishes, which is how I knew the "
        "missing Gs was the trigger.",
        styles["Bodyc"],
    ))
    story.append(P(
        "Several passing cases still carry warnings. Those warnings are the defects in Section 10: "
        "custom density stored but not used, fatigue utilisation above 100% while design() still "
        "returns CAD, cross-bracing and end-diaphragm grades ignored, and missing DCR categories "
        "printed as 0.0.",
        styles["Bodyc"],
    ))
    data = [[
        P("<b>Case</b>", styles["CellHead"]),
        P("<b>Result</b>", styles["CellHead"]),
        P("<b>What I saw</b>", styles["CellHead"]),
    ]]
    notes = {
        "TC01_basic_optimized": "Default E 350A / M40, 30 m. Design stops: Gs is not set.",
        "TC02_custom_materials": "Custom steel density 80 and custom deck. CAD and plots come out. Analysis still uses 78500 N/m3.",
        "TC03_skew_footpath_median": "Skew 12 deg, both footpaths, median. Several util keys show 0.0 even though LTB is 20.44%.",
        "TC04_span_min_boundary": "20 m, default E 350A. Same Gs stop as TC01.",
        "TC05_span_max_boundary": "45 m custom materials. CAD produced. Fatigue UR 160%.",
        "TC06_additional_inputs": "Non-default deck, wearing course, studs, gamma. Values reach CAD.",
        "TC07_distinct_cb_ed_materials": "Three different custom steels stored. Design uses girder steel only.",
        "TC08_db_grade_with_gs": "Same as TC01 but Gs and deck fck primed. Design completes.",
        "TC09_custom_section_stiffeners": "Design Type = Custom. Explicit plates and two bearing stiffeners.",
        "TC10_osi_roundtrip": "OSI reload into a new backend. Keys survive at API. GUI map is still wrong.",
        "TC_MULTI_01": "Three designs after reset. CAD 25 m, then 30 m, then 35 m. No leftover span.",
    }
    for c in ov.get("cases") or []:
        cid = str(c.get("case_id", ""))
        data.append([
            P(cid, styles["Cell"]),
            P(str(c.get("status", "")), styles["Cell"]),
            P(notes.get(cid, ""), styles["Cell"]),
        ])
    story.append(styled_table(data, [2.05 * inch, 1.25 * inch, 3.35 * inch], styles["CellHead"]))
    story.append(Spacer(1, 6))
    story.append(P(
        "PASS_WITH_WARNINGS means design() returned and CAD was built, but I recorded a defect "
        "in the same run. I counted those as passes for the suite score and as bugs for the issue drafts.",
        styles["Bodyc"],
    ))

    h2(story, styles, "s5", "5. Exact parameters I used")
    story.append(P(
        "Unless a row says Custom, Design Type is Optimized. Project location is Mumbai for every case. "
        "That is the combination I saved in each .osi file under osi_files/.",
        styles["Bodyc"],
    ))
    params = [
        [P("<b>Case</b>", styles["CellHead"]),
         P("<b>Geometry</b>", styles["CellHead"]),
         P("<b>Materials and extras</b>", styles["CellHead"])],
        [P("TC01", styles["Cell"]), P("L=30 m, CW=7.5 m, skew=0, no median, no footpath", styles["Cell"]), P("Database E 350A, M40", styles["Cell"])],
        [P("TC02", styles["Cell"]), P("L=30 m, CW=7.5 m", styles["Cell"]), P("custom_steel_350_490, density 80; custom deck density 26", styles["Cell"])],
        [P("TC03", styles["Cell"]), P("L=28 m, CW=10 m, skew=12 deg, footpath Both, median Yes", styles["Cell"]), P("custom_steel_300_440", styles["Cell"])],
        [P("TC04", styles["Cell"]), P("L=20 m, CW=6 m", styles["Cell"]), P("Database E 350A, M40", styles["Cell"])],
        [P("TC05", styles["Cell"]), P("L=45 m, CW=12 m", styles["Cell"]), P("Custom steel/deck, density 78.5 / 25", styles["Cell"])],
        [P("TC06", styles["Cell"]), P("L=30 m, CW=7.5 m", styles["Cell"]), P("Deck 280 mm; wearing 22 x 80; stud 22 x 125; gamma_m0=1.15; ecc=1.5 m", styles["Cell"])],
        [P("TC07", styles["Cell"]), P("L=30 m, CW=7.5 m", styles["Cell"]), P("Girder 350/80; cross bracing 250/70; end diaphragm 280/75", styles["Cell"])],
        [P("TC08", styles["Cell"]), P("Same geometry as TC01", styles["Cell"]), P("E 350A plus Gs and deck fck/fctm/Ecm written on input_dict", styles["Cell"])],
        [P("TC09", styles["Cell"]), P("L=30 m; Design Type = Custom", styles["Cell"]), P("Plates 1400x450x20 / 520x25, tw=12; bearing stiffeners=2", styles["Cell"])],
        [P("TC10", styles["Cell"]), P("L=30 m", styles["Cell"]), P("TC02 OSI loaded into a fresh backend", styles["Cell"])],
        [P("MULTI", styles["Cell"]), P("25/7.5/0 deg then 30/8.5/5 deg then 35/9.5/10 deg", styles["Cell"]), P("Custom materials; reset() between runs", styles["Cell"])],
    ]
    story.append(styled_table(params, [0.85 * inch, 2.75 * inch, 3.05 * inch], styles["CellHead"]))

    h2(story, styles, "s6", "6. UI values vs input dictionary vs output dictionary")
    story.append(P(
        "After set_input I compared every planned field with input_dict. After design() I compared "
        "the same field with output_dict where that key exists. Match = Yes means the three sides "
        "agree within 1e-6. I print four tables here so the report can be read without opening JSON. "
        "The rest of the cases are in test_cases/DICTIONARY_COMPARISON.md.",
        styles["Bodyc"],
    ))
    compact_compare(story, styles, "TC02_custom_materials_comparison.json",
                    "Table 6.1  TC02 - custom steel and deck (stored correctly)", show_keys)
    story.append(P(
        "Table 6.1 is the important one for custom materials. Density 80 is in both dictionaries. "
        "The analysis still used 78500 N/m3. So the UI and the dicts are honest; _build_material_props "
        "is not reading density. That is defect 10.1.",
        styles["Bodyc"],
    ))
    compact_compare(story, styles, "TC06_additional_inputs_comparison.json",
                    "Table 6.2  TC06 - additional inputs reach both dictionaries", show_keys)
    story.append(P(
        "On TC06 the deck thickness 280 mm, wearing-course density and stud diameter 22 mm all "
        "match. The CAD deck thickness matched 280 mm as well, so additional inputs are not being "
        "silently replaced by defaults for those fields.",
        styles["Bodyc"],
    ))
    compact_compare(story, styles, "TC07_distinct_cb_ed_materials_comparison.json",
                    "Table 6.3  TC07 - three different steel grades are stored", show_keys)
    story.append(P(
        "TC07 was meant to check whether girder, cross bracing and end diaphragm can be different "
        "steels. The dictionaries do keep three grades. The design steel object is still built "
        "from the girder only (defect 10.4).",
        styles["Bodyc"],
    ))
    compact_compare(
        story, styles, "TC01_basic_optimized_comparison.json",
        "Table 6.4  TC01 - failed run: input dictionary after set_input (no complete output)",
        ["geometry.span", "geometry.carriageway_width", "material.girder", "material.deck"],
    )
    story.append(P(
        "TC01 never produced an output dictionary because design() raised on Gs. Geometry and the "
        "grade name did reach input_dict. The gap is the missing Gs key, not a failure to store span.",
        styles["Bodyc"],
    ))

    h2(story, styles, "s7", "7. Steel members and the deck")
    story.append(P(
        "The task asked to cover steel members and the deck, not only span and materials. "
        "Numbers below are from TC02 unless I say otherwise. They are the same keys the Output "
        "dock and the design-report chapters read.",
        styles["Bodyc"],
    ))
    cov = ((tc02.get("checks") or {}).get("coverage") or {})
    if cov.get("util_values"):
        urows = [[
            P("<b>Output-dock key</b>", styles["CellHead"]),
            P("<b>%</b>", styles["CellHead"]),
            P("<b>Remark</b>", styles["CellHead"]),
        ]]
        for k, v in cov["util_values"].items():
            flag = "Above 100; design() still finished" if isinstance(v, (int, float)) and v > 100 else "Within 100"
            urows.append([
                P(k, styles["Cell"]),
                P(f"{float(v):.2f}" if isinstance(v, (int, float)) else str(v), styles["Cell"]),
                P(flag, styles["Cell"]),
            ])
        h3(story, styles, "Table 7.1  Utilisation on the output dock (TC02)")
        story.append(styled_table(urows, [2.5 * inch, 1.0 * inch, 3.15 * inch], styles["CellHead"]))
        story.append(Spacer(1, 6))
        story.append(P(
            "Flexure, shear, LTB and deflection are all under 100%. Fatigue is 157%. The module "
            "still built CAD. I treated that as a defect (10.5), not as a pass on the check itself.",
            styles["Bodyc"],
        ))
    if slim02:
        srows = [[
            P("<b>Output key</b>", styles["CellHead"]),
            P("<b>Value</b>", styles["CellHead"]),
            P("<b>What it is</b>", styles["CellHead"]),
        ]]
        for k, note in [
            ("steeldesign.details.grade_of_material", "Steel grade on the dock"),
            ("steeldesign.details.section_designation", "Welded girder"),
            ("steeldesign.details.total_depth", "Girder depth (mm)"),
            ("steeldesign.details.web_thickness", "Web (mm)"),
            ("steeldesign.details.top_flange_width", "Top flange width (mm)"),
            ("steeldesign.details.shear.diameter", "Shear stud (mm)"),
            ("steeldesign.details.stiffener_summary.method", "Stiffener method"),
            ("steeldesign.details.stiffener_summary.end_count", "Bearing stiffeners"),
        ]:
            srows.append([P(k, styles["Cell"]), P(str(slim02.get(k, "-")), styles["Cell"]), P(note, styles["Cell"])])
        h3(story, styles, "Table 7.2  Steel dock vs output dictionary (TC02)")
        story.append(styled_table(srows, [3.15 * inch, 1.6 * inch, 1.9 * inch], styles["CellHead"]))
        story.append(Spacer(1, 6))
    if deck:
        drows = [[
            P("<b>Key</b>", styles["CellHead"]),
            P("<b>Value</b>", styles["CellHead"]),
            P("<b>What it is</b>", styles["CellHead"]),
        ]]
        for k, note in [
            ("deck.report.span", "Girder spacing 2.1 m"),
            ("deck.report.fy", "Fe 500 from Design Options"),
            ("deck.report.w_dl", "Slab dead load"),
            ("deck.report.m_uls_sag", "ULS sagging moment"),
            ("deck.report.as_req_bot", "Required bottom As"),
            ("deck.report.punch_ok", "Punching"),
            ("deck.report.shear_ok", "One-way shear"),
        ]:
            drows.append([P(k, styles["Cell"]), P(str(deck.get(k)), styles["Cell"]), P(note, styles["Cell"])])
        h3(story, styles, "Table 7.3  Deck report bag (TC02)")
        story.append(styled_table(drows, [2.2 * inch, 2.1 * inch, 2.35 * inch], styles["CellHead"]))
        story.append(Spacer(1, 6))
    echo = (tc06.get("checks") or {}).get("additional_echo") or {}
    if echo:
        story.append(P(
            f"On TC06 the extra section data is visible in the output: deck thickness "
            f"{echo.get('deck_thickness_out')} mm "
            f"(CAD {(tc06.get('checks') or {}).get('cad_deck_thickness')} mm); "
            f"wearing course density {echo.get('wc_density_out')} kN/m3, thickness "
            f"{echo.get('wc_thickness_out')} mm; stud entered {echo.get('stud_dia_in')} mm, "
            f"dock {echo.get('stud_dia_out')} mm.",
            styles["Bodyc"],
        ))
    dens7 = ((tc07.get("checks") or {}).get("custom_steel_density") or {})
    if dens7:
        story.append(P(
            f"On TC07 I set girder density {dens7.get('ui_input_density')}, cross bracing "
            f"{dens7.get('cb_ui_density')}, end diaphragm {dens7.get('ed_ui_density')}. "
            f"The analysis density was {dens7.get('backend_rho')} (girder default).",
            styles["Bodyc"],
        ))

    h2(story, styles, "s8", "8. Three designs in a row after Unlock")
    story.append(P(
        "Unlock on the desktop calls backend.reset() and clears the results. I needed to know "
        "whether the next Design still drew the previous span. TC_MULTI_01 uses one PlateGirderBridge "
        "instance, calls reset(), changes span / carriageway / skew, and designs again. The case "
        "fails if the old span is still in the output dictionary or if the CAD span does not move.",
        styles["Bodyc"],
    ))
    if multi.get("runs"):
        mrows = [[
            P("<b>Run</b>", styles["CellHead"]),
            P("<b>Planned L / CW / skew</b>", styles["CellHead"]),
            P("<b>Output L / CW / skew</b>", styles["CellHead"]),
            P("<b>CAD span (mm)</b>", styles["CellHead"]),
            P("<b>Stale?</b>", styles["CellHead"]),
        ]]
        for r in multi["runs"]:
            mrows.append([
                P(str(r.get("run")), styles["Cell"]),
                P(f"{r.get('span')} / {r.get('cw')} / {r.get('skew')}", styles["Cell"]),
                P(f"{r.get('output_span')} / {r.get('output_cw')} / {r.get('output_skew')}", styles["Cell"]),
                P(str(r.get("cad_span_mm")), styles["Cell"]),
                P(str(r.get("stale_span_detected")), styles["Cell"]),
            ])
        story.append(styled_table(mrows, [0.6 * inch, 1.7 * inch, 1.7 * inch, 1.3 * inch, 1.35 * inch], styles["CellHead"]))
        story.append(Spacer(1, 6))
        story.append(P(
            f"Suite result: <b>{multi.get('status')}</b>. Stale data found: {multi.get('stale_data_found')}. "
            "Run 1 is 25 m, run 2 is 30 m, run 3 is 35 m. CAD span in millimetres is 25000, 30000, 35000. "
            "The live window in Section 9 and the video follow the same order, with Unlock in between.",
            styles["Bodyc"],
        ))

    h2(story, styles, "s9", "9. What the desktop window actually showed")
    story.append(P(
        "The figures in this section are full-window captures of OsdagBridge. I kept each picture "
        "inside the page margin. Look at the left dock for the numbers I typed, and at the right "
        "pane for CAD or plots after Design.",
        styles["Bodyc"],
    ))

    h3(story, styles, "Custom materials, then Design")
    story.append(P(
        "Figure 1 is before Design. Girder and Cross bracing are set to custom_steel. Span is 30 m, "
        "carriageway 7.5 m. Figure 2 is the same session after Design: the dock is locked and the "
        "OCC view shows the deck, girders and bracing. That is the custom-material run the task asked for.",
        styles["Bodyc"],
    ))
    fig = figure_one(
        styles,
        GUI / "01b_custom_materials_fields.png",
        "Figure 1. Before Design. Custom steel on Girder and Cross bracing; span 30 m.",
    )
    if fig:
        story.append(fig)
    fig = figure_one(
        styles,
        GUI / "03_after_design_window.png",
        "Figure 2. After Design. OCC 3D CAD of the girder bridge in the same window.",
    )
    if fig:
        story.append(fig)

    h3(story, styles, "Plots dock, then Unlock")
    story.append(P(
        "Figure 3 is the Plots dock inside the same window, not a file export. Figure 4 is Unlock: "
        "the CAD is gone and Design is available again, which is the starting point for the next run.",
        styles["Bodyc"],
    ))
    fig = figure_one(
        styles,
        GUI / "07_plots_dock.png",
        "Figure 3. Plots dock. Shear-force diagram in the live window.",
    )
    if fig:
        story.append(fig)
    fig = figure_one(
        styles,
        GUI / "10_unlocked.png",
        "Figure 4. After Unlock. Results cleared, ready for the next design.",
    )
    if fig:
        story.append(fig)

    h3(story, styles, "Second and third design")
    story.append(P(
        "Figure 5 is the second design (span 25 m). Figure 6 is the third (span 35 m, skew 10 deg). "
        "The model on the right follows the new geometry. It is not the 30 m model left on screen.",
        styles["Bodyc"],
    ))
    fig = figure_one(
        styles,
        GUI / "12_run2_window.png",
        "Figure 5. Second design after Unlock. Span 25 m; CAD updated.",
    )
    if fig:
        story.append(fig)
    fig = figure_one(
        styles,
        GUI / "15_run3_window.png",
        "Figure 6. Third design. Span 35 m, skew 10 deg; CAD is not leftover from run 2.",
    )
    if fig:
        story.append(fig)

    h3(story, styles, "Plots produced by the dock generators (TC02)")
    story.append(P(
        "Figures 7 and 8 are the bending-moment and shear envelopes from the same functions the "
        "Plots dock calls after a custom-material design. They are here to show the dock is not empty. "
        "The window evidence is Figure 3 and the video.",
        styles["Bodyc"],
    ))
    fig = figure_one(
        styles,
        PLOTS / "TC02_custom_materials_plot_bmd.png",
        "Figure 7. Bending-moment envelope (Mz), TC02.",
        max_h=2.2 * inch,
    )
    if fig:
        story.append(fig)
    fig = figure_one(
        styles,
        PLOTS / "TC02_custom_materials_plot_sfd.png",
        "Figure 8. Shear-force envelope (Vy), TC02.",
        max_h=2.2 * inch,
    )
    if fig:
        story.append(fig)

    
    h3(story, styles, "Exported OCC 3D CAD (evidence/screenshots/cad_3d)")
    story.append(P(
        "Besides the live GUI window, I exported real OCC views with the same headless "
        "Viewer3d.ExportToImage path the product uses for report figures. Files live under "
        "evidence/screenshots/cad_3d/ (iso / front / top / end). That covers visual accuracy "
        "of the 3D CAD model for custom materials, skew/median, custom section, and the "
        "three Unlock redesigns (CAD span 25000 → 30000 → 35000 mm). Full checklist: "
        "test_cases/GRAPHICAL_OUTPUT_VERIFICATION.md.",
        styles["Bodyc"],
    ))
    fig = figure_one(
        styles,
        CAD3D / "TC02_custom_materials_cad_iso.png",
        "Figure 9. OCC isometric — TC02 custom materials (girders, deck, bracing, stiffeners).",
        max_h=2.4 * inch,
    )
    if fig:
        story.append(fig)
    fig = figure_one(
        styles,
        CAD3D / "TC03_skew_footpath_median_cad_iso.png",
        "Figure 10. OCC isometric — TC03 skew + median + footpath layout.",
        max_h=2.4 * inch,
    )
    if fig:
        story.append(fig)
    fig = figure_one(
        styles,
        CAD3D / "TC_MULTI_01_run1_cad_iso.png",
        "Figure 11. Multi-run 1 — CAD span 25 m after Design.",
        max_h=2.2 * inch,
    )
    if fig:
        story.append(fig)
    fig = figure_one(
        styles,
        CAD3D / "TC_MULTI_01_run3_cad_iso.png",
        "Figure 12. Multi-run 3 — CAD span 35 m (not a stale 25 m model).",
        max_h=2.2 * inch,
    )
    if fig:
        story.append(fig)

    h2(story, styles, "s10", "10. Bugs I found, and the files that should change")
    story.append(P(
        "I did not patch these in the clone used for the log, so the failed cases are still failed. "
        "Each item below links to a live issue on "
        '<a href="https://github.com/Nidhikhare12/OsdagBridge/issues" color="#1f3a5f">'
        "<u>github.com/Nidhikhare12/OsdagBridge/issues</u></a>. "
        "Local notes and suggested patches are also in issues/ and issues/ISSUE_LINKS.md. "
        "#19 and #20 already existed; they were reopened with fresh evidence. #41-#45 are new.",
        styles["Bodyc"],
    ))
    defects = [
        ("10.1  Custom steel density is ignored  "
         '(<a href="https://github.com/Nidhikhare12/OsdagBridge/issues/20" color="#1f3a5f"><u>#20</u></a>)',
         "File: plategirderbridge.py, _build_material_props. Custom fy, fu and E are read from "
         "input_dict. Density falls back to 78500 N/m3. TC02 stores density 80 in both dictionaries; "
         "analysis does not use it. Fix: when the database lookup is empty, read "
         "KEY_MATERIAL_GIRDER_DENSITY and convert kN/m3 to N/m3."),
        ("10.2  Grade E 350A has no Gs  "
         '(<a href="https://github.com/Nidhikhare12/OsdagBridge/issues/42" color="#1f3a5f"><u>#42</u></a>)',
         "File: designer.py, BridgeConfig.from_plate_girder_bridge. KEY_MATERIAL_GIRDER_G is required. "
         "TC01 and TC04 fail. TC08 completes when Gs and deck fck are primed the way the GUI dialog "
         "would. Fix: store Gs in SQLite, or set G = E / (2(1+nu)) when Gs is missing."),
        ("10.3  OSI load does not restore the custom-material map  "
         '(<a href="https://github.com/Nidhikhare12/OsdagBridge/issues/19" color="#1f3a5f"><u>#19</u></a>)',
         "File: input_dock.py, populate_from_dict. It does not rebuild _material_custom_fields. After "
         "a cold OSI load, _prime_material_inputs can overwrite custom fy, E and density. TC10 keeps "
         "the keys at API level. Fix: rebuild the map from loaded sub-keys, or skip priming when they "
         "already exist."),
        ("10.4  Cross-bracing and end-diaphragm custom grades are unused  "
         '(<a href="https://github.com/Nidhikhare12/OsdagBridge/issues/43" color="#1f3a5f"><u>#43</u></a>)',
         "One SteelProperties object is built from the girder grade only. TC07 stores distinct CB/ED "
         "fy and density; global design steel follows the girder. Fix: pass CB/ED properties into "
         "those members, or say in the UI that only girder steel is used."),
        ("10.5  Fatigue utilisation above 100% does not fail design()  "
         '(<a href="https://github.com/Nidhikhare12/OsdagBridge/issues/44" color="#1f3a5f"><u>#44</u></a>)',
         "TC02, TC05, TC06, TC07 finish and still emit CAD with util.fatigue between 157% and 176%. "
         "Fix: set a failed-design flag when any util.* exceeds 100, or ask before showing CAD."),
        ("10.6  Custom deck density is ignored  "
         '(<a href="https://github.com/Nidhikhare12/OsdagBridge/issues/41" color="#1f3a5f"><u>#41</u></a>)',
         "ConcreteProperties has no density field. add_dead_loads() calls create_deck_load with "
         "thickness only, so 25 kN/m3 is used. TC02 and TC06 enter 26. Fix: pass "
         "KEY_MATERIAL_DECK_DENSITY into create_deck_load."),
        ("10.7  Missing DCR categories are written as 0.0  "
         '(<a href="https://github.com/Nidhikhare12/OsdagBridge/issues/45" color="#1f3a5f"><u>#45</u></a>)',
         "store_design_results uses category_urs.get(..., 0.0)*100. On TC03, flexure/shear/fatigue "
         "show 0.0 while LTB is 20.44%. A skipped check looks like a safe 0%. Fix: write None when "
         "the category is absent."),
    ]
    for title, body in defects:
        story.append(KeepTogether([P(title, styles["H3c"]), P(body, styles["Bodyc"])]))

    h2(story, styles, "s11", "11. Video")
    story.append(P(
        "The file OsdagBridge_Testing_Demo.mp4 is a silent recording of the same desktop window "
        "as Section 9. There is no title card. The whole application window is in frame "
        "(letterboxed, not cropped).",
        styles["Bodyc"],
    ))
    story.append(P(
        "Order of shots: (1) custom steel and deck in Basic Inputs, span 30 m; "
        "(2) after Design, OCC 3D CAD; (3) Plots dock; (4) Unlock; "
        "(5) second design, span 25 m; (6) third design, span 35 m and skew 10 deg, CAD and plots updated. "
        "That covers custom materials, three consecutive runs, and CAD/plots. "
        "Upload the mp4 to YouTube (unlisted) or Drive and put the public URL in the form.",
        styles["Bodyc"],
    ))

    h2(story, styles, "s12", "12. What I take away")
    story.append(P(
        "Custom and additional inputs are stored from the values I typed, through input_dict, "
        "into output_dict. Three designs after Unlock do not keep a stale span or a stale CAD. "
        "The live window shows custom materials, 3D CAD and plots. Girder, stiffener, shear-connector "
        "and deck-report quantities are present after a passing design.",
        styles["Bodyc"],
    ))
    story.append(P(
        "Default E 350A cannot finish until Gs (and deck fck) are on input_dict; TC08 isolates that. "
        "Custom steel and deck densities are stored but not applied in analysis. Cross-bracing and "
        "end-diaphragm custom grades are not consumed. Fatigue UR can exceed 100% without aborting "
        "design. Both the passing cases and the two failures are in the log, with the exact parameter "
        "sets the task asked for.",
        styles["Bodyc"],
    ))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        title="OsdagBridge Software Testing Report",
        author=AUTHOR,
        subject="Short-span steel girder module - functional testing",
        leftMargin=LEFT_M,
        rightMargin=RIGHT_M,
        topMargin=20 * mm,
        bottomMargin=16 * mm,
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
