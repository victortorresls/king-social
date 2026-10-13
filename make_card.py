"""Gera o card semanal de resultados do mês para o Instagram (1080x1350).
Uso: python3 make_card.py dados.json saida.png
dados.json = resposta de https://thekingstats.com/api/dashboard-resumo
"""
import json, sys, calendar, datetime
from PIL import Image, ImageDraw, ImageFont

F = "/usr/share/fonts/opentype/inter/"
def font(w, s):
    for name in (f"InterDisplay-{w}.otf", f"Inter-{w}.otf"):
        try:
            return ImageFont.truetype(F + name, s)
        except OSError:
            pass
    return ImageFont.load_default()

BG, PANEL, LINE = (10, 15, 28), (18, 26, 46), (36, 48, 78)
BLUE, BLUE2 = (37, 110, 255), (96, 156, 255)
TXT, MUTED = (238, 242, 250), (140, 152, 178)
GREEN, RED = (52, 211, 153), (248, 113, 113)

data = json.load(open(sys.argv[1]))
out = sys.argv[2]
d = data["desempenho"]
dias = data["dias"]
last = datetime.date.fromisoformat(dias[-1]["day"])
month = calendar.month_name[last.month].upper()
units = d["units"]
pos = sum(1 for x in dias if x["units"] > 0)

W, H = 1080, 1350
im = Image.new("RGB", (W, H), BG)
dr = ImageDraw.Draw(im)

# brilho azul no topo
glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
for i in range(60):
    r = 900 - i * 12
    c = tuple(int(BG[k] + (BLUE[k] - BG[k]) * (i / 60) * 0.35) for k in range(3))
    gd.ellipse((W / 2 - r, -r * 0.9, W / 2 + r, r * 0.55), fill=c)
im = Image.blend(im, glow, 0.6)
dr = ImageDraw.Draw(im)

M = 80
# coroa simples + marca
cx, cy = M + 22, 112
dr.polygon([(cx - 22, cy + 14), (cx - 22, cy - 10), (cx - 10, cy + 2), (cx, cy - 16),
            (cx + 10, cy + 2), (cx + 22, cy - 10), (cx + 22, cy + 14)], fill=BLUE2)
dr.text((M + 62, 92), "THE KING STATS", font=font("Bold", 38), fill=TXT)
dr.text((W - M, 98), "thekingstats.com", font=font("Medium", 28), fill=MUTED, anchor="ra")

dr.text((M, 220), f"{month} SO FAR", font=font("SemiBold", 40), fill=BLUE2)
sign = "+" if units >= 0 else ""
dr.text((M - 6, 268), f"{sign}{units:.2f}u", font=font("Bold", 210), fill=TXT)
dr.text((M, 520), f"{pos} of {len(dias)} days positive", font=font("Medium", 42), fill=MUTED)

# gráfico diário
top, bot = 610, 960
dr.rounded_rectangle((M, top, W - M, bot), 28, fill=PANEL)
px0, px1, py0, py1 = M + 40, W - M - 40, top + 50, bot - 70
mx = max(abs(x["units"]) for x in dias) or 1
zero = (py0 + py1) / 2
dr.line((px0, zero, px1, zero), fill=LINE, width=2)
n = len(dias)
slot = (px1 - px0) / max(n, 1)
bw = min(46, slot * 0.62)
for i, x in enumerate(dias):
    xc = px0 + slot * (i + 0.5)
    h = (x["units"] / mx) * (py1 - py0) / 2
    y0, y1 = sorted((zero, zero - h))
    if abs(y1 - y0) < 3:
        y1 = y0 + 3
    dr.rounded_rectangle((xc - bw / 2, y0, xc + bw / 2, y1), 6, fill=GREEN if x["units"] >= 0 else RED)
    dr.text((xc, bot - 52), str(int(x["day"][-2:])), font=font("Medium", 22), fill=MUTED, anchor="ma")
dr.text((M + 40, top + 18), "Daily units", font=font("SemiBold", 24), fill=MUTED)

# contadores
labels = [("GREENS", d["greens"], GREEN), ("REDS", d["reds"], RED), ("VOIDS", d["voids"], MUTED)]
cw = (W - 2 * M - 40) / 3
for i, (lab, val, col) in enumerate(labels):
    x0 = M + i * (cw + 20)
    dr.rounded_rectangle((x0, 1000, x0 + cw, 1150), 24, fill=PANEL)
    dr.text((x0 + cw / 2, 1022), str(val), font=font("Bold", 64), fill=col, anchor="ma")
    dr.text((x0 + cw / 2, 1102), lab, font=font("SemiBold", 24), fill=MUTED, anchor="ma")

dr.text((W / 2, 1200), "Every selection tracked by the model. No edits.", font=font("Medium", 28), fill=TXT, anchor="ma")
dr.text((W / 2, 1268), "18+  ·  Statistical analysis, not betting advice", font=font("Medium", 24), fill=MUTED, anchor="ma")
im.save(out, "PNG", optimize=True)
print(out)
