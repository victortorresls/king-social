"""Gera um Reel vertical (1080x1920, 30fps) com texto animado a partir de scripts.json.
Uso: python3 make_reel.py scripts.json <id> saida.mp4
"""
import json, sys, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
F = "/usr/share/fonts/opentype/inter/"
def font(w, s):
    for n in (f"InterDisplay-{w}.otf", f"Inter-{w}.otf"):
        try:
            return ImageFont.truetype(F + n, s)
        except OSError:
            pass
    return ImageFont.load_default()

BG = (10, 15, 28); BLUE = (37, 110, 255); BLUE2 = (96, 156, 255)
TXT = (238, 242, 250); MUTED = (140, 152, 178); PANEL = (18, 26, 46)

def background():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for i in range(70):
        r = 1100 - i * 14
        c = tuple(int(BG[k] + (BLUE[k] - BG[k]) * (i / 70) * 0.30) for k in range(3))
        d.ellipse((W / 2 - r, -r * 0.7, W / 2 + r, r * 0.6), fill=c)
    return im

def crown(d, cx, cy, s=1.0, col=BLUE2):
    p = [(-22, 14), (-22, -10), (-10, 2), (0, -16), (10, 2), (22, -10), (22, 14)]
    d.polygon([(cx + x * s, cy + y * s) for x, y in p], fill=col)

def header(im):
    d = ImageDraw.Draw(im)
    crown(d, 102, 150)
    d.text((142, 128), "THE KING STATS", font=font("Bold", 40), fill=TXT)

def text_layer(text, size, color=TXT, weight="Bold", width=18):
    f = font(weight, size)
    lines = textwrap.wrap(text, width=width)
    lh = int(size * 1.18)
    layer = Image.new("RGBA", (W, lh * len(lines) + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i, ln in enumerate(lines):
        d.text((W / 2, i * lh), ln, font=f, fill=color + (255,), anchor="ma")
    return layer

def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3

def main():
    scripts = json.load(open(sys.argv[1]))
    s = next(x for x in scripts if x["id"] == int(sys.argv[2]))
    out = sys.argv[3]
    base = background()
    header(base)

    scenes = []  # (layers, duration)
    t_layer = text_layer(s["title"].upper(), 104, TXT, "Bold", 14)
    tag = text_layer("FOOTBALL STATS", 34, BLUE2, "SemiBold", 40)
    scenes.append(([(tag, -90), (t_layer, 30)], 2.6))
    for ln in s["lines"]:
        words = len(ln.split())
        size = 78 if words <= 9 else 68 if words <= 16 else 60
        wrap = 20 if size == 78 else 23 if size == 68 else 26
        scenes.append(([(text_layer(ln, size, TXT, "SemiBold", wrap), 0)], max(2.2, 0.8 + words * 0.27)))
    scenes.append(("bullets", 1.2 + 0.7 * len(s["screen"]) + 1.6))
    scenes.append(("cta", 3.4))

    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)

    total = sum(d for _, d in scenes)
    elapsed = 0.0
    for kind, dur in scenes:
        n = int(dur * FPS)
        for f in range(n):
            t = f / FPS
            fr = base.copy()
            d = ImageDraw.Draw(fr)
            # barra de progresso
            prog = (elapsed + t) / total
            d.rectangle((80, 230, W - 80, 236), fill=PANEL)
            d.rectangle((80, 230, 80 + (W - 160) * prog, 236), fill=BLUE)
            fade_out = 1 - ease((t - (dur - 0.3)) / 0.3)
            if kind == "bullets":
                items = s["screen"]
                y0 = H / 2 - len(items) * 70
                for i, it in enumerate(items):
                    a = ease((t - 0.2 - 0.7 * i) / 0.4) * fade_out
                    if a <= 0:
                        continue
                    lay = Image.new("RGBA", (W, 140), (0, 0, 0, 0))
                    ld = ImageDraw.Draw(lay)
                    ld.rounded_rectangle((90, 10, W - 90, 120), 26, fill=PANEL + (255,))
                    ld.rectangle((90, 30, 98, 100), fill=BLUE + (255,))
                    ld.text((130, 65), it, font=font("SemiBold", 48 if max(len(x) for x in items) < 30 else 40), fill=TXT + (255,), anchor="lm")
                    lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
                    fr.paste(lay, (int(40 * (1 - a)), int(y0 + i * 140)), lay)
            elif kind == "cta":
                a = ease(t / 0.5)
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ld = ImageDraw.Draw(lay)
                crown(ld, W / 2, 640, 3.2)
                ld.text((W / 2, 760), "THE KING STATS", font=font("Bold", 92), fill=TXT + (255,), anchor="ma")
                cta = text_layer(s["cta"], 56, BLUE2, "SemiBold", 26)
                lay.paste(cta, (0, 920), cta)
                ld.rounded_rectangle((W / 2 - 300, 1180, W / 2 + 300, 1290), 55, fill=BLUE + (255,))
                ld.text((W / 2, 1235), "thekingstats.com", font=font("Bold", 50), fill=(255, 255, 255, 255), anchor="mm")
                ld.text((W / 2, 1720), "18+ · Statistical analysis, not betting advice", font=font("Medium", 30), fill=MUTED + (255,), anchor="ma")
                lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
                fr.paste(lay, (0, int(30 * (1 - a))), lay)
            else:
                a = ease(t / 0.45) * fade_out
                heights = sum(l.height for l, _ in kind)
                y = H / 2 - heights / 2
                for lay, dy in kind:
                    l2 = lay.copy()
                    l2.putalpha(l2.getchannel("A").point(lambda v: int(v * a)))
                    fr.paste(l2, (0, int(y + dy + 50 * (1 - a))), l2)
                    y += lay.height
            ff.stdin.write(fr.tobytes())
        elapsed += dur
    ff.stdin.close()
    ff.wait()
    print(out, f"{total:.1f}s")

if __name__ == "__main__":
    main()
