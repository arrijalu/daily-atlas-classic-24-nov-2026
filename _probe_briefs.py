"""Scratch probe 31: solve for the smallest legal grid yield.

The grid at 61 px is exactly saturated (2-line head + 2-line dek at 12 px
leading needs y0+62). Tightening the tile's internal leading to 11 px and
the tile height to 58 px recovers 12 px of band without touching type
sizes or cutting a word. Then: how much band height do the briefs need at
a block width that still leaves the map >= 260 px?
"""

import sys

sys.path.insert(0, ".")
from PIL import Image, ImageDraw

import draw as D

d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
tw = lambda s, f: d.textbbox((0, 0), s, font=f)[2] - d.textbbox((0, 0), s, font=f)[0]

print("grid at leading 11:")
for H in (56, 57, 58, 59, 60, 61):
    need = 14 + 11 * 2 + 11 * 2 - 11
    print("  H=%2d  need %2d  %s" % (H, need, "ok" if need <= H else "OVER"))

print()
print("grid span for tile heights (4 rows, 3 gaps of 5):")
for H in (56, 57, 58, 59, 60):
    span = 4 * H + 3 * 5
    print("  H=%2d -> %3d px, grid %d..%d" % (H, span, 488, 488 + span))

print()
print("briefs capacity vs block width (band = 884 - (gridend + 10))")
B = [
    ("16", "TALLINN", "Russia warns Estonia's moves are on the verge of triggering open war.", "REPORTED"),
    ("17", "MOSCOW", "More than 700,000 Russian soldiers killed in nearly five years of war, per a new analysis.", "REPORTED"),
    ("18", "BERLIN", "At the NATO assembly, Zelensky calls for Ukraine to join.", "OFFICIAL"),
    ("19", "BENGHAZI", "UNSMIL calls for an independent inquiry into Sunday's port and coastal attacks.", "OFFICIAL"),
    ("20", "BRUSSELS/KYIV", "Seven countries call to limit Russians' EU travel, especially for sport.", "REPORTED"),
    ("21", "SEOUL", "Joint Chiefs: Russian aircraft flew inside the air-defence identification zone.", "OFFICIAL"),
    ("22", "WASHINGTON", "Commerce blacklists Singapore's Megaspeed International.", "OFFICIAL"),
    ("23", "WASHINGTON/OTTAWA", "Pentagon: Canada falls short as a credible North America partner.", "REPORTED"),
    ("24", "SEOUL", "Up to $375,000 to catch students cheating on the entrance exam with AI.", "OFFICIAL"),
    ("25", "MOGADISHU/KAMPALA", "Somalia, Uganda to intensify Al-Shabaab operations as a withdrawal begins.", "REPORTED"),
    ("26", "CAMBRIDGE", "Arm extends CEO Rene Haas to 2033 amid Nvidia speculation.", "REPORTED"),
    ("27", "EUROPE", "Champions League: Real 5-1 PSV, Arsenal 1-1 Dortmund, City 2-2 Napoli, Galatasaray 1-0 Villa, Feyenoord 0-1 Porto, Leipzig 3-1 Lens.", "OFFICIAL"),
    ("28", "SINGAPORE", "Q3 GDP +6.1%; 2026 forecast raised to around 6%.", "OFFICIAL"),
    ("29", "BEIJING", "Record 90bn yuan of ETF buying fails to halt the AI sell-off; Shanghai up from a 16-month low.", "REPORTED"),
    ("30", "TOKYO", "PMI: manufacturing 53.7 on the strongest export orders since 2018, services 50.5; 10-year JGB yield 2.70%.", "OFFICIAL"),
    ("31", "MARKETS", "Oil near a three-month low: Brent ~$86 early, ~$91 by the US close; gold -2.16% at $3,556.31; bitcoin toward $60,000.", "CONFIRMED"),
    ("32", "SEOUL/SYDNEY", "Bank of Korea seen at 3.25% Thursday; ANZ moves its first RBA cut to June 2027.", "REPORTED"),
    ("33", "WASHINGTON", "PCE, GDP Wednesday; US markets shut Thursday for Thanksgiving.", "OFFICIAL"),
]
NUM, PLC, BODY = D.F("serif_b", 9), D.F("sans_b", 7), D.F("sans", 8)


def count(item, col):
    num, place, body, sure = item
    pre = tw(num, NUM) + 3 + tw(place, PLC) + 4
    words = (body + "  " + sure).split()
    n, cur, first = 1, "", True
    for w in words:
        sep = "" if not cur else " "
        room = col - (pre if first else 0)
        if tw(cur + sep + w, BODY) <= room:
            cur = cur + sep + w
        else:
            n += 1
            cur, first = w, False
    return n


print("%-5s %-6s %-6s %-6s %-5s %-6s %s"
      % ("tileH", "band0", "band1", "height", "lines", "block", "verdict"))
for H in (56, 57, 58, 59, 60, 61):
    gend = 488 + 4 * H + 3 * 5
    b0 = gend + 10
    height = 884 - b0
    cap = height // 9
    for block in (648, 660, 672, 684, 694):
        col = (block - 14) // 2
        cc = [count(b, col) for b in B]
        best = min(range(1, len(cc)),
                   key=lambda k: max(sum(cc[:k]), sum(cc[k:])))
        mx = max(sum(cc[:best]), sum(cc[best:]))
        ok = "OK" if mx <= cap else "over %d" % (mx - cap)
        print("%-5d %-6d %-6d %-6d %-5d %-6d %s"
              % (H, b0, 884, height, cap, block, ok))
    print()
