import pandas as pd
from utils import Editor as edit
import data_usi
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

class PlanGer_Estatico:
    def __init__(self):
        self.model = pyo.ConcreteModel()
        self.data = data_usi.gerate_data()
        self.ger_obj = 1600
        edit.titulo('Planejamento da Geração - Estático')

    def custo_investimento(self, model, data, details=False):

        #Declarando Variáveis
        Pg_lim = []
        uc_inv = []
        name_usi = []
        for usi in data:
            for uni in range(int(usi.loc['novas'])):
                name_usi.append(usi.loc['Tipo'][0])
                Pg_lim.append(usi.loc['Capacidade'])
                uc_inv.append(usi.loc['Custo Investimento'])


        NVAR = len(Pg_lim)
        model.Pg = pyo.Var(range(NVAR), bounds=(0, None))
        Pg = model.Pg
        model.limites = pyo.ConstraintList()
        for g in range(NVAR):
            model.limites.add(expr=Pg[g] <= float(Pg_lim[g]))

        # Restricoes
        model.balanco = pyo.Constraint(expr=sum([Pg[g] for g in range(NVAR)]) == self.ger_obj)

        # Função Objetivo
        model.fob = pyo.Objective(expr=sum([Pg[g] * float(uc_inv[g]) for g in range(NVAR)]))
        opt = SolverFactory('glpk')
        opt.solve(model)
        results = [pyo.value(Pg[g]) for g in range(NVAR)]

        edit.relatorio_titulo('CUSTO investimento ')
        d = {'Usina': name_usi, 'Geração': results}
        resultado = pd.DataFrame(d)
        edit.relatorio_item(resultado)

        if details:
            edit.relatorio_titulo('CUSTO investimento ')
            model.pprint()
            edit.relatorio_end()

        return results

    def custo_combustivel(self, model, data, details=False):
        # Declarando Variáveis
        pot_despachada = {'leve':[],'media':[],'pesada':[]}
        duracao_patamar = {'leve':[],'media':[],'pesada':[]}
        custo_combustivel = []
        name_usi = []
        for usi in data:
            for uni in range(int(usi.loc['novas'])):
                name_usi.append(usi.loc['Tipo'][0])
                pot_despachada['leve'].append(usi.loc['despacho_leve'])
                duracao_patamar['leve'].append(usi.loc['duracao_leve'])
                custo_combustivel.append(usi.loc['Custo Combustivel'])

        NVAR = len(name_usi)
        # model.Pd = pyo.Var(range(NVAR), bounds=(0, None))
        # Pd = model.Pd
        # model.limites = pyo.ConstraintList()
        custo_comb = []
        for u in range(NVAR):
            # for patamar in pot_despachada.keys():
            #     custo = float(custo_combustivel[u])*float(pot_despachada[patamar][u])*float(duracao_patamar[patamar][u])
            #     print(custo)
            #     custo_comb.append(custo)
            custo = float(custo_combustivel[u])*float(pot_despachada['leve'][u])*float(duracao_patamar['leve'][u])
            custo_comb.append(custo)

        return custo_comb




    def solve(self, details=False):
        #cinv = self.custo_investimento(self.model, self.data, details=details)
        ccomb = self.custo_combustivel(self.model, self.data, details=details)
        print(ccomb)
        #self.FOB = cinv
        #self.results = cinv
        #return self.results

if __name__ == '__main__':
    print(PlanGer_Estatico().solve())



