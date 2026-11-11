#!/usr/bin/env python3
"""Fallen Ashe: turn Cinderfall's four facade-only buildings into real interiors.

Run AFTER scripts/apply_cinderfall_map.py. Map definitions are original Fallen Ashe
source data; the map interiors temporarily reuse existing Emerald tilesets/layouts.
"""
from __future__ import annotations

import copy
import json
import struct
import sys
from collections import deque
from pathlib import Path

root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
maps=root/"data/maps"
town_path=maps/"LittlerootTown/map.json"
town=json.loads(town_path.read_text(encoding="utf-8"))
groups_path=maps/"map_groups.json"
groups=json.loads(groups_path.read_text(encoding="utf-8"))
bin_path=root/"data/layouts/LittlerootTown/map.bin"
layout=list(struct.unpack("<812H",bin_path.read_bytes()))
W,H=28,29

def walk(x,y):
    return 0<=x<W and 0<=y<H and not bool(layout[y*W+x]&0x0400)

# Make absolutely sure the town's important positions connect to the route,
# original three functional entrances, and all four new doors.
start=(10,12)
assert walk(*start)
q=deque([start]);seen={start}
while q:
    x,y=q.popleft()
    for xx,yy in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        if (xx,yy) not in seen and walk(xx,yy):
            seen.add((xx,yy));q.append((xx,yy))

needed={
    "northern route":(10,0),
    "player home":(5,8),
    "scared family house":(14,8),
    "relief center":(7,16),
    "supply house":(23,9),
    "garrick shelter":(23,17),
    "abandoned house":(14,23),
    "trade depot":(5,25)
}
for label,p in needed.items():
    assert p in seen,f"Blocked path to {label} at {p}"
print("Cinderfall walkability: PASS (%d reachable tiles)"%len(seen))

# New maps are appended to the existing indoor Littleroot map group. This
# preserves the map IDs of all existing Emerald locations.
specs=[
    dict(name="FallenAshe_SupplyHouse", id="MAP_FALLEN_ASHE_SUPPLY_HOUSE",
         door=(23,9), indoor="home", npc="OBJ_EVENT_GFX_WOMAN_2",
         text="NELL: The DANES took our medicine.\\pI hide what remains under these crates.\\pIf you can bring help, Lastwood might survive.$"),
    dict(name="FallenAshe_GarrickShelter", id="MAP_FALLEN_ASHE_GARRICK_SHELTER",
         door=(23,17), indoor="home", npc="OBJ_EVENT_GFX_FAT_MAN",
         text="GARRICK: Don't trust the DANES.\\pTheir soldiers stole our food, then called it a tax.\\pThey will come back for the child.$"),
    dict(name="FallenAshe_AbandonedHouse", id="MAP_FALLEN_ASHE_ABANDONED_HOUSE",
         door=(14,23), indoor="abandoned", npc=None,
         text="A LETTER IN THE ASH:\\p'THEY FOUND THE CHILD. ROOK IS COMING.\\pHIDE THE KEEPER'S SEAL.'$"),
    dict(name="FallenAshe_TradeDepot", id="MAP_FALLEN_ASHE_TRADE_DEPOT",
         door=(5,25), indoor="shop", npc="OBJ_EVENT_GFX_MART_EMPLOYEE",
         text="TRADER: Supplies cost more out here.\\pThe DANES burned half our stock.\\pTake what you need to survive.$"),
]
assert len(town["warp_events"])==3,town["warp_events"]
group=groups["gMapGroup_IndoorLittleroot"]
assert len(group)==5

for spec in specs:
    name,id_=spec["name"],spec["id"]
    target=maps/name
    assert not target.exists(),f"Map already exists: {name}"
    warp_idx=len(town["warp_events"])
    x,y=spec["door"]
    assert walk(x,y),f"{name} has blocked entrance"
    town["warp_events"].append(dict(
        x=x,y=y,elevation=0,dest_map=id_,dest_warp_id="0"
    ))
    group.append(name)
    target.mkdir(parents=True)
    shop=spec["indoor"]=="shop"
    template=json.loads((maps/("OldaleTown_Mart" if shop else "OldaleTown_House1")/"map.json").read_text(encoding="utf-8"))
    template["name"]=name
    template["id"]=id_
    template["layout"]="LAYOUT_MART" if shop else "LAYOUT_HOUSE1"
    template["region_map_section"]="MAPSEC_LITTLEROOT_TOWN"
    template["music"]="MUS_POKE_MART" if shop else "MUS_LITTLEROOT"
    template["warp_events"]=[
       dict(x=x1,y=7 if shop else 8,elevation=0,dest_map="MAP_LITTLEROOT_TOWN",dest_warp_id=str(warp_idx))
       for x1 in (3,4)
    ]
    template["object_events"]=[]
    template["coord_events"]=[]
    template["bg_events"]=[]
    label=name+"_EventScript_Resident"
    if spec["npc"]:
        template["object_events"].append(dict(
            graphics_id=spec["npc"],
            x=1 if shop else 6,y=3 if shop else 4,
            elevation=3,movement_type="MOVEMENT_TYPE_FACE_DOWN",
            movement_range_x=0,movement_range_y=0,
            trainer_type="TRAINER_TYPE_NONE",trainer_sight_or_berry_tree_id="0",
            script=label,flag="0"))
    elif spec["indoor"]=="abandoned":
        template["bg_events"].append(dict(type="sign",x=5,y=3,elevation=0,
            player_facing_dir="BG_EVENT_PLAYER_FACING_ANY",script=label))
    (target/"map.json").write_text(json.dumps(template,indent=2)+"\n",encoding="utf-8")

    text=spec["text"].replace("\\p",r"\p")  # string for Emerald .string
    script=(f"{name}_MapScripts::\n"
            "    .byte 0\n\n"
            f"{label}::\n")
    if shop:
        script+=("    lock\n    faceplayer\n"
                 f"    msgbox {name}_Text_Resident, MSGBOX_DEFAULT\n"
                 "    message gText_HowMayIServeYou\n"
                 "    waitmessage\n"
                 f"    pokemart {name}_ShopItems\n"
                 "    msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT\n"
                 "    release\n    end\n\n"
                 f"    .align 2\n{name}_ShopItems:\n"
                 "    .2byte ITEM_POKE_BALL\n"
                 "    .2byte ITEM_POTION\n"
                 "    .2byte ITEM_ANTIDOTE\n"
                 "    .2byte ITEM_PARALYZE_HEAL\n"
                 "    .2byte ITEM_ESCAPE_ROPE\n"
                 "    pokemartlistend\n\n")
    else:
        script+=(f"    msgbox {name}_Text_Resident, MSGBOX_"+("SIGN" if spec["indoor"]=="abandoned" else "NPC")+"\n"
                 "    end\n\n")
    # Split pages at \p and keep line widths within Emerald's text constraints.
    pages=text[:-1].split(r"\p")
    script+=f"{name}_Text_Resident:\n"
    for i,page in enumerate(pages):
        # Inline string escapes are preserved verbatim. Limit long dialogue
        # at word boundaries so GBA boxes don't overflow horizontally.
        words=page.split()
        lines=[];line=""
        for word in words:
            if line and len(line)+1+len(word)>31:
                lines.append(line);line=word
            else:line=(line+" "+word).strip()
        if line:lines.append(line)
        for j,line in enumerate(lines):
            suffix=(r"\p" if j==len(lines)-1 and i<len(pages)-1 else
                    r"\n" if j<len(lines)-1 else "")
            script+='    .string "'+line+suffix+('"\\n')
    # Replace the final string terminator with a $ on last line.
    lines=script.splitlines()
    lines[-1]=lines[-1].replace('"\n','"').replace('"\r','"')
    if lines[-1].endswith('"'):
        lines[-1]=lines[-1][:-1]+'$"'
    script='\n'.join(lines)+'\n'
    (target/"scripts.inc").write_text(script,encoding="utf-8")
    print("  %s => exterior warp #%d, two-way interior exit"%(name,warp_idx))

town_path.write_text(json.dumps(town,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
groups_path.write_text(json.dumps(groups,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

# Unlike map metadata, Emerald's event-script assembly includes are explicit.
# Register each new room so the linker sees its MapScripts and NPC dialogue.
assembly=root/"data/event_scripts.s"
asm=assembly.read_text(encoding="utf-8")
include_anchor='\t.include "data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc"'
assert asm.count(include_anchor)==1,"Unexpected expansion include anchor"
extra_includes = "\n".join('\t.include "data/maps/'+x["name"]+'/scripts.inc"' for x in specs)
asm=asm.replace(include_anchor,include_anchor+"\n"+extra_includes,1)
assembly.write_text(asm,encoding="utf-8")

for i,spec in enumerate(specs,start=3):
    dst=town["warp_events"][i]
    assert dst["dest_map"]==spec["id"]
    indoor=json.loads((maps/spec["name"]/"map.json").read_text())
    assert all(x["dest_warp_id"]==str(i) for x in indoor["warp_events"])
print("Cinderfall interiors complete: 7 enterable exteriors, 4 new interiors and a functioning early shop.")
