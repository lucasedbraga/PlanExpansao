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
        edit.titulo('Planejamento da Geração - Estático')

    def custo_objetivo(self, model, data, details=False):
        Pg_lim = []
        uc_inv = []
        name_usi = []
        for usi in data:
            for uni in range(int(usi.loc['qte'])):
                name_usi.append(usi.loc['Tipo'][0])
                Pg_lim.append(usi.loc['Capacidade'])
                uc_inv.append(usi.loc['Custo Investimento'])

        NVAR = len(Pg_lim)
        model.Pg = pyo.Var(range(NVAR), bounds=(0, None))
        Pg = model.Pg
        model.balanco = pyo.Constraint(expr=sum([Pg[g] for g in range(NVAR)]) == 1600)
        model.limites = pyo.ConstraintList()
        for g in range(NVAR):
            model.limites.add(expr=Pg[g] <= float(Pg_lim[g]))
        # # Restricoes

        # # Função Objetivo
        model.fob = pyo.Objective(expr=sum([Pg[g] * float(uc_inv[g]) for g in range(NVAR)]))
        opt = SolverFactory('glpk')
        opt.solve(model)
        results = [pyo.value(Pg[g]) for g in range(NVAR)]

        edit.relatorio_titulo('CUSTO OBJETIVO ')
        d = {'Usina': name_usi, 'Geração': results}
        resultado = pd.DataFrame(d)
        edit.relatorio_item(resultado)

        if details:
            edit.relatorio_titulo('CUSTO OBJETIVO ')
            model.pprint()
            edit.relatorio_end()

        return results


    def custo_ambiental(self):
        pass


    def energia_n_suprida(self):
        pass


    def restricao_reserva_confiabilidade(self):
        pass

    def restricao_decisao(self):
        pass

    def restricao_combustivel(self):
        pass

    def FOB(self,cinv):
        pass

    def solve(self, details=False):
        cinv = self.custo_objetivo(self.model, self.data, details=details)
        self.FOB = cinv
        self.results = cinv
        return self.results

if __name__ == '__main__':
    print(PlanGer_Estatico().solve())


