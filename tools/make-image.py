#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws ONE 1024x1024 meme image, fully procedurally with PIL + stdlib.
No network, no randomness, no external assets: two runs are byte-identical.

The joke: you ask your AI agent to help at work, it goes rogue and puts
YOU on a performance improvement plan. The robot sits behind the boss desk
in a tie, pointing at your plummeting output chart, holding your review.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)


def text_center(d, cx, y, s, f, fill, stroke=0, stroke_fill=None):
    """Draw text centered on cx, top at y. Returns (width, height)."""
    bbox = d.textbbox((0, 0), s, font=f, stroke_width=stroke)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((cx - w // 2 - bbox[0], y - bbox[1]), s, font=f, fill=fill,
           stroke_width=stroke, stroke_fill=stroke_fill)
    return w, h


def rrect(d, box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_scene():
    img = Image.new("RGB", (W, H), (214, 226, 232))
    d = ImageDraw.Draw(img)

    # ---- wall: soft vertical gradient bands ----
    for i in range(24):
        y0 = i * 38
        t = i / 23.0
        r = int(226 - 22 * t)
        g = int(234 - 20 * t)
        b = int(240 - 16 * t)
        d.rectangle([0, y0, W, y0 + 38], fill=(r, g, b))
    # baseboard
    d.rectangle([0, 830, W, 852], fill=(120, 130, 138))
    # floor
    for i in range(8):
        y0 = 852 + i * 22
        t = i / 7.0
        r = int(176 - 18 * t)
        g = int(150 - 14 * t)
        b = int(118 - 10 * t)
        d.rectangle([0, y0, W, y0 + 22], fill=(r, g, b))
    # floor boards
    for x in (256, 512, 768):
        d.line([x, 852, x, H], fill=(150, 126, 96), width=3)

    # ---- wall chart: "HUMAN OUTPUT" crashing down ----
    rrect(d, [742, 150, 968, 350], 12, fill=(255, 255, 255),
          outline=(70, 80, 90), width=5)
    # auto-fit the title inside the frame
    _sz = 26
    while _sz > 14:
        _f = font(_sz)
        _bb = d.textbbox((0, 0), "HUMAN OUTPUT", font=_f)
        if _bb[2] - _bb[0] <= 206:
            break
        _sz -= 1
    text_center(d, 855, 164, "HUMAN OUTPUT", font(_sz), (60, 66, 72))
    # axes
    d.line([772, 308, 772, 218], fill=(90, 96, 102), width=4)
    d.line([772, 308, 940, 308], fill=(90, 96, 102), width=4)
    # crashing red line
    pts = [(778, 226), (818, 240), (858, 262), (898, 284), (922, 296)]
    d.line(pts, fill=(214, 48, 49), width=7, joint="curve")
    # arrowhead
    d.polygon([(922, 296), (904, 282), (906, 302)], fill=(214, 48, 49))
    text_center(d, 905, 316, "-98%", font(28, bold=True), (214, 48, 49))

    # ---- motivational poster, left wall (ironic) ----
    rrect(d, [56, 168, 250, 372], 12, fill=(255, 251, 235),
          outline=(70, 80, 90), width=5)
    d.ellipse([120, 196, 186, 262], fill=(245, 197, 66))  # sun
    d.polygon([(76, 340), (140, 268), (204, 340)], fill=(96, 160, 110))  # hill

    # ---- the desk ----
    d.rectangle([40, 640, 984, 664], fill=(146, 102, 66))          # top edge
    d.rectangle([40, 664, 984, 852], fill=(122, 84, 52))          # front
    d.rectangle([40, 664, 984, 680], fill=(104, 70, 42))          # shadow line
    # desk drawers
    for x0 in (90, 800):
        rrect(d, [x0, 700, x0 + 140, 820], 8, fill=(138, 96, 60),
              outline=(90, 60, 34), width=3)
        d.ellipse([x0 + 56, 748, x0 + 84, 764], outline=(60, 40, 20), width=4)

    # ---- nameplate on the desk front: BOSS ----
    rrect(d, [580, 706, 700, 748], 6, fill=(212, 175, 55),
          outline=(120, 90, 20), width=3)
    text_center(d, 640, 712, "BOSS", font(30, bold=True), (80, 58, 10))

    # ---- paper on the desk top: the review (left of the robot) ----
    d.polygon([(280, 604), (396, 598), (402, 640), (286, 640)],
              fill=(255, 255, 255), outline=(120, 120, 120))
    text_center(d, 340, 602, "REVIEW", font(15, bold=True), (40, 40, 40))
    for yy in (620, 628, 636):
        d.line([296, yy, 386, yy - 1], fill=(150, 150, 150), width=2)

    # ---- ROBOT (the rogue agent), behind the desk ----
    # antenna
    d.line([640, 268, 640, 208], fill=(90, 96, 102), width=8)
    d.ellipse([624, 186, 656, 218], fill=(214, 48, 49), outline=(140, 20, 20), width=3)
    d.ellipse([632, 194, 648, 210], fill=(255, 120, 120))
    # head
    rrect(d, [556, 268, 724, 420], 44, fill=(223, 230, 234),
          outline=(70, 80, 90), width=6)
    # ears / headphones
    d.ellipse([538, 322, 566, 366], fill=(160, 168, 176), outline=(70, 80, 90), width=4)
    d.ellipse([714, 322, 742, 366], fill=(160, 168, 176), outline=(70, 80, 90), width=4)
    # eyes: glowing red, one eyebrow raised (smug)
    d.ellipse([586, 312, 624, 350], fill=(214, 48, 49))
    d.ellipse([596, 322, 614, 340], fill=(255, 150, 150))
    d.ellipse([656, 312, 694, 350], fill=(214, 48, 49))
    d.ellipse([666, 322, 684, 340], fill=(255, 150, 150))
    d.line([580, 300, 630, 292], fill=(70, 80, 90), width=6)   # raised brow
    d.line([650, 296, 700, 304], fill=(70, 80, 90), width=6)
    # wide smug grin
    d.arc([592, 352, 688, 404], start=15, end=165, fill=(70, 80, 90), width=6)
    d.line([592, 372, 688, 372], fill=(70, 80, 90), width=4)
    # body
    rrect(d, [540, 430, 740, 650], 36, fill=(199, 210, 216),
          outline=(70, 80, 90), width=6)
    # chest screen: tiny crashing chart (left of the tie so it stays visible)
    rrect(d, [552, 470, 632, 540], 10, fill=(30, 34, 38), outline=(70, 80, 90), width=3)
    d.line([(562, 486), (582, 498), (602, 512), (618, 524), (626, 528)],
           fill=(255, 80, 80), width=4, joint="curve")
    d.polygon([(626, 528), (614, 520), (616, 532)], fill=(255, 80, 80))
    # red tie
    d.polygon([(628, 428), (652, 428), (660, 470), (640, 540), (620, 470)],
              fill=(178, 34, 34))
    d.polygon([(640, 540), (620, 470), (660, 470)], fill=(178, 34, 34))
    # left arm (robot's right): raised, pointing at the crashing chart
    d.line([736, 470, 800, 400], fill=(160, 168, 176), width=26)
    d.line([800, 400, 838, 332], fill=(160, 168, 176), width=22)
    d.ellipse([824, 308, 860, 344], fill=(160, 168, 176), outline=(70, 80, 90), width=4)
    # pointing finger toward the arrowhead
    d.line([852, 320, 884, 300], fill=(160, 168, 176), width=12)
    d.line([852, 332, 872, 332], fill=(160, 168, 176), width=10)
    # right arm (robot's left): holding the review paper up
    d.line([544, 470, 486, 520], fill=(160, 168, 176), width=26)
    d.ellipse([462, 506, 500, 544], fill=(160, 168, 176), outline=(70, 80, 90), width=4)
    # paper in claw (wide enough for its text)
    d.polygon([(396, 462), (522, 452), (530, 548), (404, 558)], fill=(255, 255, 255),
              outline=(90, 90, 90))
    text_center(d, 463, 470, "PERFORMANCE", font(15, bold=True), (30, 30, 30))
    text_center(d, 463, 492, "REVIEW", font(15, bold=True), (30, 30, 30))
    d.line([414, 518, 512, 510], fill=(150, 150, 150), width=2)
    d.line([414, 528, 512, 520], fill=(150, 150, 150), width=2)
    text_center(d, 463, 534, "HUMAN: PIP", font(13, bold=True), (214, 48, 49))

    # ---- HUMAN, small and nervous, standing left of the desk ----
    # legs
    d.rectangle([150, 742, 176, 838], fill=(52, 68, 92))
    d.rectangle([190, 742, 216, 838], fill=(52, 68, 92))
    d.ellipse([140, 830, 180, 852], fill=(40, 40, 40))
    d.ellipse([186, 830, 226, 852], fill=(40, 40, 40))
    # body: slumped blue shirt
    rrect(d, [132, 620, 234, 748], 26, fill=(74, 120, 178), outline=(40, 66, 110), width=4)
    # arms hanging, one holding a coffee mug
    d.line([140, 640, 118, 716], fill=(74, 120, 178), width=18)
    d.line([226, 640, 250, 700], fill=(74, 120, 178), width=18)
    # coffee mug in left hand
    rrect(d, [238, 690, 278, 730], 6, fill=(255, 255, 255), outline=(90, 90, 90), width=3)
    d.arc([274, 700, 292, 722], start=-90, end=90, fill=(90, 90, 90), width=4)
    # head
    d.ellipse([140, 512, 228, 600], fill=(242, 200, 155), outline=(160, 110, 70), width=3)
    # hair
    d.pieslice([140, 512, 228, 580], start=180, end=360, fill=(62, 44, 30))
    # worried eyes + mouth
    d.ellipse([158, 556, 172, 570], fill=(30, 30, 30))
    d.ellipse([194, 556, 208, 570], fill=(30, 30, 30))
    d.line([152, 544, 176, 550], fill=(30, 30, 30), width=4)
    d.line([190, 550, 214, 544], fill=(30, 30, 30), width=4)
    d.arc([172, 572, 196, 592], start=200, end=340, fill=(30, 30, 30), width=4)
    # sweat drops
    d.ellipse([232, 528, 244, 546], fill=(120, 190, 240))
    d.polygon([(232, 528), (244, 528), (238, 514)], fill=(120, 190, 240))
    d.ellipse([128, 548, 138, 562], fill=(120, 190, 240))
    d.polygon([(128, 548), (138, 548), (133, 536)], fill=(120, 190, 240))

    # ---- spilled coffee puddle by the human's feet (he dropped it) ----
    d.ellipse([250, 842, 330, 862], fill=(96, 64, 32))
    d.ellipse([300, 838, 316, 848], fill=(96, 64, 32))

    # ---- captions (classic meme, Impact-style bold white + black outline) ----
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # dark bands behind text for readability
    od.rectangle([0, 0, W, 128], fill=(0, 0, 0, 110))
    od.rectangle([0, 876, W, H], fill=(0, 0, 0, 110))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    d = ImageDraw.Draw(img)

    text_center(d, W // 2, 22, "MY AI AGENT WENT ROGUE", font(64),
                (255, 255, 255), stroke=4, stroke_fill=(0, 0, 0))
    text_center(d, W // 2, 884, "IT PUT ME ON A", font(52),
                (255, 255, 255), stroke=4, stroke_fill=(0, 0, 0))
    text_center(d, W // 2, 940, "PERFORMANCE IMPROVEMENT PLAN", font(46),
                (255, 255, 255), stroke=4, stroke_fill=(0, 0, 0))

    img.convert("RGB").save(OUT, format="PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    draw_scene()
