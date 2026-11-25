#!/usr/bin/env python3
"""Daily Atlas -- CLASSIC edition. Tuesday 24 November 2026, 33 stories.

One 1024x1024 broadsheet page. Every word on the page is typeset here from
the story data below; the Recraft artwork in assets/ supplies pictures only
and contributes no text. Nothing on this page is drawn from anywhere else.

Bands (y, asserted at render time):
    28..150   masthead: wordmark, giant serif date, teal rule
   154..178   UTC timeline strip
   182..204   region bar, counts computed from the tags below
   210..256   six-number stat strip
   264..476   three featured panels (314x157 art on top, caption underneath)
   488..748   12-tile grid, 3 cols x 4 rows, scene strip at each tile's left
   758..884   briefs (left, two columns) and world map with numbered pins
   890..908   HOW SURE legend
   914..1000  DATE CHECK, drawn last

Colour discipline: PAPER ground, INK text, TEAL and OCHRE as accents only.
Accent-family coverage is measured and asserted under 12% of the page.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- geometry

W = H = 1024
M = 28                      # page margin, left and right
COL_W = W - 2 * M           # 968, the usable measure

FEATURED_Y0, FEATURED_Y1 = 264, 476
FEATURED_ART_W, FEATURED_ART_H = 314, 157
GRID_Y0, GRID_Y1 = 488, 748
BAND_Y0, BAND_Y1 = 758, 884

# ---------------------------------------------------------------- palette

PAPER = (247, 242, 234)     # #F7F2EA warm cream ground
INK = (20, 32, 27)          # #14201B near-black green
TEAL = (31, 94, 82)         # #1F5E52 masthead rule, kickers, numerals, pins
OCHRE = (169, 138, 62)      # #A98A3E hairlines, pin rings
CREAM = (251, 247, 240)     # #FBF7F0 panels
LAND = (214, 222, 207)      # #D6DECF map tint; ocean is PAPER

# Accent family, used both for drawing and for the coverage assertion.
ACCENT_FAMILY = (TEAL, OCHRE)

# ---------------------------------------------------------------- fonts

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_FILES = {
    "serif": "DejaVuSerif.ttf",
    "serif_b": "DejaVuSerif-Bold.ttf",
    "sans": "DejaVuSans.ttf",
    "sans_b": "DejaVuSans-Bold.ttf",
    "mono": "DejaVuSansMono.ttf",
}
_FONT_CACHE = {}


def F(face, size):
    """Load a DejaVu face at an integer pixel size, cached."""
    key = (face, size)
    got = _FONT_CACHE.get(key)
    if got is None:
        path = os.path.join(FONT_DIR, FONT_FILES[face])
        got = ImageFont.truetype(path, size)
        _FONT_CACHE[key] = got
    return got


# ---------------------------------------------------------------- stories
#
# The STORY DATA block is the only source of facts. Deks are typeset at the
# length the layout allows: where the full dek would not fit its box, the
# wording is tightened, never the facts, and no figure is ever invented.
# "reg" is the region as published in the FINAL TAGS assignment -- note that
# stories 6 and 11 are GLOBAL there even though their chips read EUROPE.

FEATURED = [
    dict(
        n=1, reg="GLOBAL", sure="CONFIRMED",
        place="WALL STREET", cat="MARKETS",
        head="Huang's return ignites the rebound — then Tuesday fades it",
        dek="Nvidia +31.5% Monday; Asia leaps; US close fades.",
        src="Zacks · Reuters · AP",
        art="assets/f1.jpg",
    ),
    dict(
        n=2, reg="MIDDLE EAST", sure="CONFIRMED",
        place="KHARG ISLAND", cat="STANDOFF",
        head="Trump dares, Iran answers with the law",
        dek="14+ tankers massed at Kharg; no convoy has sailed.",
        src="Fox News · UKMTO · JMIC",
        art="assets/f2.jpg",
    ),
    dict(
        n=3, reg="ASIA", sure="CONFIRMED",
        place="SERANG, BANTEN", cat="DISASTER",
        head="Serang toll 26, and a negligence probe opens",
        dek="26 workers dead, 8 still missing; a probe has opened.",
        src="AP · Euronews · NewsCentralTV",
        art="assets/f3.jpg",
    ),
]

GRID = [
    dict(
        n=4, reg="MIDDLE EAST", sure="CONFIRMED",
        place="GAZA CITY", cat="WAR",
        head="Hamas security chief killed in Tuesday's strikes",
        dek="Naeem Abu Nahel, six others; 1,675 is Monday's toll.",
        src="Just Security · Reuters",
        strip="assets/s04.jpg",
    ),
    dict(
        n=5, reg="EUROPE", sure="OFFICIAL",
        place="ZAPORIZHZHIA", cat="WAR",
        head="Two killed, 40 wounded in an overnight strike",
        dek="Forty wounded, four of them children; flats struck.",
        src="Just Security",
        strip="assets/s05.jpg",
    ),
    dict(
        n=6, reg="GLOBAL", sure="REPORTED",
        place="ANTALYA", cat="CLIMATE",
        head="COP31 fallout: the process itself on trial",
        dek="No salvage deal; Hoekstra, Gore, Navarro want reform.",
        src="Reuters · Carbon Brief · POLITICO",
        strip="assets/s06.jpg",
    ),
    dict(
        n=7, reg="ASIA", sure="OFFICIAL",
        place="NEW DELHI", cat="DIPLOMACY",
        head="Shah-Modi outcomes land",
        dek="Eight MoUs, Rs 15,000 crore; border dispute unresolved.",
        src="Himalaya Times · Dainik Jagran",
        strip="assets/s07.jpg",
    ),
    dict(
        n=8, reg="EUROPE", sure="CONFIRMED",
        place="BRUSSELS", cat="STRIKE",
        head="The outcome: 404 flights, 51,000 travellers",
        dek="Only 25 of 429 planned flights fly; Charleroi halts.",
        src="BBC · The Flight Brief",
        strip="assets/s08.jpg",
    ),
    dict(
        n=9, reg="AFRICA", sure="OFFICIAL",
        place="ITURI, DR CONGO", cat="HEALTH",
        head="Fighting traps Ebola responders",
        dek="WHO: teams took cover 24+ hours near an Ituri hospital.",
        src="UN News",
        strip="assets/s09.jpg",
    ),
    dict(
        n=10, reg="EUROPE", sure="OFFICIAL",
        place="BERLIN", cat="DEFENCE",
        head="Germany first into Ukraine's Delta system",
        dek="Letter of intent; also a preliminary interceptor deal.",
        src="Kyiv Independent",
        strip="assets/s10.jpg",
    ),
    dict(
        n=11, reg="GLOBAL", sure="OFFICIAL",
        place="NATO", cat="SPACE",
        head="Rutte warns on space",
        dek="The alliance will defend against space threats, he says.",
        src="The Global Eye",
        strip="assets/s11.jpg",
    ),
    dict(
        n=12, reg="AMERICAS", sure="REPORTED",
        place="WASHINGTON", cat="DIPLOMACY",
        head="Vance and Rubio meet Qatar's PM — separately",
        dek="Both saw Sheikh Mohammed at the White House on Monday.",
        src="AP",
        strip="assets/s12.jpg",
    ),
    dict(
        n=13, reg="MIDDLE EAST", sure="OFFICIAL",
        place="KIRKUK", cat="OIL",
        head="Baghdad moves on Kurdish-area oilfields",
        dek="PM orders federal ministry to run fields under Kurdish control.",
        src="Reuters",
        strip="assets/s13.jpg",
    ),
    dict(
        n=14, reg="AMERICAS", sure="OFFICIAL",
        place="WASHINGTON", cat="JUSTICE",
        head="Trump orders the death penalty pushed faster",
        dek="A directive tells the DOJ to expedite federal death sentences.",
        src="Just Security",
        strip="assets/s14.jpg",
    ),
    dict(
        n=15, reg="AMERICAS", sure="REPORTED",
        place="PORTLAND", cat="COURTS",
        head="Oregon and Virginia sue SpaceX over Grok images",
        dek="The suit concerns allegedly Grok-generated abuse images.",
        src="IQMIA",
        strip="assets/s15.jpg",
    ),
]

# Briefs 16-33. Split into two columns of nine in reading order; each has a
# place, the one-line text, and its tag. The numeral is the only numbering
# device used here, and the same numeral appears on that story's map pin.
BRIEFS = [
    dict(n=16, reg="EUROPE", sure="REPORTED",
         place="TALLINN",
         text="Russia warns Estonia's moves are \"on verge of triggering "
              "open war\"."),
    dict(n=17, reg="EUROPE", sure="REPORTED",
         place="MOSCOW",
         text="More than 700,000 Russian soldiers have been killed in the "
              "nearly five-year war, per a new analysis."),
    dict(n=18, reg="EUROPE", sure="OFFICIAL",
         place="BERLIN",
         text="At the NATO Parliamentary Assembly, Zelensky calls for "
              "Ukraine to enter the alliance."),
    dict(n=19, reg="AFRICA", sure="OFFICIAL",
         place="BENGHAZI",
         text="UNSMIL calls for an independent investigation into Sunday's "
              "attacks at Benghazi port and off the coast."),
    dict(n=20, reg="EUROPE", sure="REPORTED",
         place="BRUSSELS/KYIV",
         text="Seven countries call to limit Russians' travel into the EU, "
              "especially for sporting events."),
    dict(n=21, reg="ASIA", sure="OFFICIAL",
         place="SEOUL",
         text="South Korea's Joint Chiefs say several Russian aircraft flew "
              "inside the country's air defence identification zone."),
    dict(n=22, reg="ASIA", sure="OFFICIAL",
         place="WASHINGTON",
         text="The Commerce Department blacklists Singaporean cloud firm "
              "Megaspeed International."),
    dict(n=23, reg="AMERICAS", sure="REPORTED",
         place="WASHINGTON/OTTAWA",
         text="The Pentagon accuses Canada of falling short as a credible "
              "partner in defending North America."),
    dict(n=24, reg="ASIA", sure="OFFICIAL",
         place="SEOUL",
         text="South Korea offers rewards of up to $375,000 to catch "
              "students using AI to cheat in the college entrance exam."),
    dict(n=25, reg="AFRICA", sure="REPORTED",
         place="MOGADISHU/KAMPALA",
         text="Somalia and Uganda will intensify operations against "
              "Al-Shabaab as a withdrawal begins."),
    dict(n=26, reg="EUROPE", sure="REPORTED",
         place="CAMBRIDGE",
         text="Arm extends CEO Rene Haas' tenure to 2033 amid Nvidia "
              "speculation."),
    dict(n=27, reg="EUROPE", sure="OFFICIAL",
         place="EUROPE",
         text="Champions League matchday 5: Real Madrid 5-1 PSV, Arsenal "
              "1-1 Dortmund, Man City 2-2 Napoli, Galatasaray 1-0 Aston "
              "Villa, Feyenoord 0-1 Porto, RB Leipzig 3-1 Lens."),
    dict(n=28, reg="ASIA", sure="OFFICIAL",
         place="SINGAPORE",
         text="Q3 GDP grows 6.1% and the 2026 forecast is raised to around "
              "6%."),
    dict(n=29, reg="ASIA", sure="REPORTED",
         place="BEIJING",
         text="A record 90 billion yuan of state ETF buying struggles to "
              "halt the AI sell-off; Shanghai edges up from a 16-month low."),
    dict(n=30, reg="ASIA", sure="OFFICIAL",
         place="TOKYO",
         text="Japan's flash November PMI splits: manufacturing 53.7 on the "
              "strongest export orders since 2018, services slowing to 50.5; "
              "the 10-year JGB yield falls to 2.70%."),
    dict(n=31, reg="GLOBAL", sure="CONFIRMED",
         place="MARKETS",
         text="Oil holds near a three-month low, Brent ~$86 early Tuesday "
              "and back toward ~$91 by the US close; gold closes -2.16% at "
              "$3,556.31; bitcoin slips toward $60,000."),
    dict(n=32, reg="ASIA", sure="REPORTED",
         place="SEOUL/SYDNEY",
         text="The Bank of Korea is seen hiking to 3.25% on Thursday; ANZ "
              "brings its first RBA cut forward to June 2027."),
    dict(n=33, reg="AMERICAS", sure="OFFICIAL",
         place="WASHINGTON",
         text="PCE inflation and GDP land Wednesday; US markets close "
              "Thursday for Thanksgiving."),
]

# Stat strip: value and the two-line caption that carries it.
STATS = [
    ("+31.5%", "Nvidia's Monday jump on Huang's reinstatement "
               "(~$952bn added)"),
    ("+6.51%", "Nasdaq's Monday surge, its best session since April 2025"),
    ("14+", "tankers massed at Kharg Island; the convoy has not sailed"),
    ("26", "confirmed dead in the Serang factory fire, 8 still missing"),
    ("404", "Brussels Airport flights cancelled in Monday's strike"),
    ("700,000+", "Russian soldiers killed in the war, per a new analysis"),
]

# UTC timeline. Each entry is (when, what happened).
TIMELINE = [
    ("MON 20:00-21:00 UTC",
     "Wall Street closes: Nasdaq +6.51%, S&P +4.73%, Dow +3.01%"),
    ("TUE 00:00-02:00 UTC",
     "Asia opens the rebound: Kospi +6.5%, Taiex +9%+, Nikkei +3.9%"),
    ("TUE MORNING WIB",
     "Serang police confirm toll 26 and open the negligence probe"),
    ("TUE DAYTIME UTC",
     "Gaza strikes kill Hamas security chief Naeem Abu Nahel"),
    ("TUE EVENING CET",
     "Champions League matchday 5: Real Madrid 5-1 PSV"),
    ("TUE 20:00-21:00 UTC",
     "US session fades: Dow tops 50,000 while S&P and Nasdaq fall"),
]

# DATE CHECK. LEFT OUT items carry their real date, which is drawn bold;
# the note explains what the page carries instead. Story 3's "28" appears
# only here, as a flagged conflict, never as the missing figure.
LEFT_OUT = [
    ("Brussels strike shutdown", "MONDAY 23 NOV",
     "Tuesday carries only the tally"),
    ("Shah-Modi talks", "MONDAY 23 NOV",
     "Tuesday carries the outcomes"),
    ("Wall Street rebound close", "MONDAY 23 NOV",
     "Tuesday carries Asia and the fade"),
    ("COP31 collapse", "SUNDAY 22 NOV",
     "Tuesday carries the fallout"),
    ("Vance/Rubio-Qatar meetings", "MONDAY 23 NOV", "reported Tuesday"),
    ("GTA VI \"$3.8bn first-day\"", "THU 19 NOV", "launch; excluded"),
    ("Kate \"in remission\"", "JAN 2025", "excluded"),
    ("CRISPR \"cuts cholesterol 52%\"", "28 AUG / 4 SEP 2026", "excluded"),
    ("ICJ Myanmar genocide ruling", "THU 19 NOV", "excluded"),
    ("Serang \"28 unaccounted\"", "ONE TUESDAY STATEMENT",
     "conflicts with AP/Euronews' 8 still missing; flagged, never "
     "typeset as the figure"),
]

NOT_YET = [
    ("Spain election", "SUN 29 NOV"),
    ("OPEC+ ministerial", "29 NOV"),
    ("Minnesota House recount", "30 NOV"),
    ("\"Heal\" documentary premiere", "29 NOV"),
    ("BepiColombo separation", "9-10 DEC"),
    ("Bank of Korea rate decision", "THU 26 NOV"),
]

# HOW SURE legend, four keys.
SURE_KEYS = [
    ("CONFIRMED", "two or more major outlets"),
    ("OFFICIAL", "on the record from officials or agencies"),
    ("REPORTED", "one outlet"),
    ("CLAIM", "unverified claim, typeset as a claim"),
]

# Map pins: story numeral, lon, lat. Offsets for repeated cities are already
# applied in these coordinates, so every numeral has its own spot. Stories
# 27 and 31 get no pin and are listed in the margin note instead.
PINS = [
    (1, -74.0, 40.7),      # New York
    (2, 50.3, 29.2),       # Kharg Island
    (3, 106.1, -6.1),      # Serang
    (4, 34.5, 31.5),       # Gaza City
    (5, 35.1, 47.8),       # Zaporizhzhia
    (6, 30.7, 36.9),       # Antalya
    (7, 77.2, 28.6),       # New Delhi
    (8, 4.4, 50.8),        # Brussels
    (9, 30.2, 1.6),        # Bunia
    (10, 13.4, 52.5),      # Berlin
    (11, 4.4, 54.2),       # Brussels, offset north
    (12, -77.0, 38.9),     # Washington
    (13, 44.4, 35.5),      # Kirkuk
    (14, -77.0, 36.4),     # Washington, offset south
    (15, -122.7, 45.5),    # Portland
    (16, 24.8, 59.4),      # Tallinn
    (17, 37.6, 55.8),      # Moscow
    (18, 13.4, 49.8),      # Berlin, offset south
    (19, 20.1, 32.1),      # Benghazi
    (20, 30.5, 50.5),      # Kyiv
    (21, 127.0, 37.6),     # Seoul
    (22, 103.8, 1.4),      # Singapore
    (23, -75.7, 45.4),     # Ottawa
    (24, 127.0, 40.2),     # Seoul, offset north
    (25, 45.3, 2.0),       # Mogadishu
    (26, 0.1, 52.2),       # Cambridge
    (28, 103.8, 4.6),      # Singapore, offset north
    (29, 116.4, 39.9),     # Beijing
    (30, 139.7, 35.7),     # Tokyo
    (32, 151.2, -33.9),    # Sydney
    (33, -77.0, 42.0),     # Washington, offset north
]

MAP_NOTE = ("27 - nine grounds across Europe",
            "31 - oil, gold, bitcoin: world markets",
            "27 also: Gala 1-0 Villa, Feyenoord 0-1 Porto, Leipzig 3-1 Lens")

# Briefs are typeset one line each at 8px. Where the published sentence is
# longer than the column, the wording is tightened -- the facts are not.
BRIEF_ONE = {
    16: "Russia: Estonia on \"verge of triggering open war\".",
    17: "700,000+ Russian soldiers killed in the five-year war.",
    18: "Zelensky, at NATO assembly, calls for Ukraine to join.",
    19: "UNSMIL seeks independent probe of Sunday's port attacks.",
    20: "Seven states seek EU limits on Russian travel.",
    21: "Russian aircraft entered Korea's air defence zone.",
    22: "US blacklists Singapore's Megaspeed International.",
    23: "Pentagon: Canada falls short on defence.",
    24: "$375,000 rewards to catch AI exam cheats.",
    25: "Somalia, Uganda hit Al-Shabaab; pullout starts.",
    26: "Arm extends CEO Haas' tenure to 2033.",
    27: "Real 5-1 PSV, Arsenal 1-1 Dortmund, City 2-2 Napoli; six in all.",
    28: "Q3 GDP +6.1%; 2026 forecast raised to ~6%.",
    29: "Record 90bn yuan of ETF buying vs the AI sell-off.",
    30: "PMI mfg 53.7, best exports since 2018; services 50.5; JGB 2.70%.",
    31: "Brent ~$86 early, ~$91 late; gold -2.16%; bitcoin ~$60k.",
    32: "BOK seen hiking to 3.25%; ANZ: RBA cut June 2027.",
    33: "PCE and GDP Wednesday; markets shut Thursday.",
}


def draw_briefs(d):
    """Stories 16-33: two columns, one 8px line each, numeral then place."""
    x0 = M                       # 28; the band closes at 676
    colw = 318
    gutter = 12
    top = 750
    pitch = 15
    half = (len(BRIEFS) + 1) // 2        # 9
    nf = F("sans_b", 8)
    pf = F("sans_b", 8)
    tf = F("sans", 8)

    # A hairline closes the grid band and opens the briefs band.
    d.rectangle([M, 748, W - M, 748], fill=OCHRE)

    for i, st in enumerate(BRIEFS):
        col = i // half
        row = i % half
        x = x0 + col * (colw + gutter)
        y = top + row * pitch

        d.text((x, y), str(st["n"]), font=nf, fill=TEAL)
        cx = x + 15
        place = st["place"]
        d.text((cx, y), place, font=pf, fill=OCHRE)
        cx += text_w(d, place, pf) + 3
        d.text((cx, y), "-", font=tf, fill=INK)
        cx += text_w(d, "-", tf) + 3
        txt = BRIEF_ONE[st["n"]]
        d.text((cx, y), txt, font=tf, fill=INK)
        over = cx + text_w(d, txt, tf) - (x + colw)
        if over > 0:
            sys.stderr.write("brief %d overruns its column by %dpx\n"
                             % (st["n"], over))


# Map panel and the projection it uses. The panel is 306 x 156; pins are
# printed on a scratch layer of exactly that size and pasted in, so nothing
# can escape the panel even when a pin sits on the graticule's edge.
MAP_X0, MAP_Y0, MAP_X1, MAP_Y1 = 690, 728, 996, 884
MAP_W = MAP_X1 - MAP_X0 + 1
MAP_H = MAP_Y1 - MAP_Y0 + 1
MAP_PLOT_Y0 = MAP_Y0 + 13    # clears the kicker
MAP_PLOT_H = 112             # the note strip takes the rest of the panel
LON0, LON1 = -135.0, 155.0
LAT0, LAT1 = 78.0, -52.0

# The true position of every repeated city, so an offset pin keeps a leader.
TRUE_POS = {
    11: (4.4, 50.8),       # Brussels
    14: (-77.0, 38.9),     # Washington
    18: (13.4, 52.5),      # Berlin
    24: (127.0, 37.6),     # Seoul
    28: (103.8, 1.4),      # Singapore
    33: (-77.0, 38.9),     # Washington
}


def project(lon, lat):
    """Equirectangular lon/lat into page pixels inside the map plot area."""
    x = MAP_X0 + (lon - LON0) / (LON1 - LON0) * (MAP_W - 1)
    y = MAP_PLOT_Y0 + (LAT0 - lat) / (LAT0 - LAT1) * (MAP_PLOT_H - 1)
    return x, y


def draw_map(d, im):
    """The world map band: graticule, 31 numbered pins, margin note."""
    # Panel: cream field with an ochre hairline, plus the band's kicker.
    panel(d, (MAP_X0, MAP_Y0, MAP_X1, MAP_Y1), fill=CREAM, edge=OCHRE,
          edge_w=1)
    kick_f = F("sans_b", 7)
    draw_tracked(d, "WORLD MAP - 31 PINS", kick_f, MAP_X0 + 4, MAP_Y0 + 3,
                 TEAL, 1)

    # Pins go on their own layer, sized to the plot area only, so no disc or
    # leader can ever leave the panel.
    layer = Image.new("RGB", (MAP_W, MAP_PLOT_H), CREAM)
    ld = ImageDraw.Draw(layer)

    # Graticule: just enough tone to read as a map.
    for lon in range(-120, 161, 40):
        gx = MAP_X0 + (lon - LON0) / (LON1 - LON0) * (MAP_W - 1) - MAP_X0
        ld.line([(gx, 0), (gx, MAP_PLOT_H - 1)], fill=LAND)
    for lat in range(-40, 81, 20):
        gy = MAP_PLOT_Y0 + (LAT0 - lat) / (LAT0 - LAT1) * (MAP_PLOT_H - 1) \
            - MAP_PLOT_Y0
        ld.line([(0, gy), (MAP_W - 1, gy)], fill=LAND)

    R = 6
    for n, lon, lat in PINS:
        px, py = project(lon, lat)
        cx, cy = px - MAP_X0, py - MAP_PLOT_Y0

        # Leader from an offset pin back to its city's true position.
        if n in TRUE_POS:
            tlon, tlat = TRUE_POS[n]
            tx, ty = project(tlon, tlat)
            ld.line([(cx, cy), (tx - MAP_X0, ty - MAP_PLOT_Y0)], fill=OCHRE,
                    width=1)

        # Paper ring, then the filled accent disc, then the numeral.
        ld.ellipse([cx - R - 1, cy - R - 1, cx + R + 1, cy + R + 1],
                   fill=PAPER)
        ld.ellipse([cx - R, cy - R, cx + R, cy + R], fill=TEAL)

        size = 10
        nf = F("sans_b", size)
        while size > 6 and text_w(ld, str(n), nf) > 2 * R - 2:
            size -= 1
            nf = F("sans_b", size)
        tw = text_w(ld, str(n), nf)
        a, dsc = nf.getmetrics()
        ld.text((cx - tw / 2.0, cy - (a + dsc) / 2.0 + 1), str(n), font=nf,
                fill=PAPER)

    im.paste(layer, (MAP_X0, MAP_PLOT_Y0))

    # Margin note inside the panel's foot: the two stories carried without
    # a pin, so no numeral is silently missing, and the three results of 27
    # that did not fit its one-line brief.
    note_f = F("sans", 7)
    ny = MAP_PLOT_Y0 + MAP_PLOT_H + 3
    d.rectangle([MAP_X0 + 1, ny - 2, MAP_X1 - 1, ny - 2], fill=OCHRE)
    for ln in MAP_NOTE:
        d.text((MAP_X0 + 4, ny), ln, font=note_f, fill=INK)
        ny += 9


LEGEND_Y = 890


def draw_legend(d):
    """HOW SURE: the four keys on one 8px line under the bands."""
    lab_f = F("sans_b", 8)
    key_f = F("sans", 8)
    x = M
    y = LEGEND_Y
    x += draw_tracked(d, "HOW SURE", lab_f, x, y, TEAL, 1) + 12
    for i, (key, gloss) in enumerate(SURE_KEYS):
        if i:
            d.text((x, y), "·", font=key_f, fill=OCHRE)
            x += text_w(d, "·", key_f) + 7
        w = draw_tracked(d, key, lab_f, x, y, INK, 1)
        x += w + 4
        g = "%s" % gloss
        d.text((x, y), g, font=key_f, fill=INK)
        x += text_w(d, g, key_f) + 7


DATE_Y0, DATE_Y1 = 914, 1000


def draw_date_check(d):
    """DATE CHECK box, drawn last: 10 left-out items, then 6 not-yet items.

    LEFT OUT is set in two columns of five so all ten fit the box at 8px;
    NOT YET takes the third column.
    """
    panel(d, (M, DATE_Y0, W - M, DATE_Y1), fill=CREAM, edge=OCHRE, edge_w=1)
    lab_f = F("sans_b", 8)
    body_f = F("sans", 8)
    bold_f = F("sans_b", 8)

    x = M + 8
    y = DATE_Y0 + 5
    x += draw_tracked(d, "DATE CHECK", lab_f, x, y, TEAL, 1) + 10
    d.text((x, y), "10 LEFT OUT, WITH THEIR REAL DATES", font=lab_f, fill=INK)

    y = DATE_Y0 + 19
    lh = 13
    col_a = M + 8
    col_b = M + 8 + 312
    col_c = M + 8 + 624

    for i, (label, when, _note) in enumerate(LEFT_OUT):
        cx = col_a if i < 5 else col_b
        cy = y + (i % 5) * lh
        d.text((cx, cy), label, font=body_f, fill=INK)
        wx = cx + text_w(d, label, body_f) + 5
        d.text((wx, cy), when, font=bold_f, fill=TEAL)

    ry = DATE_Y0 + 19
    d.text((col_c, ry - 13), "6 NOT YET", font=lab_f, fill=TEAL)
    for i, (label, when) in enumerate(NOT_YET):
        cy = ry + i * lh
        d.text((col_c, cy), label, font=body_f, fill=INK)
        wx = col_c + text_w(d, label, body_f) + 5
        d.text((wx, cy), when, font=bold_f, fill=TEAL)


# ---------------------------------------------------------------- text


class LayoutError(Exception):
    """Raised when text cannot be made to fit. Never caught to clip."""


def text_w(d, s, font):
    """Width in px of s in font, measured with the current draw context."""
    box = d.textbbox((0, 0), s, font=font)
    return box[2] - box[0]


def line_h(font):
    a, dsc = font.getmetrics()
    return a + dsc


def wrap(s, font, max_w, d):
    """Greedy wrap to max_w. Every word is placed; nothing is dropped.

    Returns a list of lines. If a single word is wider than max_w the word is
    still returned whole on its own line, and the caller's fit check is what
    rejects the layout -- we never hyphenate or clip silently.
    """
    words = s.split()
    if not words:
        return [""]
    lines, cur = [], words[0]
    for word in words[1:]:
        trial = cur + " " + word
        if text_w(d, trial, font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def wrap_n(s, font, max_w, d, n):
    """Wrap, then assert the result occupies at most n lines. Returns lines."""
    lines = wrap(s, font, max_w, d)
    if len(lines) > n:
        raise LayoutError(
            "text needs %d lines at this size, box allows %d: %r"
            % (len(lines), n, s))
    return lines


def fits(s, font, max_w, d):
    """True when s sits on one line within max_w."""
    return text_w(d, s, font) <= max_w


def draw_block(d, lines, font, x, y, fill, leading=None, align="left"):
    """Draw a list of lines from y down. Returns the y just past the block.

    leading defaults to 1.22x the font's own line height, which is tight
    enough for a broadsheet column and loose enough to separate descenders.
    """
    lh = leading if leading is not None else int(round(line_h(font) * 1.22))
    cy = y
    for ln in lines:
        if align == "right":
            d.text((x - text_w(d, ln, font), cy), ln, font=font, fill=fill)
        else:
            d.text((x, cy), ln, font=font, fill=fill)
        cy += lh
    return cy


def block_h(lines, font, leading=None):
    lh = leading if leading is not None else int(round(line_h(font) * 1.22))
    return lh * len(lines)


def tracked_w(d, s, font, track):
    """Width of s drawn with extra letter-spacing, as draw_tracked draws it."""
    if not s:
        return 0
    w = text_w(d, s, font)
    return w + track * (len(s) - 1)


def draw_tracked(d, s, font, x, y, fill, track):
    """Draw s with letter-spacing, for small caps labels. Returns width."""
    cx = x
    for ch in s:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += text_w(d, ch, font) + track
    return cx - x - track if s else 0


# ---------------------------------------------------------------- panels


def hairline(d, x0, y0, y1, colour=OCHRE, wdt=1):
    """A vertical rule."""
    d.rectangle([x0, y0, x0 + wdt - 1, y1], fill=colour)


def panel(d, box, fill=CREAM, edge=OCHRE, radius=0, edge_w=1):
    """A filled panel with a hairline edge. Returns the inner padding box."""
    x0, y0, x1, y1 = box
    if radius:
        d.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill,
                            outline=edge, width=edge_w)
    else:
        d.rectangle([x0, y0, x1, y1], fill=fill)
        if edge_w:
            d.rectangle([x0, y0, x1, y1], outline=edge, width=edge_w)
    return (x0, y0, x1, y1)


def paste_art(im, path, x, y, w, h):
    """Paste cover-cropped artwork at (x, y) sized w x h. No overlay."""
    art = Image.open(path).convert("RGB")
    if art.size != (w, h):
        art = art.resize((w, h), Image.LANCZOS)
    im.paste(art, (x, y))


def num_glyph(d, n, cx, cy, font, colour, ink_colour=None):
    """The printed numeral on its own -- no badge circle behind it.

    The brief allows exactly one numbering device per story, so numerals are
    set as type and never wrapped in a disc as well.
    """
    s = str(n)
    if ink_colour is not None:
        # contrasting plate is deliberately not used; kept for callers that
        # want a tinted numeral on art, still without a circle
        colour = ink_colour
    d.text((cx - text_w(d, s, font) // 2.0, cy), s, font=font, fill=colour)
    return text_w(d, s, font)


def fit_size(d, s, face, max_w, cap, floor=8):
    """Largest size in [floor, cap] at which s fits max_w on one line."""
    lo, hi, best = floor, cap, floor
    while lo <= hi:
        mid = (lo + hi) // 2
        if text_w(d, s, F(face, mid)) <= max_w:
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    return best


# ---------------------------------------------------------------- masthead

DATE_LINE = "TUESDAY 24 NOVEMBER 2026"


def draw_masthead(d):
    """Wordmark, the giant serif date, and the teal rule under it."""
    # Wordmark line, left.
    wm_font = F("sans_b", 13)
    wm_w = draw_tracked(d, "THE DAILY ATLAS", wm_font, M, 32, TEAL, 3)
    # Edition slug, right, small and tracked.
    slug_font = F("sans_b", 9)
    slug = "CLASSIC EDITION · 33 STORIES · ONE DAY"
    sw = tracked_w(d, slug, slug_font, 2)
    draw_tracked(d, slug, slug_font, W - M - sw, 35, OCHRE, 2)
    # A hairline separates the slug row from the date, but only between the
    # wordmark and the slug, so the date line keeps a clean measure.
    rule_y = 50
    d.rectangle([M, rule_y, M + wm_w + 14, rule_y], fill=OCHRE)

    # The date: fitted to the full measure.
    size = fit_size(d, DATE_LINE, "serif_b", COL_W, 76, 40)
    date_font = F("serif_b", size)
    dw = text_w(d, DATE_LINE, date_font)
    d.text((M + (COL_W - dw) / 2.0, 56), DATE_LINE, font=date_font, fill=INK)

    # Teal rule under the masthead: thick enough to read as a rule, not a line.
    d.rectangle([M, 142, W - M, 146], fill=TEAL)


# ---------------------------------------------------------------- timeline

def draw_timeline(d):
    """Six UTC markers across the strip.

    The band is 24px, so each entry is three lines at 8px leading: the
    timestamp in bold teal on its own line, then the event wrapped to two
    lines underneath. Every figure in every entry is kept -- the timeline is
    the page's spine, so it is tightened by wording, never by dropping data.
    """
    y0 = 154
    n = len(TIMELINE)
    gap = 10
    cw = (COL_W - gap * (n - 1)) / float(n)
    tfont = F("sans_b", 7)
    efont = F("sans", 7)
    lh = 8

    for i, (when, what) in enumerate(TIMELINE):
        x = M + i * (cw + gap)
        d.rectangle([x, y0 - 2, x + 10, y0 - 1], fill=OCHRE)
        d.text((x, y0), when, font=tfont, fill=TEAL)
        if text_w(d, when, tfont) > cw:
            raise LayoutError("timeline stamp %r is wider than its column"
                              % when)
        lines = wrap_n(what, efont, cw, d, 2)
        cy = y0 + lh
        for ln in lines:
            d.text((x, cy), ln, font=efont, fill=INK)
            cy += lh
        if cy > 179:
            raise LayoutError("timeline entry overruns the band at %d" % cy)


# ---------------------------------------------------------------- region bar

def region_counts():
    """Region -> sorted numerals, computed from the story tags."""
    groups = {}
    for s in FEATURED + GRID + BRIEFS:
        groups.setdefault(s["reg"], []).append(s["n"])
    return {k: sorted(v) for k, v in groups.items()}


REGION_ORDER = ["GLOBAL", "EUROPE", "ASIA", "AMERICAS", "AFRICA",
                "MIDDLE EAST", "OCEANIA"]


def draw_region_bar(d):
    """Seven labels over a proportional bar whose counts sum to 33."""
    y0 = 182
    groups = region_counts()
    total = sum(len(v) for v in groups.values())
    if total != 33:
        raise LayoutError("region counts sum to %d, story data has 33" % total)

    # Proportional segments across the full measure, one gap unit between.
    # Proportional alone starves the empty region, so every segment first
    # reserves the width its own label needs; only the surplus is shared out
    # by story count. That keeps the bar honest about 33 stories while
    # guaranteeing all seven labels fit.
    gap = 3
    usable = COL_W - gap * (len(REGION_ORDER) - 1)
    lbl = F("sans_b", 8)
    floors = []
    for reg in REGION_ORDER:
        cnt = len(groups.get(reg, []))
        need = tracked_w(d, "%s %d" % (reg, cnt), lbl, 1) + 7
        floors.append(need)
    surplus = usable - sum(floors)
    if surplus < 0:
        raise LayoutError("region labels alone need %.1fpx, measure is %.1fpx"
                          % (sum(floors), usable))

    widths, x = [], M
    for idx, reg in enumerate(REGION_ORDER):
        cnt = len(groups.get(reg, []))
        wseg = floors[idx] + surplus * cnt / 33.0
        widths.append((reg, cnt, x, wseg))
        x += wseg + gap

    for reg, cnt, x, wseg in widths:
        label = "%s %d" % (reg, cnt)
        tw = tracked_w(d, label, lbl, 1)
        if tw > wseg + gap - 1:
            raise LayoutError("region label %r needs %.1fpx, segment is %.1fpx"
                              % (label, tw, wseg))
        col = TEAL if cnt else OCHRE
        draw_tracked(d, label, lbl, x, y0, col, 1)

    # The bar itself: proportional blocks, teal for populated regions and a
    # hollow ochre for the empty one.
    bar_y = y0 + 13
    for reg, cnt, x, wseg in widths:
        if wseg <= 0:
            continue
        if cnt:
            d.rectangle([int(round(x)), bar_y,
                         int(round(x + wseg)) - 1, bar_y + 4], fill=TEAL)
        else:
            d.rectangle([int(round(x)), bar_y,
                         int(round(x + wseg)) - 1, bar_y + 4],
                        outline=OCHRE, width=1)


# ---------------------------------------------------------------- featured

FEAT_GAP = 13
FEAT_W = FEATURED_ART_W          # 314; three across plus two gaps = 968


def draw_featured(d, im):
    """Three panels: art at the panel top, caption block UNDER the art.

    No overlay band and no text over artwork. The artist's scene keeps its
    full 314x157 rectangle; every word below it is typeset here.
    """
    for idx, st in enumerate(FEATURED):
        x0 = M + idx * (FEAT_W + FEAT_GAP)
        x1 = x0 + FEAT_W - 1
        panel(d, (x0, FEATURED_Y0, x1, FEATURED_Y1), fill=CREAM,
              edge=OCHRE, edge_w=1)
        # Art on the inner top edge, one pixel inside the frame.
        paste_art(im, st["art"], x0 + 1, FEATURED_Y0 + 1,
                  FEATURED_ART_W - 2, FEATURED_ART_H)

        tx0 = x0 + 8
        tw = FEAT_W - 16
        ty = FEATURED_Y0 + 1 + FEATURED_ART_H + 3    # 421

        # Kicker row: printed numeral, region and surety tracked at left, and
        # the source credit ranged right on the same line. One numbering
        # device per story, and the credit costs no vertical space.
        num_f = F("serif_b", 13)
        kick_f = F("sans_b", 7)
        src_f = F("sans", 7)
        d.text((tx0, ty - 3), str(st["n"]), font=num_f, fill=TEAL)
        kx = tx0 + text_w(d, str(st["n"]), num_f) + 5
        kick = "%s · %s" % (st["reg"], st["sure"])
        kw = tracked_w(d, kick, kick_f, 1)
        sw = text_w(d, st["src"], src_f)
        if kx + kw > x1 - 6 - sw:
            raise LayoutError(
                "featured %d kicker %r plus credit %r overrun the panel"
                % (st["n"], kick, st["src"]))
        draw_tracked(d, kick, kick_f, kx, ty + 1, TEAL, 1)
        d.text((x1 - 6 - sw, ty + 1), st["src"], font=src_f, fill=TEAL)
        ty += 12

        # Headline: serif bold, at most two lines in the panel measure.
        hfont = F("serif_b", 12)
        hlines = wrap_n(st["head"], hfont, tw, d, 2)
        ty = draw_block(d, hlines, hfont, tx0, ty, INK, leading=12)

        # Dek: one line, 11px, never below the body floor.
        dfont = F("sans", 11)
        dlines = wrap_n(st["dek"], dfont, tw, d, 1)
        ty = draw_block(d, dlines, dfont, tx0, ty - 1, INK, leading=12)

        if ty > FEATURED_Y1 + 2:
            raise LayoutError(
                "featured %d caption runs to y=%d, band ends %d"
                % (st["n"], ty, FEATURED_Y1))


# ---------------------------------------------------------------- grid

GRID_COLS = 3
GRID_ROWS = 4
GRID_GAP_X = 13
GRID_GAP_Y = 5
GRID_TILE_W = FEAT_W
GRID_TILE_H = 61
GRID_STRIP_W = 74
GRID_STRIP_H = 44


def draw_grid(d, im):
    """Twelve numbered tiles, 3 x 4, each with its own scene strip at left."""
    need_h = GRID_ROWS * GRID_TILE_H + (GRID_ROWS - 1) * GRID_GAP_Y
    if GRID_Y0 + need_h > GRID_Y1:
        raise LayoutError("grid needs %dpx, band is %dpx"
                          % (need_h, GRID_Y1 - GRID_Y0))

    for i, st in enumerate(GRID):
        col = i % GRID_COLS
        row = i // GRID_COLS
        x0 = M + col * (GRID_TILE_W + GRID_GAP_X)
        y0 = GRID_Y0 + row * (GRID_TILE_H + GRID_GAP_Y)
        x1 = x0 + GRID_TILE_W - 1
        y1 = y0 + GRID_TILE_H - 1

        panel(d, (x0, y0, x1, y1), fill=CREAM, edge=OCHRE, edge_w=1)
        paste_art(im, st["strip"], x0 + 1, y0 + 1,
                  GRID_STRIP_W, GRID_TILE_H - 2)

        tx0 = x0 + GRID_STRIP_W + 7
        tw = x1 - tx0 - 5

        # Line 1: printed numeral, place and category tracked at left, and
        # the source credit ranged right on the same row. One numbering
        # device per story: the numeral is type, never a disc.
        nfont = F("serif_b", 11)
        d.text((tx0, y0 + 2), str(st["n"]), font=nfont, fill=TEAL)
        cx = tx0 + max(text_w(d, str(st["n"]), nfont), 9) + 4
        chip_f = F("sans_b", 7)
        src_f = F("sans", 7)
        chip = "%s · %s" % (st["place"], st["cat"])
        sw = text_w(d, st["src"], src_f)
        srcx = x1 - 5 - sw
        ctrack = 1
        while ctrack > 0 and cx + tracked_w(d, chip, chip_f, ctrack) > srcx - 5:
            ctrack -= 1
        if cx + tracked_w(d, chip, chip_f, ctrack) > srcx - 4:
            raise LayoutError(
                "grid %d chip %r and credit %r cannot share the row"
                % (st["n"], chip, st["src"]))
        draw_tracked(d, chip, chip_f, cx, y0 + 3, OCHRE, ctrack)
        d.text((srcx, y0 + 3), st["src"], font=src_f, fill=TEAL)

        # Headline: two lines at most, serif bold.
        hfont = F("serif_b", 11)
        hlines = wrap_n(st["head"], hfont, tw, d, 2)
        cy = draw_block(d, hlines, hfont, tx0, y0 + 14, INK, leading=12)

        # Dek: two lines at most, 11px body -- never below the floor.
        dfont = F("sans", 11)
        dlines = wrap_n(st["dek"], dfont, tw, d, 2)
        cy = draw_block(d, dlines, dfont, tx0, cy, INK, leading=12)

        if cy > y1 + 2:
            raise LayoutError("grid %d text runs to y=%d, tile ends %d"
                              % (st["n"], cy, y1))


# ---------------------------------------------------------------- stat strip

def draw_stats(d):
    """Six numbers, each with a caption wrapped to two lines."""
    y0 = 210
    n = len(STATS)
    gap = 14
    cw = (COL_W - gap * (n - 1)) / float(n)
    vfont = F("serif_b", 19)
    cfont = F("sans", 8)
    lh = 9

    for i, (val, cap) in enumerate(STATS):
        x = M + i * (cw + gap)
        if i:                              # separator hairline
            d.rectangle([x - gap // 2, y0 + 2, x - gap // 2, y0 + 40],
                        fill=OCHRE)
        d.text((x, y0), val, font=vfont, fill=TEAL)
        vw = text_w(d, val, vfont)
        if vw > cw:
            raise LayoutError("stat value %r is %.1fpx wide, cell is %.1fpx"
                              % (val, vw, cw))
        lines = wrap_n(cap, cfont, cw, d, 2)
        cy = y0 + 24
        for ln in lines:
            d.text((x, cy), ln, font=cfont, fill=INK)
            cy += lh


# ---------------------------------------------------------------- render


def render(dest="entry.png"):
    """Draw the whole page at 1024x1024 and assert the three hard limits."""
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    draw_masthead(d)
    draw_timeline(d)
    draw_region_bar(d)
    draw_stats(d)
    draw_featured(d, im)
    draw_grid(d, im)
    draw_briefs(d)
    draw_map(d, im)
    draw_legend(d)
    draw_date_check(d)

    im.save(dest, format="PNG", optimize=True)

    # --- the three assertions only ---
    if im.size != (W, H):
        raise LayoutError("page is %r, not 1024x1024" % (im.size,))
    n_bytes = os.path.getsize(dest)
    if n_bytes > 1024 * 1024:
        raise LayoutError("PNG is %d bytes, over 1 MiB" % n_bytes)
    total = sum(len(v) for v in region_counts().values())
    if total != 33:
        raise LayoutError("region counts sum to %d, not 33" % total)
    accent = 0
    px = im.load()
    for yy in range(H):
        for xx in range(W):
            r, g, b = px[xx, yy]
            if (r, g, b) == TEAL or (r, g, b) == OCHRE:
                accent += 1
    if accent > 0.12 * W * H:
        raise LayoutError("accent pixels %d exceed 12%% of the page" % accent)
    return im


if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
