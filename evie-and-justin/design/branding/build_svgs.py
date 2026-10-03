#!/usr/bin/env python3
"""Generates the branding SVG mockups. Run: python3 build_svgs.py  (no dependencies).
Mockups only: simple vector placeholders for layout/colour. Real logo art = redraw from the approved character sheets."""
FONT = "'Fredoka','Baloo 2','Nunito','Trebuchet MS',sans-serif"
C = dict(cream="#FFF1D6", gold="#EBA02B", sun="#FFC76B", indigo="#2B2D52", plum="#5B4A6B",
         sky="#8EC8F0", peach="#FFD9A8", rose="#F2A5A0", evie="#B3203C", justin="#3C8A1C",
         eviefur="#F5EFE9", justinfur="#2A1A14", blue="#0A67A0", teal="#3FA7A6")

def svg(w, h, body, title, bg=None, extra_defs=""):
    bgrect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title.replace("&","&amp;")}">
<title>{title.replace("&","&amp;")}</title>
<defs>{DEFS}{extra_defs}</defs>
{bgrect}
{body}
</svg>
'''

DEFS = f'''
<g id="evie-head">
  <path d="M-62,-30 L-70,-92 Q-68,-100 -60,-96 L-22,-62 Z" fill="{C['eviefur']}"/>
  <path d="M62,-30 L70,-92 Q68,-100 60,-96 L22,-62 Z" fill="{C['eviefur']}"/>
  <path d="M-58,-44 L-62,-80 L-34,-60 Z" fill="#F3A38F"/>
  <path d="M58,-44 L62,-80 L34,-60 Z" fill="#F3A38F"/>
  <ellipse cx="0" cy="0" rx="82" ry="70" fill="{C['eviefur']}"/>
  <path d="M-66,-44 Q-48,-86 -22,-66 Q-34,-52 -46,-34 Q-58,-30 -66,-44 Z" fill="#1A1412"/>
  <circle cx="-30" cy="4" r="18" fill="#fff"/><circle cx="30" cy="4" r="18" fill="#fff"/>
  <circle cx="-28" cy="6" r="13" fill="{C['blue']}"/><circle cx="32" cy="6" r="13" fill="{C['blue']}"/>
  <circle cx="-28" cy="6" r="7" fill="#05080C"/><circle cx="32" cy="6" r="7" fill="#05080C"/>
  <circle cx="-24" cy="0" r="3.5" fill="#fff"/><circle cx="36" cy="0" r="3.5" fill="#fff"/>
  <path d="M-6,30 L6,30 L0,38 Z" fill="#F2958A"/>
  <path d="M-14,44 Q0,56 14,44" fill="none" stroke="#7a4a44" stroke-width="3.5" stroke-linecap="round"/>
  <circle cx="-52" cy="30" r="9" fill="#F7C2B3" opacity=".7"/><circle cx="52" cy="30" r="9" fill="#F7C2B3" opacity=".7"/>
</g>
<g id="justin-head">
  <path d="M-62,-30 L-70,-92 Q-68,-100 -60,-96 L-22,-62 Z" fill="{C['justinfur']}"/>
  <path d="M62,-30 L70,-92 Q68,-100 60,-96 L22,-62 Z" fill="{C['justinfur']}"/>
  <path d="M-58,-44 L-62,-80 L-34,-60 Z" fill="#EBA591"/>
  <path d="M58,-44 L62,-80 L34,-60 Z" fill="#EBA591"/>
  <ellipse cx="0" cy="0" rx="86" ry="70" fill="{C['justinfur']}"/>
  <circle cx="-30" cy="4" r="19" fill="#FBF4EE"/><circle cx="30" cy="4" r="19" fill="#FBF4EE"/>
  <circle cx="-28" cy="6" r="13" fill="#3F8A1E"/><circle cx="32" cy="6" r="13" fill="#3F8A1E"/>
  <circle cx="-28" cy="6" r="7" fill="#05080C"/><circle cx="32" cy="6" r="7" fill="#05080C"/>
  <circle cx="-24" cy="0" r="3.5" fill="#fff"/><circle cx="36" cy="0" r="3.5" fill="#fff"/>
  <path d="M-6,30 L6,30 L0,38 Z" fill="#B9564A"/>
  <path d="M-14,44 Q0,56 14,44" fill="none" stroke="#b9a89a" stroke-width="3.5" stroke-linecap="round"/>
</g>
<g id="tag">
  <circle r="26" fill="{C['gold']}" stroke="#B8700A" stroke-width="3"/>
  <ellipse cx="0" cy="6" rx="9" ry="8" fill="#B8700A"/>
  <circle cx="-11" cy="-6" r="4" fill="#B8700A"/><circle cx="-4" cy="-13" r="4" fill="#B8700A"/>
  <circle cx="4" cy="-13" r="4" fill="#B8700A"/><circle cx="11" cy="-6" r="4" fill="#B8700A"/>
</g>
<g id="pair">
  <use href="#evie-head" x="-78" y="0" transform="rotate(-6 -78 0)"/>
  <use href="#justin-head" x="78" y="10" transform="rotate(6 78 10)"/>
  <path d="M-130,64 Q-78,92 -30,70" fill="none" stroke="{C['evie']}" stroke-width="9" stroke-linecap="round"/>
  <path d="M30,80 Q80,104 134,76" fill="none" stroke="#22160F" stroke-width="9" stroke-linecap="round"/>
  <use href="#tag" x="-76" y="100" transform="scale(.7) translate(-32 43)"/>
  <use href="#tag" x="82" y="108" transform="scale(.7) translate(35 46)"/>
</g>
<g id="badge">
  <circle r="380" fill="{C['cream']}"/>
  <circle r="380" fill="none" stroke="{C['gold']}" stroke-width="20"/>
  <path d="M-380,120 Q0,40 380,120 L380,0 A380,380 0 0 0 -380,0 Z" fill="none"/>
  <clipPath id="bclip"><circle r="368"/></clipPath>
  <g clip-path="url(#bclip)">
    <rect x="-380" y="-380" width="760" height="470" fill="{C['sky']}"/>
    <rect x="-380" y="-60" width="760" height="150" fill="{C['peach']}" opacity=".85"/>
    <circle cx="150" cy="-40" r="70" fill="{C['sun']}"/>
    <rect x="-380" y="90" width="760" height="290" fill="#8CBF6A"/>
    <rect x="-380" y="80" width="760" height="20" fill="{C['teal']}"/>
    <use href="#pair" transform="translate(0 30) scale(1.75)"/>
  </g>
</g>
'''

def txt(x, y, s, size, fill, weight=700, anchor="middle", extra=""):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'

def wordmark(cx, y1, size, dark=True):
    col = C['indigo'] if dark else C['cream']
    return (txt(cx, y1, "Evie &amp; Justin's", size, col, 700) +
            txt(cx, y1 + size*0.86, "Little Adventures", size*0.62, C['gold'] if dark else C['sun'], 600, extra='letter-spacing="2"'))

files = {}
# 1 avatar badge 800x800
files['logo-badge.svg'] = svg(800, 800, '<g transform="translate(400 400) scale(1)"><use href="#badge"/></g>'.replace('scale(1)','scale(1.03)'), "Evie & Justin badge logo (mockup)", C['cream'])
# 2 wordmark horizontal
files['logo-wordmark.svg'] = svg(1800, 600,
    '<g transform="translate(300 300) scale(.72)"><use href="#badge"/></g>' + wordmark(1130, 280, 150) +
    f'<rect x="640" y="400" width="980" height="8" rx="4" fill="{C["gold"]}"/>', "Evie & Justin's Little Adventures wordmark (mockup)", C['cream'])
# 3 banner 2560x1440
files['banner.svg'] = svg(2560, 1440,
    f'<rect width="2560" height="1440" fill="url(#sky)"/>' +
    f'<circle cx="1900" cy="640" r="190" fill="{C["sun"]}"/>' +
    f'<path d="M0,900 Q500,820 1000,880 T2000,860 T2560,880 L2560,1440 L0,1440 Z" fill="#9CC657"/>' +
    f'<path d="M0,1010 Q700,950 1400,1010 T2560,990 L2560,1440 L0,1440 Z" fill="#8CBF6A"/>' +
    f'<rect x="0" y="880" width="2560" height="26" fill="{C["teal"]}" opacity=".8"/>' +
    f'<g transform="translate(1280 520)">' + wordmark(0, 0, 150, True).replace(C['indigo'], C['indigo']) + '</g>' +
    f'<g transform="translate(640 760) scale(1.2)"><use href="#pair"/></g>' +
    f'<g transform="translate(1920 760) scale(1.2)"><use href="#pair"/></g>' +
    txt(1280, 1010, "A tiny adventure to a big place, every week", 52, C['indigo'], 500) +
    f'<g id="safe-area-guide" display="none"><rect x="507" y="508" width="1546" height="423" fill="none" stroke="red" stroke-width="4" stroke-dasharray="20 12"/></g>',
    "YouTube banner 2560x1440 (mockup). Safe area 1546x423 centred, set display=inline on #safe-area-guide to check.", C['sky'],
    f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["sky"]}"/><stop offset=".62" stop-color="{C["peach"]}"/></linearGradient>')
# 4 thumbnail template 1280x720
files['thumbnail-template.svg'] = svg(1280, 720,
    f'<rect width="1280" height="720" fill="url(#tsky)"/>' +
    f'<rect y="470" width="1280" height="250" fill="#8CBF6A"/><rect y="462" width="1280" height="16" fill="{C["teal"]}"/>' +
    f'<text x="40" y="60" font-family="{FONT}" font-size="26" fill="{C["indigo"]}" opacity=".6">[ BACKGROUND: episode location, golden hour, no text, lower third clear ]</text>' +
    f'<g transform="translate(300 470) scale(1.45)"><use href="#pair"/></g>' +
    f'<rect x="20" y="20" width="1240" height="680" rx="26" fill="none" stroke="{C["teal"]}" stroke-width="16"/>' +
    f'<g><rect x="60" y="70" width="560" height="190" rx="28" fill="{C["cream"]}" opacity=".92"/>' +
    txt(340, 160, "TITLE LINE", 80, C['indigo'], 700) + txt(340, 232, "(max 3 words, 2 lines)", 46, C['plum'], 500) + '</g>' +
    f'<g transform="translate(1130 130) scale(1.1)"><circle r="82" fill="{C["gold"]}"/><text y="14" font-family="{FONT}" font-size="46" font-weight="700" fill="{C["indigo"]}" text-anchor="middle">EP.1</text></g>' +
    f'<g id="safe-guide" display="none"><rect x="1100" y="630" width="160" height="70" fill="red" opacity=".35"/><text x="1180" y="672" font-size="20" text-anchor="middle" fill="#fff">timestamp</text></g>',
    "Thumbnail template 1280x720 (mockup). Keep bottom-right 160x70 clear for the video-length badge.", None,
    f'<linearGradient id="tsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["sky"]}"/><stop offset="1" stop-color="{C["peach"]}"/></linearGradient>')
# 5 end card 1920x1080
files['end-card.svg'] = svg(1920, 1080,
    f'<rect width="1920" height="1080" fill="url(#esky)"/>' +
    f'<rect y="760" width="1920" height="320" fill="#4F5B73" opacity=".35"/>' +
    txt(960, 150, "Goodnight, little adventurers", 84, C['cream'], 700) +
    txt(960, 215, "More adventures are waiting...", 44, C['peach'], 500) +
    f'<rect x="150" y="300" width="760" height="428" rx="30" fill="none" stroke="{C["gold"]}" stroke-width="8" stroke-dasharray="26 14"/>' + txt(530, 530, "VIDEO 1 (next episode)", 38, C['cream'], 500) +
    f'<rect x="1010" y="300" width="760" height="428" rx="30" fill="none" stroke="{C["gold"]}" stroke-width="8" stroke-dasharray="26 14"/>' + txt(1390, 530, "VIDEO 2 (best for viewer)", 38, C['cream'], 500) +
    f'<circle cx="960" cy="860" r="90" fill="none" stroke="{C["sun"]}" stroke-width="8" stroke-dasharray="20 12"/>' + txt(960, 868, "SUBSCRIBE", 24, C['cream'], 600) +
    f'<g transform="translate(300 940) scale(.55)"><use href="#pair"/></g><g transform="translate(1620 940) scale(.55)"><use href="#pair"/></g>' +
    f'<circle cx="1700" cy="120" r="60" fill="{C["sun"]}" opacity=".5"/>',
    "End card 1920x1080 (mockup). Dashed boxes = YouTube end-screen element slots; keep slots free of art. Dusk look.", None,
    f'<linearGradient id="esky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["indigo"]}"/><stop offset=".7" stop-color="#8E6BA8"/><stop offset="1" stop-color="{C["rose"]}"/></linearGradient>')
# 6 lower third 1920x1080 transparent
files['lower-third.svg'] = svg(1920, 1080,
    f'<g transform="translate(120 800)"><rect width="760" height="130" rx="30" fill="{C["cream"]}" opacity=".95"/>' +
    f'<rect width="18" height="130" rx="9" fill="{C["teal"]}"/>' +
    f'<g transform="translate(86 66) scale(.5)"><use href="#tag"/></g>' +
    txt(140, 62, "LOCATION NAME", 48, C['indigo'], 700, "start") + txt(140, 106, "Province  •  one-line fact", 32, C['plum'], 500, "start") + '</g>',
    "Lower third 1920x1080 (mockup, transparent). Slide in from left, 0.4 s ease-out; hold 4 s; accent bar = episode accent colour.", None)
# 7 title card 1920x1080
files['title-card.svg'] = svg(1920, 1080,
    f'<rect width="1920" height="1080" fill="url(#csky)"/><circle cx="1500" cy="560" r="170" fill="{C["sun"]}"/>' +
    f'<rect y="700" width="1920" height="380" fill="#9CC657"/><rect y="690" width="1920" height="20" fill="{C["teal"]}"/>' +
    txt(960, 220, "EPISODE 1", 54, C['indigo'], 600, extra='letter-spacing="8"') +
    txt(960, 360, "The Land Below", 150, C['indigo'], 700) + txt(960, 500, "the Sea", 150, C['indigo'], 700) +
    f'<g transform="translate(960 800) scale(1.15)"><use href="#pair"/></g>' +
    txt(960, 1040, "Evie &amp; Justin's Little Adventures", 40, C['plum'], 600),
    "Episode title card 1920x1080 (mockup). Hold 3 s with gentle push-in.", None,
    f'<linearGradient id="csky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["sky"]}"/><stop offset="1" stop-color="{C["peach"]}"/></linearGradient>')
# 8 palette board
eps = [("Master golden hour", ["#FFC76B","#FFF1D6","#F7B58A","#8EC8F0","#FFD9A8","#F2A5A0","#5B4A6B","#2B2D52"]),
 ("Ep1 Afsluitdijk", ["#8EC8F0","#FFE3B0","#8CBF6A","#B9B1A6","#3FA7A6","#E8DCC8","#4F5B73","#FFF1D6"]),
 ("Ep2 Schokland", ["#A9D3F0","#FFE0A8","#9CC657","#B8D77A","#E3B93C","#F3EBD8","#6A5A5E","#FFF4D0"]),
 ("Ep3 Giethoorn", ["#9AD0E8","#FFD9B0","#7DB86A","#C9A24B","#4FA37A","#B5533C","#3F5A5C","#FFEFD0"]),
 ("Ep4 Hunebedden", ["#9CB8DC","#F4CBB0","#6E8F4E","#6B4B38","#8B8499","#A29BB0","#4A405C","#F6E6D6"]),
 ("Ep5 Kootwijkerzand", ["#9FD0F0","#FFD8A0","#E8A55B","#3F6B4A","#9A5FB0","#F2D29B","#5B4A6B","#FFF0D0"]),
 ("Ep6 Delta Works", ["#7DB8E8","#FFD4A8","#BFC6CC","#3C8FC8","#4C7FB0","#D5DADF","#3F4F6E","#FFF1D6"]),
 ("Ep7 Wadden Sea", ["#B5CCE6","#F6D3CC","#B79A94","#9CC4D0","#E7C6CF","#F3D9D2","#6A5668","#FFF4EA"])]
chars = [("Evie", [("fur","#F5EFE9"),("patch","#1A1412"),("eyes","#0A67A0"),("collar","#B3203C"),("tag","#EBA02B"),("ear","#F3A38F")]),
 ("Justin", [("fur","#2A1A14"),("ear back","#F6E3DA"),("eyes","#2F7A1A"),("collar","#22160F"),("tag","#EBA02B"),("nose","#B9564A")]),
 ("Cotton", [("wool","#F7EBD9"),("ear","#F29A8A"),("eyes","#0A67A0"),("collar","#8FB6DB"),("bell","#EBA02B"),("hoof","#4A332C")]),
 ("Toffee", [("wool","#6A3418"),("cream","#F2DCC8"),("eyes","#357A22"),("collar","#4F7F2E"),("bell","#EBA02B"),("hoof","#3A2620")])]
b = txt(60, 70, "Palette board (proposed v1.0) - STYLE_GUIDE sections 2 and character sheets", 34, C['indigo'], 700, "start")
y = 110
for name, cols in eps:
    b += txt(60, y+34, name, 24, C['indigo'], 600, "start")
    for i, c in enumerate(cols):
        x = 330 + i*150
        b += f'<rect x="{x}" y="{y}" width="140" height="56" rx="10" fill="{c}" stroke="#0002"/>' + txt(x+70, y+80, c, 15, C['plum'], 500)
    y += 100
y += 10
b += txt(60, y+10, "Characters (albedo, proposed)", 30, C['indigo'], 700, "start"); y += 40
for name, parts in chars:
    b += txt(60, y+34, name, 24, C['indigo'], 600, "start")
    for i, (pn, c) in enumerate(parts):
        x = 330 + i*150
        b += f'<rect x="{x}" y="{y}" width="140" height="56" rx="10" fill="{c}" stroke="#0002"/>' + txt(x+70, y+76, pn, 14, C['plum'], 500) + txt(x+70, y+92, c, 14, C['plum'], 500)
    y += 110
files['palette-board.svg'] = svg(1280, y+20, b, "Palette board", C['cream'])
for n, s in files.items():
    open(n, 'w').write(s)
print("wrote", ", ".join(files))
