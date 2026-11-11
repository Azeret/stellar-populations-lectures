"""Where were the elements of the Solar System made?

Approximate fraction of each element (by number of atoms, at the time the Sun
formed) contributed by each kind of source. Rounded, for teaching: they follow
the "nucleosynthesis periodic table" of J. A. Johnson (2019, Science 363, 474)
and the yields compilation of Kobayashi, Karakas & Lugaro (2020, ApJ 900, 179).
The split between s- and r-process for heavy elements follows the usual solar
decomposition (e.g. Arlandini et al. 1999; Bisterzo et al. 2014). Where the
literature disagrees (e.g. the r-process site, Cu, Zn, Ga-Kr), take the numbers
as "mostly / partly", not as measurements.

Sources (keys):
  bb   Big Bang
  cr   cosmic rays hitting C, N, O in space (spallation)
  agb  dying low-mass stars (AGB stars, 1-8 Msun; also novae for Li): C, N, s-process
  ccsn exploding massive stars (core-collapse SN, > 8 Msun): O ... Ca, part of Fe
  ia   exploding white dwarfs (SN Ia): most of Fe, Mn, Ni
  r    merging neutron stars (r-process; rare kinds of supernovae may add)
  none no long-lived isotopes (made in labs or only as short-lived decay products)
"""

SOURCES = {
    "bb":   ("Big Bang", "#b39dff"),
    "cr":   ("cosmic rays", "#d9d9e3"),
    "agb":  ("dying low-mass stars", "#5cc8a1"),
    "ccsn": ("exploding massive stars", "#1e8fd5"),
    "ia":   ("exploding white dwarfs", "#f5a623"),
    "r":    ("merging neutron stars", "#ef5d8f"),
    "none": ("no stable isotopes", "#4a4a5e"),
}

# Z, symbol, name, fractions
_E = """
1 H hydrogen bb=1
2 He helium bb=0.92 agb=0.04 ccsn=0.04
3 Li lithium bb=0.25 cr=0.15 agb=0.6
4 Be beryllium cr=1
5 B boron cr=0.9 ccsn=0.1
6 C carbon agb=0.5 ccsn=0.5
7 N nitrogen agb=0.6 ccsn=0.4
8 O oxygen ccsn=0.95 agb=0.05
9 F fluorine agb=0.5 ccsn=0.5
10 Ne neon ccsn=1
11 Na sodium ccsn=0.9 agb=0.1
12 Mg magnesium ccsn=0.95 ia=0.05
13 Al aluminium ccsn=0.95 agb=0.05
14 Si silicon ccsn=0.75 ia=0.25
15 P phosphorus ccsn=1
16 S sulphur ccsn=0.7 ia=0.3
17 Cl chlorine ccsn=0.9 ia=0.1
18 Ar argon ccsn=0.7 ia=0.3
19 K potassium ccsn=0.9 ia=0.1
20 Ca calcium ccsn=0.7 ia=0.3
21 Sc scandium ccsn=1
22 Ti titanium ccsn=0.8 ia=0.2
23 V vanadium ccsn=0.5 ia=0.5
24 Cr chromium ccsn=0.4 ia=0.6
25 Mn manganese ccsn=0.25 ia=0.75
26 Fe iron ccsn=0.4 ia=0.6
27 Co cobalt ccsn=0.6 ia=0.4
28 Ni nickel ccsn=0.4 ia=0.6
29 Cu copper ccsn=0.8 agb=0.05 ia=0.15
30 Zn zinc ccsn=0.9 agb=0.05 ia=0.05
31 Ga gallium ccsn=0.6 agb=0.4
32 Ge germanium ccsn=0.6 agb=0.4
33 As arsenic ccsn=0.4 agb=0.2 r=0.4
34 Se selenium ccsn=0.4 agb=0.1 r=0.5
35 Br bromine ccsn=0.3 agb=0.1 r=0.6
36 Kr krypton ccsn=0.4 agb=0.3 r=0.3
37 Rb rubidium agb=0.5 r=0.5
38 Sr strontium agb=0.7 ccsn=0.1 r=0.2
39 Y yttrium agb=0.7 ccsn=0.1 r=0.2
40 Zr zirconium agb=0.65 ccsn=0.1 r=0.25
41 Nb niobium agb=0.6 r=0.4
42 Mo molybdenum agb=0.5 ccsn=0.2 r=0.3
43 Tc technetium none=1
44 Ru ruthenium agb=0.3 ccsn=0.1 r=0.6
45 Rh rhodium agb=0.2 r=0.8
46 Pd palladium agb=0.5 r=0.5
47 Ag silver agb=0.2 r=0.8
48 Cd cadmium agb=0.6 r=0.4
49 In indium agb=0.6 r=0.4
50 Sn tin agb=0.7 r=0.3
51 Sb antimony agb=0.3 r=0.7
52 Te tellurium agb=0.2 r=0.8
53 I iodine agb=0.05 r=0.95
54 Xe xenon agb=0.2 r=0.8
55 Cs caesium agb=0.15 r=0.85
56 Ba barium agb=0.85 r=0.15
57 La lanthanum agb=0.75 r=0.25
58 Ce cerium agb=0.8 r=0.2
59 Pr praseodymium agb=0.5 r=0.5
60 Nd neodymium agb=0.6 r=0.4
61 Pm promethium none=1
62 Sm samarium agb=0.3 r=0.7
63 Eu europium agb=0.05 r=0.95
64 Gd gadolinium agb=0.15 r=0.85
65 Tb terbium agb=0.05 r=0.95
66 Dy dysprosium agb=0.15 r=0.85
67 Ho holmium agb=0.1 r=0.9
68 Er erbium agb=0.2 r=0.8
69 Tm tm agb=0.15 r=0.85
70 Yb ytterbium agb=0.4 r=0.6
71 Lu lutetium agb=0.2 r=0.8
72 Hf hafnium agb=0.5 r=0.5
73 Ta tantalum agb=0.4 r=0.6
74 W tungsten agb=0.55 r=0.45
75 Re rhenium agb=0.1 r=0.9
76 Os osmium agb=0.1 r=0.9
77 Ir iridium agb=0.01 r=0.99
78 Pt platinum agb=0.05 r=0.95
79 Au gold agb=0.05 r=0.95
80 Hg mercury agb=0.6 r=0.4
81 Tl thallium agb=0.75 r=0.25
82 Pb lead agb=0.8 r=0.2
83 Bi bismuth agb=0.4 r=0.6
84 Po polonium none=1
85 At astatine none=1
86 Rn radon none=1
87 Fr francium none=1
88 Ra radium none=1
89 Ac actinium none=1
90 Th thorium r=1
91 Pa protactinium none=1
92 U uranium r=1
93 Np neptunium none=1
94 Pu plutonium none=1
"""

ELEMENTS = []
for line in _E.strip().splitlines():
    parts = line.split()
    z, sym, name = int(parts[0]), parts[1], parts[2]
    frac = {k: float(v) for k, v in (p.split("=") for p in parts[3:])}
    ELEMENTS.append(dict(Z=z, symbol=sym, name=name if name != "tm" else "thulium", frac=frac))


def position(z):
    """(row, column) in the usual 18-column table; lanthanides/actinides in rows 8 and 9."""
    if z <= 2:
        return 0, 0 if z == 1 else 17
    if z <= 10:
        return 1, (z - 3) if z <= 4 else z + 7
    if z <= 18:
        return 2, (z - 11) if z <= 12 else z - 1
    if z <= 36:
        return 3, z - 19
    if z <= 54:
        return 4, z - 37
    if 57 <= z <= 71:
        return 8, z - 57 + 2
    if 89 <= z <= 103:
        return 9, z - 89 + 2
    if z <= 56:
        return 5, z - 55
    if z <= 86:
        return 5, z - 72 + 3
    if z <= 88:
        return 6, z - 87
    return 6, z - 104 + 3


if __name__ == "__main__":
    for e in ELEMENTS:
        s = sum(e["frac"].values())
        assert abs(s - 1) < 1e-6, (e["symbol"], s)
    print(len(ELEMENTS), "elements, fractions sum to 1")
