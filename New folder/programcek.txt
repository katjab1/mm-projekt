import pandas as pd
import pulp as p

df = pd.read_excel(r"D:\Faks\MM_projekt\podatki.xlsx", sheet_name="ucenci7_izbire")

Lp_prop = p.LpProblem("problem", p.LpMaximize)

x1_1 = p.LpVariable("x1_1", lowBound=0, upBound=1, cat='Integer')
x1_2 = p.LpVariable("x1_2", lowBound=0, upBound=1, cat='Integer')
x1_3 = p.LpVariable("x1_3", lowBound=0, upBound=1, cat='Integer')
x1_4 = p.LpVariable("x1_4", lowBound=0, upBound=1, cat='Integer')
x2_1 = p.LpVariable("x2_1", lowBound=0, upBound=1, cat='Integer')
x2_2 = p.LpVariable("x2_2", lowBound=0, upBound=1, cat='Integer')
x2_3 = p.LpVariable("x2_3", lowBound=0, upBound=1, cat='Integer')
x2_4 = p.LpVariable("x2_4", lowBound=0, upBound=1, cat='Integer')

Lp_prop += 1000 * x1_1 + 100 * x1_2 + 10 * x1_3 + x1_4 + x2_1 + 10 * x2_2 + 100 * x2_3 + 1000 * x2_4

Lp_prop += 2*x1_1 + 2 * x1_2 + x1_3 + x1_4 == 1
Lp_prop += 2*x2_1 + 2 * x2_2 + x2_3 + x2_4 == 2


Lp_prop += x1_1 + x2_1 >= 0.0
Lp_prop += x1_1 + x2_1 <= 2.0

Lp_prop += x1_2 + x2_2 >= 0.0
Lp_prop += x1_2 + x2_2 <= 2.0

Lp_prop += x1_3 + x2_3 >= 0.0
Lp_prop += x1_3 + x2_3 <= 2.0

Lp_prop += x1_4 + x2_4 >= 0.0
Lp_prop += x1_4 + x2_4 <= 2.0

solution = Lp_prop.solve()
print(f"SOLUTION \n")
print(f"x11 = {p.value(x1_1)}")
print(f"x12 = {p.value(x1_2)}")
print(f"x13 = {p.value(x1_3)}")
print(f"x14 = {p.value(x1_4)}")
print(f"x21 = {p.value(x2_1)}")
print(f"x22 = {p.value(x2_2)}")
print(f"x23 = {p.value(x2_3)}")
print(f"x24 = {p.value(x2_4)}")
print(f"Resitev: {p.value(Lp_prop.objective)}")
