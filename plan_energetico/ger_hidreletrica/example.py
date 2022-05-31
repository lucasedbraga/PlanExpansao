import pyomo.environ as pyo
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()
model.Pg1 = pyo.Var(range(4), bounds=(0, None))
model.Pg2 = pyo.Var(range(4), bounds=(0, None))
Pg1 = model.Pg1
Pg2 = model.Pg2
model.balancoM1 = pyo.Constraint(expr=sum([Pg1[g] for g in range(4)]) == 6)
model.balancoM2 = pyo.Constraint(expr=sum([Pg2[g] for g in range(4)]) == 6)
model.limites = pyo.ConstraintList()

model.limites.add(expr=Pg1[0] <= 1)
model.limites.add(expr=Pg2[0] <= 1)
model.limites.add(expr=Pg1[1] <= 1)
model.limites.add(expr=Pg2[1] <= 1)


model.volume = pyo.Var(range(2), bounds=(0, None))
vol = model.volume
model.balanco_hidricoM1 = pyo.Constraint(expr=vol[0] + Pg1[3] == 6)
model.balanco_hidricoM2 = pyo.Constraint(expr=vol[1] + Pg2[3] - vol[0] == 2)

custo1 = 0.25*Pg1[0] + 0.75*Pg1[1] + 2.5*Pg1[2]
custo2 = 0.25*Pg2[0] + 0.75*Pg2[1] + 2.5*Pg2[2]

model.fob = pyo.Objective(expr=custo1+custo2)
model.pprint()
opt = SolverFactory('glpk')
opt.solve(model)
resultsM1 = [pyo.value(Pg1[g]) for g in range(4)]
resultsM2 = [pyo.value(Pg2[g]) for g in range(4)]
resultsAgua = [pyo.value(vol[g]) for g in range(2)]

print(f'Geração Mês 1 \n {resultsM1}')
print(f'Geração Mês 2 \n {resultsM2}')
print(f'Volume Armazenado de Água \n {resultsAgua}')