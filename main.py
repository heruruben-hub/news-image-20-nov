#!/usr/bin/env python3
"""News Image 20 November 2026.

Draws a newspaper-style front page on a 1024x1024 canvas summing up the
world news of Friday 20 November 2026. Python 3 standard library only, no
network, no clock, no randomness: every run produces byte-identical output.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- font -----
# 5x7 bitmap font, embedded as data. Each glyph is 7 rows of 5 pixels.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01110"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "11001", "10101", "10011", "10011", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10011", "10101", "11001", "10001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00010", "00100", "00100", "00100"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "01100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "01100", "01000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "%": ("10001", "10010", "00010", "00100", "01000", "10010", "10001"),
    "$": ("00100", "01111", "10101", "01110", "00101", "11110", "00100"),
    "/": ("00001", "00010", "00010", "00100", "00100", "01000", "10000"),
    "(": ("00011", "00100", "01000", "01000", "01000", "00100", "00011"),
    ")": ("11000", "00100", "00010", "00010", "00010", "00100", "11000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
}

# -------------------------------------------------------------- colours ----
PAPER = (245, 240, 228)
INK = (22, 22, 30)
NAVY = (18, 38, 74)
NAVY_DARK = (12, 26, 52)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
GRAY = (102, 102, 100)
DARKGRAY = (58, 58, 62)
TINT_BLUE = (232, 237, 245)
TINT_RED = (245, 230, 224)
TINT_GOLD = (247, 238, 214)
RULE = (150, 145, 130)
WHITE = (255, 255, 255)
SKY = (168, 205, 232)
SEA = (46, 110, 158)
GREEN = (34, 120, 60)
ORANGE = (214, 110, 30)

# ----------------------------------------------------------- framebuffer ----
fb = bytearray(W * H * 3)


def px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        fb[i], fb[i + 1], fb[i + 2] = color


def fill_rect(x, y, w, h, color):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        for xx in range(x0, x1):
            i = base + (xx - x0) * 3
            fb[i], fb[i + 1], fb[i + 2] = color


def rect_outline(x, y, w, h, color, t=1):
    fill_rect(x, y, w, t, color)
    fill_rect(x, y + h - t, w, t, color)
    fill_rect(x, y, t, h, color)
    fill_rect(x + w - t, y, t, h, color)


def disc(cx, cy, r, color):
    for dy in range(-r, r + 1):
        dx = int((r * r - dy * dy) ** 0.5)
        for xx in range(cx - dx, cx + dx + 1):
            px(xx, cy + dy, color)


def ring(cx, cy, r, color, t=2):
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            d2 = dx * dx + dy * dy
            if (r - t) * (r - t) <= d2 <= r * r:
                px(cx + dx, cy + dy, color)


def line(x0, y0, x1, y1, color, t=1):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        for ox in range(t):
            for oy in range(t):
                px(x0 + ox, y0 + oy, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def triangle(x0, y0, x1, y1, x2, y2, color):
    pts = sorted(((x0, y0), (x1, y1), (x2, y2)), key=lambda p: p[1])
    (ax, ay), (bx, by), (cx, cy) = pts
    if ay == cy:
        return
    for y in range(ay, cy + 1):
        if y < by:
            xa = ax + (bx - ax) * (y - ay) / max(1, by - ay)
            xb = ax + (cx - ax) * (y - ay) / max(1, cy - ay)
        else:
            xa = bx + (cx - bx) * (y - by) / max(1, cy - by)
            xb = ax + (cx - ax) * (y - ay) / max(1, cy - ay)
        for x in range(int(min(xa, xb)), int(max(xa, xb)) + 1):
            px(x, y, color)


def rounded_rect(x, y, w, h, r, color):
    fill_rect(x + r, y, w - 2 * r, h, color)
    fill_rect(x, y + r, w, h - 2 * r, color)
    disc(x + r, y + r, r, color)
    disc(x + w - r - 1, y + r, r, color)
    disc(x + r, y + h - r - 1, r, color)
    disc(x + w - r - 1, y + h - r - 1, r, color)


# -------------------------------------------------------------- text -------
def char_width(scale):
    return 6 * scale


def text_width(text, scale):
    return len(text) * char_width(scale) - scale


def draw_char(ch, x, y, scale, color):
    glyph = FONT.get(ch.upper(), FONT[" "])
    for row in range(7):
        bits = glyph[row]
        for col in range(5):
            if bits[col] == "1":
                fill_rect(x + col * scale, y + row * scale, scale, scale, color)


def draw_text(x, y, text, scale, color):
    cx = x
    for ch in text:
        draw_char(ch, cx, y, scale, color)
        cx += char_width(scale)
    return cx


def draw_text_centered(cx, y, text, scale, color):
    draw_text(cx - text_width(text, scale) // 2, y, text, scale, color)


def wrap_text(text, scale, max_width):
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(x, y, text, scale, max_width, line_h, color, max_lines=None):
    lines = wrap_text(text, scale, max_width)
    if max_lines:
        lines = lines[:max_lines]
    for i, ln in enumerate(lines):
        draw_text(x, y + i * line_h, ln, scale, color)
    return len(lines)


# --------------------------------------------------------- pictograms ------
def pic_flags(x, y, s):
    # Two flags on poles: US (stars and stripes) and Iran (tricolour).
    line(x + 22, y + 8, x + 22, y + s - 14, INK, 2)
    line(x + s - 24, y + 8, x + s - 24, y + s - 14, INK, 2)
    # US flag, left
    fx, fy, fw, fh = x + 20, y + 10, 44, 30
    for i in range(7):
        fill_rect(fx, fy + i * 4, fw, 4, RED if i % 2 == 0 else WHITE)
    fill_rect(fx, fy, 19, 16, NAVY)
    for r in range(3):
        for c in range(4):
            px(fx + 3 + c * 5, fy + 3 + r * 5, WHITE)
    # Iran flag, right
    gx, gy, gw, gh = x + 72, y + 10, 44, 30
    fill_rect(gx, gy, gw, 10, GREEN)
    fill_rect(gx, gy + 10, gw, 10, WHITE)
    fill_rect(gx, gy + 20, gw, 10, RED)
    disc(gx + gw // 2, gy + 15, 4, RED)
    # ground line
    line(x + 8, y + s - 12, x + s - 8, y + s - 12, INK, 2)


def pic_cyclone(x, y, s):
    # Spiral storm: parametric swirl + rain streaks.
    cx, cy = x + s // 2, y + s // 2 - 6
    prev = None
    steps = 220
    for i in range(steps + 1):
        t = i / steps * 4.2 * 3.14159
        r = 3 + i / steps * 52
        px2 = int(cx + r * 0.94 * _cos(t))
        py2 = int(cy + r * 0.94 * _sin(t))
        if prev is not None:
            line(prev[0], prev[1], px2, py2, SEA, 3)
        prev = (px2, py2)
    disc(cx, cy, 7, NAVY)
    for dx, dy in ((-38, 34), (-18, 40), (6, 42), (28, 36)):
        line(x + s // 2 + dx, y + s - 34, x + s // 2 + dx - 5, y + s - 20, SEA, 2)


def _cos(t):
    # Deterministic cosine. Reduce to [0, pi/2] first so the Taylor
    # series (to x^6) stays accurate to ~0.0003.
    pi = 3.141592653589793
    t = t % (2 * pi)
    sign = 1
    if t > pi:
        t -= pi
        sign = -1
    if t > pi / 2:
        t = pi - t
        sign = -sign
    x2 = t * t
    return sign * (1 - x2 / 2 + x2 * x2 / 24 - x2 * x2 * x2 / 720)


def _sin(t):
    return _cos(t - 3.141592653589793 / 2)


def pic_markets(x, y, s):
    # Rising bars and an arrow over axes.
    ox, oy = x + 16, y + s - 22
    line(ox, y + 14, ox, oy, INK, 2)
    line(ox, oy, x + s - 14, oy, INK, 2)
    bars = [18, 30, 44, 62]
    bw = 16
    for i, bh in enumerate(bars):
        bx = ox + 12 + i * 26
        fill_rect(bx, oy - bh, bw, bh, GREEN if i == 3 else SEA)
    line(ox + 8, oy - 14, x + s - 30, y + 22, RED, 3)
    triangle(x + s - 34, y + 18, x + s - 20, y + 26, x + s - 30, y + 34, RED)
    draw_text(x + 16, y + 8, "+17%", 2, RED)


def pic_space(x, y, s):
    # Asteroid with craters + small probe with solar panels.
    ax, ay, ar = x + 44, y + 78, 34
    disc(ax, ay, ar, (150, 140, 125))
    disc(ax - 12, ay - 8, 8, (120, 110, 96))
    disc(ax + 10, ay + 10, 6, (120, 110, 96))
    disc(ax + 14, ay - 14, 4, (120, 110, 96))
    ring(ax, ay, ar, (120, 110, 96), 2)
    # probe body
    fill_rect(x + 84, y + 22, 26, 18, GOLD)
    fill_rect(x + 76, y + 26, 8, 10, NAVY)
    fill_rect(x + 110, y + 26, 8, 10, NAVY)
    line(x + 97, y + 22, x + 97, y + 12, INK, 2)
    disc(x + 97, y + 10, 3, RED)
    line(x + 84, y + 40, x + 76, y + 52, INK, 2)
    line(x + 110, y + 40, x + 118, y + 52, INK, 2)


def pic_talks(x, y, s):
    # Two speech bubbles facing each other.
    rounded_rect(x + 12, y + 22, 52, 40, 8, TINT_BLUE)
    rect_outline(x + 12, y + 22, 52, 40, NAVY, 2)
    triangle(x + 22, y + 62, x + 34, y + 62, x + 26, y + 76, NAVY)
    rounded_rect(x + s - 64, y + 66, 52, 40, 8, TINT_GOLD)
    rect_outline(x + s - 64, y + 66, 52, 40, NAVY, 2)
    triangle(x + s - 34, y + 106, x + s - 22, y + 106, x + s - 28, y + 120, NAVY)
    for i in range(3):
        fill_rect(x + 24 + i * 14, y + 38, 8, 3, NAVY)
        fill_rect(x + s - 52 + i * 14, y + 82, 8, 3, NAVY)


def pic_controller(x, y, s):
    # Game controller.
    rounded_rect(x + 14, y + 44, s - 28, 52, 16, NAVY)
    disc(x + 30, y + 96, 12, NAVY)
    disc(x + s - 30, y + 96, 12, NAVY)
    # d-pad
    fill_rect(x + 30, y + 56, 8, 26, WHITE)
    fill_rect(x + 21, y + 65, 26, 8, WHITE)
    # buttons
    disc(x + s - 44, y + 62, 5, RED)
    disc(x + s - 32, y + 72, 5, GOLD)
    disc(x + s - 56, y + 72, 5, GREEN)
    disc(x + s - 44, y + 82, 5, WHITE)
    # joysticks
    disc(x + 52, y + 82, 6, (120, 130, 150))
    disc(x + s - 66, y + 56, 6, (120, 130, 150))
    draw_text(x + 34, y + 14, "$1.8BN", 2, RED)


# -------------------------------------------------------------- stories ----
STORIES = [
    {
        "kicker": "DIPLOMACY - US / IRAN",
        "headline": "TRUMP: 'NO RUSH' ON IRAN DECISION",
        "deck": "President says he will look at it next year, Axios reports; "
                "no decision before 2027 is expected.",
        "source": "SOURCE: REUTERS / AXIOS - REPORTED 20 NOV",
        "stat": "2027",
        "stat_label": "EARLIEST EXPECTED DECISION",
        "pic": pic_flags,
        "tint": TINT_BLUE,
    },
    {
        "kicker": "WEATHER - INDIA",
        "headline": "CYCLONE AKVAN BEARS DOWN ON ODISHA",
        "deck": "Landfall due around noon; nearly 300,000 people moved to "
                "shelters as winds near 110 kmph.",
        "source": "SOURCE: IMD VIA THE HINDU - 20 NOV",
        "stat": "300,000",
        "stat_label": "PEOPLE MOVED TO SHELTERS",
        "pic": pic_cyclone,
        "tint": TINT_BLUE,
    },
    {
        "kicker": "MARKETS - TECH",
        "headline": "ANTHROPIC SHARES JUMP ON DEBUT",
        "deck": "Shares close 17% higher on their first day of trading "
                "on Nasdaq.",
        "source": "SOURCE: THE HINDU - 20 NOV",
        "stat": "+17%",
        "stat_label": "FIRST-DAY SHARE RISE",
        "pic": pic_markets,
        "tint": TINT_GOLD,
    },
    {
        "kicker": "SPACE - JAPAN",
        "headline": "HAYABUSA2 DROPS ASTEROID LANDING",
        "deck": "Engine trouble forces Japan's probe to change plans; "
                "no more asteroid landing.",
        "source": "SOURCE: SPACE.COM - 20 NOV",
        "stat": "0",
        "stat_label": "FURTHER ASTEROID LANDINGS",
        "pic": pic_space,
        "tint": TINT_BLUE,
    },
    {
        "kicker": "EUROPE - UKRAINE",
        "headline": "EUROPE READY FOR TALKS WITH RUSSIA",
        "deck": "European leaders say they are ready for talks on ending "
                "the war in Ukraine.",
        "source": "SOURCE: BBC - 20 NOV",
        "stat": "READY",
        "stat_label": "EUROPE FOR TALKS WITH RUSSIA",
        "pic": pic_talks,
        "tint": TINT_GOLD,
    },
    {
        "kicker": "CULTURE - GAMING",
        "headline": "GTA 6 SALES PASS $1.8 BILLION",
        "deck": "Rockstar's game already tops The Odyssey's global "
                "box-office run.",
        "source": "SOURCE: MEZHA - 20 NOV",
        "stat": "$1.8BN",
        "stat_label": "GTA 6 SALES SO FAR",
        "pic": pic_controller,
        "tint": TINT_RED,
    },
]


def draw_panel(x, y, w, h, story, idx):
    rect_outline(x, y, w, h, RULE, 1)
    fill_rect(x + 1, y + 1, w - 2, 3, NAVY if idx % 2 == 0 else RED)
    draw_text(x + 16, y + 14, story["kicker"], 1, RED)
    # pictogram box, right side
    px0, py0, ps = x + w - 16 - 140, y + 30, 140
    fill_rect(px0, py0, ps, ps, story["tint"])
    rect_outline(px0, py0, ps, ps, RULE, 1)
    story["pic"](px0, py0, ps)
    # headline + deck, left of pictogram
    text_w = w - 32 - 140 - 16
    draw_wrapped(x + 16, y + 34, story["headline"], 2, text_w, 17, INK, 3)
    draw_wrapped(x + 16, y + 76, story["deck"], 1, text_w, 11, DARKGRAY, 4)
    # stat band
    fill_rect(x + 16, y + 182, w - 32, 40, story["tint"])
    rect_outline(x + 16, y + 182, w - 32, 40, RULE, 1)
    draw_text(x + 28, y + 189, story["stat"], 2, NAVY)
    draw_text(x + 28, y + 208, story["stat_label"], 1, DARKGRAY)
    # source line
    draw_text(x + 16, y + h - 22, story["source"], 1, GRAY)


def draw_page():
    fill_rect(0, 0, W, H, PAPER)
    rect_outline(10, 10, W - 20, H - 20, INK, 2)
    rect_outline(16, 16, W - 32, H - 32, RULE, 1)
    # masthead
    fill_rect(24, 24, W - 48, 140, NAVY)
    fill_rect(24, 24, W - 48, 4, GOLD)
    draw_text_centered(W // 2, 42, "THE WORLD TODAY", 8, PAPER)
    fill_rect(W // 2 - 280, 106, 560, 3, GOLD)
    draw_text_centered(W // 2, 118, "FRIDAY 20 NOVEMBER 2026", 3, GOLD)
    draw_text_centered(
        W // 2, 172, "SIX STORIES FROM AROUND THE WORLD - ONE DAY IN ONE PICTURE",
        1, GRAY)
    # grid: 2 columns x 3 rows
    pw, ph, gap = 480, 256, 16
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_panel(24 + col * (pw + gap), 184 + row * (ph + gap),
                   pw, ph, story, i)
    # footer
    draw_text_centered(W // 2, 992,
                       "DRAWN PIXEL BY PIXEL BY ONE PYTHON PROGRAM - NO PHOTOS",
                       1, GRAY)


# -------------------------------------------------------------- PNG --------
def png_bytes():
    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    for yy in range(H):
        raw.append(0)
        raw.extend(fb[yy * W * 3:(yy + 1) * W * 3])
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.png")
    path = out_dir if out_dir.endswith(".png") else os.path.join(out_dir, "entry.png")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    draw_page()
    data = png_bytes()
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (path, len(data)))


if __name__ == "__main__":
    main()
