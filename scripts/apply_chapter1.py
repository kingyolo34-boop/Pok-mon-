#!/usr/bin/env python3
"""Fallen Ashe Chapter One: implement an actual scripted ambush on Route 101.

Applies AFTER scripts/apply_fallen_ashe.py to pinned pokeemerald-expansion.
An intentionally small source patch, leaving the original Emerald intro flow
intact until the player walks north to the original Birch-rescue scene.
"""
from pathlib import Path
import json
import sys

root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()

def replace_once(rel, old, new):
    p=root/rel
    s=p.read_text(encoding="utf8")
    count=s.count(old)
    if count!=1:
        raise RuntimeError(f"{rel}: expected one anchor, found {count}: {old[:90]!r}")
    p.write_text(s.replace(old,new,1),encoding="utf8")

# Rook uses a dedicated, unused trainer slot, not an existing Emerald trainer.
replace_once("include/constants/opponents.h",
    "#define TRAINER_MAY_PLACEHOLDER             854",
    "#define TRAINER_MAY_PLACEHOLDER             854\n#define TRAINER_FALLEN_ASHE_ROOK               855")
replace_once("include/constants/opponents.h",
    "#define TRAINERS_COUNT_EMERALD     855",
    "#define TRAINERS_COUNT_EMERALD     856")
party=root/"src/data/trainers.party"
s=party.read_text(encoding="utf8")
if "=== TRAINER_FALLEN_ASHE_ROOK ===" in s: raise RuntimeError("Rook party already exists")
party.write_text(s.rstrip()+"""

=== TRAINER_FALLEN_ASHE_ROOK ===
Name: ROOK
Class: Team Magma
Pic: Magma Leader Maxie
Gender: Male
Music: Magma
AI: Check Bad Move

Poochyena
Level: 3
- Tackle
- Howl
""",encoding="utf8")

# Story flags live in two currently-unused 16-bit save flags.
replace_once("include/constants/flags.h",
    "#define FLAG_UNUSED_0x04A    0x4A // Unused Flag",
    "#define FLAG_FALLEN_ASHE_MOM_GONE      0x4A // Rook killed Mom in Chapter One")
replace_once("include/constants/flags.h",
    "#define FLAG_UNUSED_0x04B    0x4B // Unused Flag",
    "#define FLAG_FALLEN_ASHE_ROOK_HIDDEN   0x4B // Rook spawns after starter choice")

# Native chooser normally gives a starter AND launches an unavoidable wild
# Zigzagoon battle. Return to the script instead so Rook can appear afterwards.
replace_once("src/battle_setup.c",
    """    ScriptGiveMon(starterMon, 5, ITEM_NONE);
    ResetTasks();
    PlayBattleBGM();
    SetMainCallback2(CB2_StartFirstBattle);
    BattleTransition_Start(B_TRANSITION_BLUR);""",
    """    ScriptGiveMon(starterMon, 5, ITEM_NONE);
    ResetTasks();
    // Fallen Ashe: the next fight is a STORY trainer battle against Rook,
    // not Emerald's first wild Zigzagoon fight.
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);""")

# Route 101 is the temporary Cinderfall ambush road. Use real cutscene
# objects; they currently borrow the vanilla Mom, Magma grunt, and Maxie art.
p=root/"data/maps/Route101/map.json"
d=json.loads(p.read_text(encoding="utf8"))
d["weather"]="WEATHER_VOLCANIC_ASH"
d["music"]="MUS_ROUTE114"
for ob in d["object_events"]:
    if ob.get("local_id")=="LOCALID_ROUTE101_BIRCH":
        ob["graphics_id"]="OBJ_EVENT_GFX_MOM"
    elif ob.get("local_id")=="LOCALID_ROUTE101_ZIGZAGOON":
        ob["graphics_id"]="OBJ_EVENT_GFX_MAGMA_MEMBER_M"
if any(ob.get("local_id")=="LOCALID_ROUTE101_ROOK" for ob in d["object_events"]):
    raise RuntimeError("Rook NPC ID already used")
d["object_events"].append({
    "local_id":"LOCALID_ROUTE101_ROOK",
    "graphics_id":"OBJ_EVENT_GFX_MAXIE",
    "x":9,"y":11,"elevation":0,
    "movement_type":"MOVEMENT_TYPE_FACE_DOWN",
    "movement_range_x":0,"movement_range_y":0,
    "trainer_type":"TRAINER_TYPE_NONE",
    "trainer_sight_or_berry_tree_id":"0",
    "script":"Route101_EventScript_RookEcho",
    "flag":"FLAG_FALLEN_ASHE_ROOK_HIDDEN"
})
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n",encoding="utf8")

replace_once("data/maps/Route101/scripts.inc",
    """Route101_OnTransition:
	call ProfBirch_EventScript_UpdateLocation
	end""",
    """Route101_OnTransition:
	call ProfBirch_EventScript_UpdateLocation
	setflag FLAG_FALLEN_ASHE_ROOK_HIDDEN
	end""")

p=root/"data/maps/Route101/scripts.inc"
s=p.read_text(encoding="utf8")
start=s.index("Route101_EventScript_BirchsBag::")
end=s.index("Route101_EventScript_HideMayInBedroom::",start)

event= r'''Route101_EventScript_BirchsBag::
    lockall
    faceplayer
    msgbox FallenAshe_Text_BallsFall, MSGBOX_DEFAULT
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_RESCUED_BIRCH
    fadescreen FADE_TO_BLACK
    removeobject LOCALID_ROUTE101_ZIGZAGOON
    setobjectxy LOCALID_PLAYER, 6, 13
    applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
    waitmovement 0
    special ChooseStarter
    @ The modified starter callback returns directly to this scene.
    clearflag FLAG_FALLEN_ASHE_ROOK_HIDDEN
    addobject LOCALID_ROUTE101_ROOK
    fadescreen FADE_FROM_BLACK
    applymovement LOCALID_ROUTE101_ROOK, FallenAshe_Movement_RookFacesPlayer
    waitmovement 0
    msgbox FallenAshe_Text_RookRevealsMark, MSGBOX_DEFAULT
    msgbox FallenAshe_Text_MomsLastWords, MSGBOX_DEFAULT
    fadescreen FADE_TO_BLACK
    removeobject LOCALID_ROUTE101_BIRCH
    setflag FLAG_HIDE_ROUTE_101_BIRCH_ZIGZAGOON_BATTLE
    setflag FLAG_FALLEN_ASHE_MOM_GONE
    setflag FLAG_HIDE_LITTLEROOT_TOWN_MOM_OUTSIDE
    setflag FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_MOM
    setflag FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_MOM
    delay 25
    fadescreen FADE_FROM_BLACK
    msgbox FallenAshe_Text_RookKilledMom, MSGBOX_DEFAULT
    special HealPlayerParty
    trainerbattle_single TRAINER_FALLEN_ASHE_ROOK, FallenAshe_Text_RookChallenge, FallenAshe_Text_RookLoses
    msgbox FallenAshe_Text_RookHuntsYou, MSGBOX_DEFAULT
    removeobject LOCALID_ROUTE101_ROOK
    setflag FLAG_FALLEN_ASHE_ROOK_HIDDEN
    setflag FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG
    clearflag FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_BIRCH
    setvar VAR_BIRCH_LAB_STATE, 2
    setvar VAR_ROUTE101_STATE, 3
    clearflag FLAG_HIDE_MAP_NAME_POPUP
    checkplayergender
    call_if_eq VAR_RESULT, MALE, Route101_EventScript_HideMayInBedroom
    call_if_eq VAR_RESULT, FEMALE, Route101_EventScript_HideBrendanInBedroom
    msgbox FallenAshe_Text_Shelter, MSGBOX_DEFAULT
    warp MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB, 6, 5
    waitstate
    releaseall
    end

Route101_EventScript_RookEcho::
    msgbox FallenAshe_Text_RookEcho, MSGBOX_NPC
    end

FallenAshe_Movement_RookFacesPlayer:
    walk_in_place_fast_down
    step_end

FallenAshe_Text_BallsFall:
    .string "MOM: The DANES found us!\p"
    .string "Three POKé BALLS fall from\n"
    .string "her battered satchel.\p"
    .string "MOM: Take one! I'll hold them!$"

FallenAshe_Text_RookRevealsMark:
    .string "ROOK: So this is the child\n"
    .string "of the eclipse.\p"
    .string "MOM: Get away from my child!\p"
    .string "ROOK: Only one person can break\n"
    .string "the ASH CROWN.\p"
    .string "The DANES won't let you live.$"

FallenAshe_Text_MomsLastWords:
    .string "MOM: I kept the seal from them.\p"
    .string "Go. Keep going. Save who you can.\p"
    .string "And know that I love you.$"

FallenAshe_Text_RookKilledMom:
    .string "Rook strikes your mother.\p"
    .string "She falls into the ash\n"
    .string "and does not rise.\p"
    .string "ROOK: No more running, child.$"

FallenAshe_Text_RookChallenge:
    .string "ROOK: Your life ends here!$"

FallenAshe_Text_RookLoses:
    .string "ROOK: Tch. You won't escape\n"
    .string "the hunt forever.$"

FallenAshe_Text_RookHuntsYou:
    .string "ROOK: Every road, every town.\n"
    .string "My DANES will find you.\p"
    .string "And when you fall, child,\n"
    .string "I'll be waiting.$"

FallenAshe_Text_Shelter:
    .string "A survivor signals you toward\n"
    .string "the lab, now a refuge.\p"
    .string "You flee into the ashes.$"

FallenAshe_Text_RookEcho:
    .string "The air smells of smoke.\n"
    .string "Rook's footsteps are gone.$"

'''
s=s[:start]+event+s[end:]

strings={
    'Route101_Text_HelpMe:': r'''Route101_Text_HelpMe:
    .string "MOM: RUN! THE DANES ARE HERE!$"
''',
    'Route101_Text_PleaseHelp:': r'''Route101_Text_PleaseHelp:
    .string "MOM: Behind us! A DANE patrol!\p"
    .string "Quick! My bag! Take a POKéMON!$"
''',
    'Route101_Text_DontLeaveMe:': r'''Route101_Text_DontLeaveMe:
    .string "MOM: Don't leave without a\n"
    .string "POKéMON! They'll kill us!$"
''',
    'Route101_Text_RouteSign:': r'''Route101_Text_RouteSign:
    .string "CINDERFALL OUTSKIRTS\p"
    .string "WARNING: DANE CHECKPOINT AHEAD$"
''',
}
for label,replacement in strings.items():
    a=s.index(label)
    b=s.find("\nRoute101_Text_",a+len(label))
    if b<0:
        b=len(s)
    s=s[:a]+replacement.rstrip()+"\n\n"+s[b:].lstrip("\n")
p.write_text(s,encoding="utf8")

# The wider town looks bleak before the attack; the custom ruined tilesets
# will be a separate art/map milestone.
p=root/"data/maps/LittlerootTown/map.json"
d=json.loads(p.read_text(encoding="utf8"))
d["weather"]="WEATHER_VOLCANIC_ASH"
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n",encoding="utf8")

# GBA prologue acceptance check: keep order and preserve true story requirements.
script=(root/"data/maps/Route101/scripts.inc").read_text()
key=["FallenAshe_Text_BallsFall","special ChooseStarter",
     "FallenAshe_Text_RookRevealsMark","FLAG_FALLEN_ASHE_MOM_GONE",
     "trainerbattle_single TRAINER_FALLEN_ASHE_ROOK",
     "FallenAshe_Text_RookHuntsYou"]
positions=[script.index(k,script.index("Route101_EventScript_BirchsBag::")) for k in key]
assert positions==sorted(positions),positions
assert "CB2_StartFirstBattle" in (root/"src/battle_setup.c").read_text()  # function still present upstream
assert "SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);" in (root/"src/battle_setup.c").read_text()
print("Fallen Ashe Chapter One applied: Mom -> three starters -> Rook -> death -> trainer fight -> escape")
