import pandas as pd
import pulp as p

df = pd.read_excel(r"D:\Faks\MM_projekt\podatki.xlsx", sheet_name="ucenci7_izbire")
dfPredmeti = pd.read_excel(r"D:\Faks\MM_projekt\podatki.xlsx", sheet_name="predmeti7")
predmeti_P = set()

for index, row in df.iterrows():
    predmeti_P.add(row["izbira1"])
print(predmeti_P)

stevec = {predmet: 0 for predmet in predmeti_P}

for value in df["izbira1"]:
    if value in predmeti_P:  # Preverimo, če je vrednost med predmeti
        stevec[value] += 1

for value in df["izbira2"]:
    if value in predmeti_P:
        stevec[value] += 1
print(stevec)


# če si učenci kot 1. in 2. izbiro niso zaželeli predmeta vsaj 17x ga odstranimo:
for key, value in stevec.items():
    if value < 17:
        for index, row in df.iterrows():
            if row["izbira1"] == key:
                df.at[index, "izbira1"] = '0'
            if row["izbira2"] == key:
                df.at[index, "izbira2"] = '0'
            if row["izbira3"] == key:
                df.at[index, "izbira2"] = '0'
            if row["izbira4"] == key:
                df.at[index, "izbira2"] = '0'

predmeti = set()
for index, row in df.iterrows():
    if row["izbira1"] != '0':
        predmeti.add(row["izbira1"])

Lp_prop = p.LpProblem("problem", p.LpMaximize)
print(df)

for index, row in df.iterrows():
    for predmet in predmeti:
        imeX = f'x_{row["sifra"]}_{predmet}'
        v = p.LpVariable(imeX, lowBound=0, upBound=1, cat="Integer")
        Lp_prop.addVariable(v)
for variable in Lp_prop.variables():
    print(variable)

df2 = df[['sifra', 'moznost']].copy()
ucenecUre = df2.set_index('sifra').to_dict()

for key, value in ucenecUre['moznost'].items():
    if value == 1:
        ucenecUre['moznost'][key] = 2
    elif value == 2:
        ucenecUre['moznost'][key] = 3
    elif value == 3:
        ucenecUre['moznost'][key] = 1
    elif value == 4:
        ucenecUre['moznost'][key] = 0

dfPredmeti = dfPredmeti.drop(columns=['imepredmeta'])
df = df.set_index('sifra')
print(df)

dfPredmeti = dfPredmeti.set_index('sifra')
predmetiUre = dfPredmeti.to_dict()

dfIzbire = df.drop(columns=['Razred', 'moznost'])

w = {}

for index, row in dfIzbire.iterrows():
    for predmet in predmeti:
        ime = f'w_{index}_{predmet}'
        if dfIzbire.loc[index, "izbira1"] == predmet:
            w[ime] = 1000
        elif dfIzbire.loc[index, "izbira2"] == predmet:
            w[ime] = 100
        elif dfIzbire.loc[index, "izbira3"] == predmet:
            w[ime] = 10
        elif dfIzbire.loc[index, "izbira4"] == predmet:
            w[ime] = 1
        else:
            w[ime] = 0

print(dfIzbire)
print(dfPredmeti)
print(predmetiUre)
print(ucenecUre)
print(w)

kriterijskaF = {}

for x in Lp_prop.variables():
    for kljuc in w.keys():
        if (kljuc.__str__()[1:]) == (x.__str__()[1:]):
            kriterijskaF[x] = w[kljuc]

funkcija = p.LpAffineExpression([(x, kriterijskaF[x]) for x in kriterijskaF])
print(funkcija)
Lp_prop += funkcija

omejitve = {}
omejitve2 = []
for key, value in ucenecUre['moznost'].items():
    omejitve2 = []
    for x in Lp_prop.variables():
        if (x.__str__()[2:6]) == key:
            for key2, value2 in predmetiUre['stevilour'].items():
                if (x.__str__()[7:]) == key2:
                    omejitve2.append(x * value2)
        omejitve[key] = omejitve2

omejitve_sestete = {}
for key, values in omejitve.items():
    omejitve_sestete[key] = sum(values)

for key, value in ucenecUre['moznost'].items():
    for sifra, omejitveUcenca in omejitve_sestete.items():
        if key == sifra:
            Lp_prop += omejitveUcenca == value

omejitvePredmetov = {}
spremenljivkePredmetov = []
for predmet in predmeti:
    spremenljivkePredmetov = []
    for x in Lp_prop.variables():
        if (x.__str__()[7:]) == predmet:
            spremenljivkePredmetov.append(x)
        omejitvePredmetov[predmet] = spremenljivkePredmetov

omejitvePredmetov_sestete = {}
for key, values in omejitvePredmetov.items():
    omejitvePredmetov_sestete[key] = sum(values)
print(omejitvePredmetov_sestete)

# nastavimo omejitev maksimalnega števila učencev pri izvajanem predmetu
for sifra, omejitvePredmeta in omejitvePredmetov_sestete.items():
    Lp_prop += omejitvePredmeta <= 27

    # v primeru, da se šola odloči, da bo izvajala vse ponujene predmete,
    # lahko dodamo to kodo in program enakomerno razdeli predmete kot najbolj optimalno možnost,
    # pri čemer je na vsak predmet prijavljenih med 14 in 27 učencev
"""
    Lp_prop += omejitvePredmeta >= 14
    Lp_prop += omejitvePredmeta >= 27
"""

stevec = {}
for predmet in predmeti:
    stevec[predmet] = 0

solution = Lp_prop.solve()
for x in Lp_prop.variables():
    if p.value(x) == 1:
        predmet = x.__str__()[7:]
        stevec[predmet] += 1
        print("Ucenec ", x.__str__()[2:6], "dobi predmet ", x.__str__()[7:])
# print(x.__str__(), p.value(x))
print(f"Resitev: {p.value(Lp_prop.objective)}")

for predmet in predmeti:
    print("Predmet ", predmet, "obiskuje ", stevec.get(predmet, 0), "ucencev")
