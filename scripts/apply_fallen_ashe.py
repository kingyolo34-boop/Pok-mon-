#!/usr/bin/env python3
"""Build-test bootstrap for Fallen Ashe, applied to pinned pokeemerald-expansion.
This intentionally changes starter data only until a verified ROM build exists.
"""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
file = root / 'src/data/pokemon/species_info/gen_3_families.h'
s = file.read_text(encoding='utf-8')
entries = {
 'TREECKO': ('Verdrake', 'TYPE_GRASS', (49,55,48,64,62,42), 'Young Sprout',18),
 'GROVYLE': ('Leafdrake', 'TYPE_GRASS, TYPE_DRAGON', (68,78,70,72,75,57), 'Thorn Drake',36),
 'SCEPTILE': ('Grovedrake', 'TYPE_GRASS, TYPE_DRAGON', (94,110,94,78,80,79), 'Forest Drake',None),
 'MUDKIP': ('Aqualye', 'TYPE_WATER', (53,42,52,62,66,45), 'Tide Foal',18),
 'MARSHTOMP': ('Tidalcorn', 'TYPE_WATER, TYPE_FAIRY', (67,58,68,80,86,61), 'Tide Unicorn',36),
 'SWAMPERT': ('Abysscorn', 'TYPE_WATER, TYPE_FAIRY', (88,70,90,101,103,83), 'Abyss Horn',None),
 'TORCHIC': ('Embergryph', 'TYPE_FIRE', (46,64,44,64,58,44), 'Ember Griff',18),
 'COMBUSKEN': ('Flaregryph', 'TYPE_FIRE, TYPE_FLYING', (63,84,63,89,68,53), 'Flame Griff',36),
 'BLAZIKEN': ('Inferngryph', 'TYPE_FIRE, TYPE_FLYING', (80,117,76,114,76,72), 'Inferno Wing',None),
}
assert all(len(v[3]) <= 12 for v in entries.values()), 'Category label exceeds GBA limit'
for species, (name,types,stats,category,evo) in entries.items():
    pattern = r'(    \[SPECIES_' + species + r'\] =\s*\{)(.*?)(?=\n    \[SPECIES_|\Z)'
    match = re.search(pattern, s, re.S)
    if not match: raise SystemExit('Missing species block: '+species)
    text = match.group(2)
    for field,val in zip(('baseHP','baseAttack','baseDefense','baseSpeed','baseSpAttack','baseSpDefense'),stats):
        text, count = re.subn(r'(\.'+field+r'\s*=\s*)\d+',lambda m: m.group(1)+str(val),text,count=1)
        if count != 1: raise SystemExit('Missing stat '+field+' for '+species)
    text, count = re.subn(r'(\.types\s*=\s*)MON_TYPES\([^\)\n]*\)',lambda m: m.group(1)+'MON_TYPES('+types+')',text,count=1)
    if count != 1: raise SystemExit('Missing types for '+species)
    for field,replacement in [('speciesName','_("'+name+'")'),('categoryName','_("'+category+'")')]:
        text, count = re.subn(r'(\.'+field+r'\s*=\s*)[^,\n]+',lambda m: m.group(1)+replacement,text,count=1)
        if count != 1: raise SystemExit('Missing '+field+' for '+species)
    if evo is not None:
        text, count = re.subn(r'(\{EVO_LEVEL,\s*)\d+',lambda m:m.group(1)+str(evo),text,count=1)
        if count != 1: raise SystemExit('Missing evolution for '+species)
    s = s[:match.start(2)] + text + s[match.end(2):]
file.write_text(s,encoding='utf-8')
starter = root/'src/starter_choose.c'
s = starter.read_text(encoding='utf-8')
old = '    GRASS_STARTER,\n    FIRE_STARTER,\n    WATER_STARTER,'
new = '    GRASS_STARTER,\n    WATER_STARTER,\n    FIRE_STARTER,'
if old not in s and new not in s: raise SystemExit('Starter selector format changed')
starter.write_text(s.replace(old,new,1),encoding='utf-8')
strings = root/'src/strings.c'
s = strings.read_text(encoding='utf-8')
s, n = re.subn(r'(const u8 gText_BirchInTrouble\[\] = _\(")[^\"]+("\);)',r'\1Your mother dropped three POKé BALLS!\\nChoose one. Hurry!\2',s,count=1)
if n != 1: raise SystemExit('Starter prompt not found')
strings.write_text(s,encoding='utf-8')
print('Applied Fallen Ashe starter names, typings, stats, evolution levels and choice order')
