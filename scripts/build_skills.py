#!/usr/bin/env python3
"""Builds assets/skills.svg: grouped, animated skill chips (self-hosted, no badge servers)."""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "skills.svg"
GROUPS = [   # only skills evidenced by public repos; add more as you ship them
    ("Backend",  "#58e6aa", ["Java", "Spring Boot", "REST APIs"]),
    ("Frontend", "#79c0ff", ["TypeScript", "React", "React Native", "HTML / CSS"]),
    ("Mobile",   "#d2a8ff", ["Android"]),
    ("Tooling",  "#ffa657", ["Git & GitHub", "GitHub Actions"]),
]
W, CH, PAD, GAP, ROW = 900, 30, 14, 10, 52
y = 44
body, delay = [], 0.0
for title, color, items in GROUPS:
    body.append(f'<text x="36" y="{y+5}" class="g" fill="{color}">{escape(title)}</text>')
    x = 150
    for it in items:
        w = len(it) * 8.2 + PAD * 2
        if x + w > W - 30:
            x, y = 150, y + CH + 10
        body.append(f'<g class="chip" style="animation-delay:{delay:.2f}s"><rect x="{x}" y="{y-CH/2:.0f}" width="{w:.0f}" height="{CH}" rx="15" fill="{color}" fill-opacity=".10" stroke="{color}" stroke-opacity=".55"/>'
                    f'<text x="{x+w/2:.0f}" y="{y+4}" text-anchor="middle" class="c">{escape(it)}</text></g>')
        x += w + GAP; delay += 0.05
    y += ROW
H = y - 4
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Skills: Java, Spring Boot, TypeScript, React, React Native, Android, Git">'
       '<style>text{font-family:Consolas,Menlo,"DejaVu Sans Mono",monospace}.g{font-size:13px;font-weight:700}.c{font-size:13px;fill:#c9d1d9}'
       '.chip{opacity:0;animation:pop .5s cubic-bezier(.2,.9,.3,1.2) forwards;transform-box:fill-box;transform-origin:center}'
       '@keyframes pop{from{opacity:0;transform:translateY(8px) scale(.92)}to{opacity:1;transform:none}}'
       '@media (prefers-reduced-motion:reduce){.chip{opacity:1;animation:none}}</style>'
       f'<rect width="{W}" height="{H}" rx="14" fill="#0d1117" stroke="#30363d"/>' + "".join(body) + '</svg>')
OUT.write_text(svg); print("wrote", OUT, f"{W}x{H}")
