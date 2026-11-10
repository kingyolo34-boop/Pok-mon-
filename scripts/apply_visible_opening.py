#!/usr/bin/env python3
"""Make Fallen Ashe recognizably different FROM NEW GAME (visual alpha v2).

This is a real source patch, applied after apply_fallen_ashe.py and apply_chapter1.py.
No fake UI mockups: edits actual new-game dialogue, area names, and GBA palettes.
Does not claim to create the planned ruined-house custom tileset.
"""
from pathlib import Path
import json
import re
import sys

root = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()

def replace_once(rel, old, new):
    p = root / rel
    s = p.read_text(encoding="utf-8")
    if s.count(old) != 1:
        raise RuntimeError(f"{rel}: expected one unique anchor; got {s.count(old)}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")

def replace_text(rel, label, content):
    p=root/rel
    s=p.read_text(encoding="utf-8")
    # The script labels are top-level: replace only the named text block.
    a=s.find(label+":")
    if a<0: raise RuntimeError("Text label not found: "+label)
    line_end=s.find("\n",a)
    if line_end<0: raise RuntimeError("No text label line ending: "+label)
    # Birch text uses '::' (global assembler labels). Preserve it!
    label_line=s[a:line_end]
    if label_line not in (label+":",label+"::"):
        raise RuntimeError("Unexpected text label form: "+label_line)
    b=s.find("\n\n",line_end)
    if b<0: b=len(s)
    ending="\n\n" if b<len(s) else "\n"
    s=s[:a]+label_line+"\n"+content.rstrip()+ending+s[b+2:]
    p.write_text(s,encoding="utf-8")

# Show the custom name in the ROM header and emulator's ROM selector.
replace_once("Makefile", "TITLE        ?= POKEMON EMER", "TITLE        ?= FALLEN ASHE")

# Actual Professor Birch new-game speech: the FIRST conversation after New Game.
intro="data/text/birch_speech.inc"
replace_text(intro,"gText_Birch_Welcome",r'''    .string "POKéMON FALLEN ASHE\p"
    .string "ASHVALE REGION. YEAR OF ASH.\p"
    .string "The DANES rule the ruined roads.\p"
    .string "I am BIRCH. I keep a refuge\n"
    .string "outside CINDERFALL.$"''')
replace_text(intro,"gText_Birch_MainSpeech",r'''    .string "The sky has burned for years.\p"
    .string "The DANES promise order, then\n"
    .string "leave only ash behind.\p"
    .string "POKéMON are not weapons.\n"
    .string "They are all we have left.\p"
    .string "Rumors tell of the ASH CROWN,\n"
    .string "and a child it cannot command.\p"
    .string "Someone is hunting that child.$"''')
replace_text(intro,"gText_Birch_YourePlayer",r'''    .string "So, your name is {PLAYER}{KUN}.\p"
    .string "Your mother is hiding you\n"
    .string "in CINDERFALL.\p"
    .string "Whatever the DANES demand,\n"
    .string "do not give them your life.$"''')
replace_text(intro,"gText_Birch_AreYouReady",r'''    .string "A convoy has brought you to\n"
    .string "the gates of CINDERFALL.\p"
    .string "Trust the POKéMON that stands\n"
    .string "beside you when the sky burns.\p"
    .string "This is the beginning of\n"
    .string "POKéMON FALLEN ASHE.$"''')

town="data/maps/LittlerootTown/scripts.inc"
replace_text(town,"LittlerootTown_Text_OurNewHomeLetsGoInside",r'''    .string "MOM: Stay close, {PLAYER}.\p"
    .string "The supply convoy made it\n"
    .string "through the DANE blockade.\p"
    .string "This is CINDERFALL. It used to\n"
    .string "be a peaceful town.\p"
    .string "The buildings are scarred,\n"
    .string "but some families survived.\p"
    .string "We can hide here for now.\p"
    .string "Keep your head down.\n"
    .string "Please. Let's go inside.$"''')
replace_text(town,"LittlerootTown_Text_TownSign",r'''    .string "CINDERFALL - ASHVALE\p"
    .string "THE LAST HOMES BEFORE THE ASH$"''')
replace_text(town,"LittlerootTown_Text_ProfBirchsLab",r'''    .string "CINDERFALL RELIEF LAB\p"
    .string "SHELTER - MEDICINE - SUPPLIES$"''')
replace_text(town,"LittlerootTown_Text_CanUsePCToStoreItems",r'''    .string "A few PCs still have power.\p"
    .string "We store food and POKéMON\n"
    .string "supplies here during raids.$"''')
replace_text(town,"LittlerootTown_Text_IfYouGoInGrassPokemonWillJumpOut",r'''    .string "Don't go north alone!\p"
    .string "DANE patrols have been seen\n"
    .string "at the broken road.$"''')
replace_text(town,"LittlerootTown_Text_CanYouGoSeeWhatsHappening",r'''    .string "Please listen!\p"
    .string "Soldiers came through the trees.\n"
    .string "They have a DANE insignia.\p"
    .string "Someone is screaming on\n"
    .string "the north road...$"''')

# Display Cinderfall on town-entry banner and Pokenav world map.
regions=root/"src/data/region_map/region_map_sections.json"
d=json.loads(regions.read_text(encoding="utf-8"))
for entry in d["map_sections"]:
    if entry.get("id")=="MAPSEC_LITTLEROOT_TOWN":
        entry["name"]="CINDERFALL"
regions.write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

# The existing town and Route101 reuse the outdoor Petalburg secondary palette.
# Tint those palettes into a muted wasteland palette, preserving relative brightness.
# It also affects maps reusing the Petalburg secondary tileset; future dedicated
# Cinderfall tilesets will isolate the effect.
def ash_color(r,g,b):
    highest=max(r,g,b)
    if highest==0: return (r,g,b)
    if r>230 and b>180 and g<90:  # magenta / reserved transparency markers
        return (r,g,b)
    if g>r*1.13 and g>b*1.05:  # bright grass => dry ochre, olive ash
        lum=0.22*r+0.65*g+0.13*b
        return (min(255,int(lum*1.06+19)),min(255,int(lum*.85+14)),min(255,int(lum*.57+15)))
    lum=.30*r+.58*g+.12*b
    # Desaturate into stone, tan, and rust; keep light values distinguishable.
    return (min(255,int(.60*r+.40*lum*.92)),min(255,int(.58*g+.42*lum*.83)),min(255,int(.61*b+.39*lum*.72)))

pal_files=[
    root/"data/tilesets/primary/general/palettes/02.pal",
    *sorted((root/"data/tilesets/secondary/petalburg/palettes").glob("*.pal"))
]
count=0
for p in pal_files:
    lines=p.read_text(encoding="utf8").splitlines(keepends=True)
    if not lines[0].startswith("JASC-PAL"):raise RuntimeError("Bad palette format: "+str(p))
    for i in range(3,len(lines)):
        values=lines[i].strip().split()
        if len(values)!=3:continue
        r,g,b=map(int,values)
        # Palette index zero is traditionally transparent. Preserve it.
        if i==3:continue
        r2,g2,b2=ash_color(r,g,b)
        lines[i]=f"{r2} {g2} {b2}\n"
    p.write_text("".join(lines),encoding="utf8")
    count+=1

# Ensure the values that identify Fallen Ashe are built into source,
# rather than merely claimed in a changelog.
assert "POKéMON FALLEN ASHE" in (root/intro).read_text()
assert "CINDERFALL" in (root/town).read_text()
assert "TITLE        ?= FALLEN ASHE" in (root/"Makefile").read_text()
assert count==17,count
print("Fallen Ashe visual alpha: new-game story, Cinderfall banner, ash/dry-stone palette, ROM title")
