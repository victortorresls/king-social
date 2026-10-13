"""Arte dos jogos do dia com maior frequência de +3.5 gols (1080x1350).
Uso: python3 make_games_card.py games.json saida.png
games.json = {"date": "YYYY-MM-DD", "games": [{"time_utc": "HH:MM", "league": str,
  "home": str, "away": str, "p35": int, "h35": int, "a35": int, "avg": str}]}  (1 a 5 jogos)
"""
import json, sys, datetime, re
from PIL import Image, ImageDraw, ImageFont

F = "/usr/share/fonts/opentype/inter/"
def font(w, s):
    for n in (f"InterDisplay-{w}.otf", f"Inter-{w}.otf"):
        try:
            return ImageFont.truetype(F + n, s)
        except OSError:
            pass
    return ImageFont.load_default()

BG, PANEL, LINE = (10, 15, 28), (18, 26, 46), (36, 48, 78)
BLUE, BLUE2 = (37, 110, 255), (96, 156, 255)
TXT, MUTED, GREEN = (238, 242, 250), (140, 152, 178), (52, 211, 153)
W, H, M = 1080, 1350, 70

def fit(d, text, f, maxw):
    if d.textlength(text, font=f) <= maxw:
        return text
    while text and d.textlength(text + "…", font=f) > maxw:
        text = text[:-1]
    return text + "…"

def main():
    data = json.load(open(sys.argv[1]))
    games = data["games"][:5]
    day = datetime.date.fromisoformat(data["date"])
    im = Image.new("RGB", (W, H), BG)
    glow = Image.new("RGB", (W, H), BG)
    gd = ImageDraw.Draw(glow)
    for i in range(60):
        r = 900 - i * 12
        c = tuple(int(BG[k] + (BLUE[k] - BG[k]) * (i / 60) * 0.35) for k in range(3))
        gd.ellipse((W / 2 - r, -r * 0.9, W / 2 + r, r * 0.5), fill=c)
    im = Image.blend(im, glow, 0.6)
    d = ImageDraw.Draw(im)

    cx, cy = M + 22, 102
    d.polygon([(cx - 22, cy + 14), (cx - 22, cy - 10), (cx - 10, cy + 2), (cx, cy - 16),
               (cx + 10, cy + 2), (cx + 22, cy - 10), (cx + 22, cy + 14)], fill=BLUE2)
    d.text((M + 62, 82), "THE KING STATS", font=font("Bold", 38), fill=TXT)
    d.text((W - M, 88), day.strftime("%b %d").upper(), font=font("SemiBold", 30), fill=MUTED, anchor="ra")

    d.text((M, 175), "TODAY'S HIGH-GOAL GAMES", font=font("Bold", 66), fill=TXT)
    d.text((M, 262), "Over 3.5 goals frequency ≥ 70%  ·  last 10, home/away", font=font("Medium", 30), fill=BLUE2)

    n = len(games)
    top, bottom = 340, 1190
    gap = 18
    ch = min(150, (bottom - top - gap * (n - 1)) / n)
    y = top + ((bottom - top) - (ch * n + gap * (n - 1))) / 2 if n < 5 else top
    for g in games:
        d.rounded_rectangle((M, y, W - M, y + ch), 24, fill=PANEL)
        d.rectangle((M, y + 22, M + 6, y + ch - 22), fill=BLUE)
        lx = M + 34
        d.text((lx, y + 22), f"{g['time_utc']} UTC  ·  " + fit(d, re.sub(r"^\[[A-Z]{2}\] ", "", g["league"]), font("Medium", 24), 420),
               font=font("Medium", 24), fill=MUTED)
        teams = fit(d, f"{g['home']} vs {g['away']}", font("SemiBold", 36), 620)
        d.text((lx, y + 58), teams, font=font("SemiBold", 36), fill=TXT)
        d.text((lx, y + ch - 44), f"Home {g['h35']}%  ·  Away {g['a35']}%  ·  Avg goals {g['avg']}",
               font=font("Medium", 24), fill=MUTED)
        d.text((W - M - 34, y + ch / 2 - 8), f"{g['p35']}%", font=font("Bold", 72), fill=GREEN, anchor="rm")
        d.text((W - M - 34, y + ch / 2 + 40), "OVER 3.5", font=font("SemiBold", 20), fill=MUTED, anchor="rm")
        y += ch + gap

    d.text((W / 2, 1222), "Free stats for every game: thekingstats.com", font=font("Medium", 28), fill=TXT, anchor="ma")
    d.text((W / 2, 1278), "18+  ·  Historical frequency, not a guarantee  ·  Not betting advice", font=font("Medium", 22), fill=MUTED, anchor="ma")
    im.save(sys.argv[2], "PNG", optimize=True)
    print(sys.argv[2])

if __name__ == "__main__":
    main()
