#!/usr/bin/env python3
"""Builds assets/hero.svg: self-typing ASCII portrait + terminal intro. No external services.
Usage: python3 scripts/build_hero.py   (reads assets/portrait.txt)"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
portrait = (ROOT / "assets" / "portrait.txt").read_text().split("\n")
while portrait and not portrait[-1].strip():
    portrait.pop()

# ---- layout -------------------------------------------------------------
W, H = 900, 560
PANEL, BORDER = "#0d1117", "#30363d"
P_FS, P_CW, P_LH = 8.0, 4.9, 9.0          # portrait font size / char width / line height
P_X, P_Y = 26, 26
T_X = 482                                    # terminal column x
T_FS, T_CW, T_LH = 14, 8.4, 25

# ---- terminal script: (kind, text) -------------------------------------
script = [
    ("cmd", "whoami"),
    ("out", "Dhanika Jagodaarachchi", "hl"),
    ("gap",),
    ("cmd", "cat role.txt"),
    ("out", "Full-Stack Software Engineer", "txt"),
    ("out", "intern / junior  ·  open to work", "dim"),
    ("gap",),
    ("cmd", "cat stack.txt"),
    ("out", "Java · Spring Boot · TypeScript", "txt"),
    ("out", "React · React Native · Android", "txt"),
    ("gap",),
    ("cmd", "cat now.txt"),
    ("out", "Shipping a production e-commerce", "txt"),
    ("out", "platform for a real client", "txt"),
    ("gap",),
    ("cmd", "cat location.txt"),
    ("out", "Sri Lanka  ·  UTC+5:30  ·  remote-friendly", "dim"),
]

out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
  f'aria-label="ASCII portrait of Dhanika and a terminal intro: full-stack software engineer, open to an internship or junior roles">')
a('<defs>')
a('<linearGradient id="pg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#58e6aa"/><stop offset="1" stop-color="#79c0ff"/></linearGradient>')
a('<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#58e6aa" stop-opacity="0"/><stop offset=".5" stop-color="#58e6aa" stop-opacity=".22"/><stop offset="1" stop-color="#58e6aa" stop-opacity="0"/></linearGradient>')
a(f'<clipPath id="pclip"><rect x="0" y="0" width="{T_X-18}" height="{H}"/></clipPath>')
a('</defs>')
a('<style>')
a("text{font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,'DejaVu Sans Mono',monospace;white-space:pre}")
a('.pl{fill:url(#pg);opacity:0;animation:show .25s ease-out forwards}')
a('.cover{fill:%s;transform-box:fill-box;animation:wipe var(--d,1s) steps(var(--n,10),end) var(--t,0s) forwards}' % PANEL)
a('.scan{animation:sweep 5.5s linear 3s infinite;transform:translateY(-40px)}')
a('.cur{animation:blink 1s steps(1) infinite}')
a('.prompt{fill:#58e6aa}.txt{fill:#c9d1d9}.hl{fill:#79c0ff;font-weight:700}.dim{fill:#8b949e}')
a('@keyframes show{to{opacity:1}}')
a('@keyframes wipe{to{transform:translateX(104%)}}')
a('@keyframes sweep{to{transform:translateY(%dpx)}}' % (H + 40))
a('@keyframes blink{50%{opacity:0}}')
a('@media (prefers-reduced-motion:reduce){.pl{opacity:1;animation:none}.cover,.scan{display:none}.cur{animation:none}}')
a('</style>')

a(f'<rect width="{W}" height="{H}" rx="14" fill="{PANEL}"/>')

# ---- portrait -----------------------------------------------------------
a('<g clip-path="url(#pclip)">')
for i, line in enumerate(portrait):
    if not line.strip():
        continue
    a(f'<text class="pl" x="{P_X}" y="{P_Y + i*P_LH:.2f}" font-size="{P_FS}" textLength="{len(line)*P_CW:.1f}" '
      f'lengthAdjust="spacing" style="animation-delay:{0.25 + i*0.045:.3f}s" xml:space="preserve">{escape(line)}</text>')
a(f'<rect class="scan" x="0" y="0" width="{T_X-18}" height="36" fill="url(#scan)"/>')
a('</g>')

# ---- divider + terminal chrome -----------------------------------------
a(f'<line x1="{T_X-18}" y1="22" x2="{T_X-18}" y2="{H-22}" stroke="{BORDER}"/>')
for k, c in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
    a(f'<circle cx="{T_X+6+k*20}" cy="30" r="6" fill="{c}"/>')
a(f'<text x="{T_X+84}" y="34" font-size="12" class="dim">dhanika@portfolio: ~</text>')

# ---- terminal typing ----------------------------------------------------
y, t = 88, 0.6
a('<g>')
for item in script:
    kind = item[0]
    if kind == "gap":
        y += T_LH * 0.6
        t += 0.12
        continue
    if kind == "cmd":
        txt = item[1]
        n = len(txt) + 2
        dur = n * 0.045
        a(f'<text x="{T_X}" y="{y:.1f}" font-size="{T_FS}" textLength="{2*T_CW:.1f}" lengthAdjust="spacing" class="prompt">$ </text>')
        a(f'<text x="{T_X+2*T_CW:.1f}" y="{y:.1f}" font-size="{T_FS}" class="txt" textLength="{len(txt)*T_CW:.1f}" lengthAdjust="spacing">{escape(txt)}</text>')
        wid = n * T_CW
        a(f'<rect class="cover" x="{T_X-2}" y="{y-T_FS-2:.1f}" width="{wid+6:.1f}" height="{T_LH}" style="--n:{n};--d:{dur:.2f}s;--t:{t:.2f}s"/>')
        t += dur + 0.2
    else:
        txt, cls = item[1], item[2]
        n = len(txt)
        dur = n * 0.02
        a(f'<text x="{T_X}" y="{y:.1f}" font-size="{T_FS}" class="{cls}" textLength="{n*T_CW:.1f}" lengthAdjust="spacing">{escape(txt)}</text>')
        a(f'<rect class="cover" x="{T_X-2}" y="{y-T_FS-2:.1f}" width="{n*T_CW+6:.1f}" height="{T_LH}" style="--n:{n};--d:{dur:.2f}s;--t:{t:.2f}s"/>')
        t += dur + 0.06
    y += T_LH
# final prompt with blinking cursor
a(f'<text x="{T_X}" y="{y+T_LH*0.6:.1f}" font-size="{T_FS}" class="prompt" textLength="{2*T_CW}" lengthAdjust="spacing">$ </text>')
a(f'<rect class="cur" x="{T_X+2*T_CW+2:.1f}" y="{y+T_LH*0.6-T_FS+1:.1f}" width="8" height="{T_FS+2}" fill="#58e6aa"/>')
a('</g>')

# frame on top so moving covers never erase the border
a(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{BORDER}"/>')
a('</svg>')

(ROOT / "assets" / "hero.svg").write_text("\n".join(out))
print("hero.svg", len("\n".join(out)) // 1024, "KB; typing ends ~%.1fs" % t)
