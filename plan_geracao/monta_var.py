import pandas as pd

import data_usi
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()
data = data_usi.gerate_data()
Pg_lim = []
uc_inv = []
name_usi = []
for usi in data:
    for uni in range(int(usi.loc['qte'])):
        name_usi.append(usi.loc['Tipo'][0])
        Pg_lim.append(usi.loc['Capacidade'])
        uc_inv.append(usi.loc['Custo Investimento'])

max_candidatas = len(Pg_lim)
model.Pg = pyo.Var(range(max_candidatas), bounds=(0, None))
Pg = model.Pg

# # Restricoes
model.balanco = pyo.Constraint(expr=sum([Pg[g] for g in range(max_candidatas)]) == 1600)
model.limites = pyo.ConstraintList()
for g in range(max_candidatas):
    model.limites.add(expr=Pg[g] <= float(Pg_lim[g]))


# # Função Objetivo
model.fob = pyo.Objective(expr=sum([Pg[g]*float(uc_inv[g]) for g in range(max_candidatas)]))
opt = SolverFactory('glpk')
opt.solve(model)

model.pprint()

results = [pyo.value(Pg[g]) for g in range(max_candidatas)]
d = {'Usina': name_usi, 'Geração': results}
resultado = pd.DataFrame(d)
print(resultado)