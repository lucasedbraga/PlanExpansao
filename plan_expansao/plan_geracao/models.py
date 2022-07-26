import numpy as np
import pandas as pd
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import data_usi
from utils import Editor as edit


class PlanGer_Estatico:
    def __init__(self):
        self.model = pyo.ConcreteModel()
        self.data = data_usi.gerate_data()
        self.limite_emissao = 1000
        self.demanda_ponta = 1200
        self.reserva_capacidade = 0.2
        self.limite_lolp = 2
        edit.titulo('Planejamento da Geração - Estático')

    def custo_investimento(self, data, details=False):
        Pg_lim = []
        self.uc_inv = []
        self.name_usi = []
        self.model.candidatas = pyo.VarList(domain=pyo.Integers, bounds=(0, 1))
        self.list_candidatas = self.model.candidatas
        for usi in data:
            for uni in range(int(usi.loc['novas'])):
                self.name_usi.append(usi.loc['Tipo'][0])
                Pg_lim.append(usi.loc['Capacidade'])
                self.uc_inv.append(usi.loc['Custo Investimento'])
                self.list_candidatas.add()
        self.NVAR = len(Pg_lim)
        self.model.Pg = pyo.Var(range(self.NVAR), bounds=(0, None))
        self.Pg = self.model.Pg
        self.model.limites = pyo.ConstraintList()
        for g in range(self.NVAR):
            self.model.limites.add(expr=self.Pg[g] <= float(Pg_lim[g]))
        self.model.balanco = pyo.Constraint(expr=sum([self.list_candidatas[g + 1] * self.Pg[g] for g in range(self.NVAR)]) == self.demanda_ponta)


    def custo_combustivel(self, model, data, details=False):
        # Declarando Variáveis
        pot_despachada = {'ponta': [], 'fora_ponta': []}
        custo_combustivel = []
        name_usi = []
        for usi in data:
            for uni in range(int(usi.loc['novas'])):
                name_usi.append(usi.loc['Tipo'][0])
                pot_despachada['ponta'].append(self.demanda_ponta)
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
            custo = float(custo_combustivel[u]) * float(pot_despachada['ponta'][u])
            custo_comb.append(custo)

        return custo_comb

    def custo_oem(self, model, data, details=False):
        # Declarando Variáveis
        pot_despachada = {'ponta': [], 'fora_ponta': []}
        custo_variavel = []
        custo_fixo = []
        name_usi = []
        Pg_lim = []
        for usi in data:
            for uni in range(int(usi.loc['novas'])):
                name_usi.append(usi.loc['Tipo'][0])
                # TODO demanda_ponta tem 2h, e o nome ta errado. O nome correto é duração
                pot_despachada['ponta'].append(self.demanda_ponta)
                custo_variavel.append(usi.loc['OeM vari'])
                custo_fixo.append(usi.loc['OeM fixo'])
                Pg_lim.append(usi.loc['Capacidade'])

        NVAR = len(name_usi)
        # model.Pd = pyo.Var(range(NVAR), bounds=(0, None))
        # Pd = model.Pd
        # model.limites = pyo.ConstraintList()
        custo_oem_var = []
        for u in range(NVAR):
            # for patamar in pot_despachada.keys():
            #     custo = float(custo_combustivel[u])*float(pot_despachada[patamar][u])*float(duracao_patamar[patamar][u])
            #     print(custo)
            #     custo_comb.append(custo)
            custo = float(custo_variavel[u]) * float(pot_despachada['ponta'][u])
            custo_oem_var.append(custo)

        custo_fixo = [float(Pg_lim[u]) * float(custo_fixo[u]) for u in range(NVAR)]

    def custo_ambiental(self, model, data, details=False):
        # Declarando Variáveis
        pot_despachada = {'ponta': [], 'fora_ponta': []}
        emissao = []
        name_usi = []
        for usi in data:
            for uni in range(int(usi.loc['novas'])):
                name_usi.append(usi.loc['Tipo'][0])
                pot_despachada['ponta'].append(self.demanda_ponta)
                emissao.append(usi.loc['Emissao'])

        NVAR = len(name_usi)
        # model.Pd = pyo.Var(range(NVAR), bounds=(0, None))
        # Pd = model.Pd
        # model.limites = pyo.ConstraintList()
        custo_emissao = []
        for u in range(NVAR):
            # for patamar in pot_despachada.keys():
            #     custo = float(custo_combustivel[u])*float(pot_despachada[patamar][u])*float(duracao_patamar[patamar][u])
            #     print(custo)
            #     custo_comb.append(custo)
            custo = float(emissao[u]) * float(pot_despachada['ponta'][u])
            custo_emissao.append(custo)

        emissao_total = sum(custo_emissao)
        custo_amb = emissao_total - self.limite_emissao

        return custo_amb

    def energia_n_suprida(self):
        pass

    def restricao_reserva_confiabilidade(self, model, data, details=False):
        reserva = (1 + self.reserva_capacidade) * self.demanda_ponta
        if sum(self.geracao_candidata) >= reserva:
            edit.aviso('ATENDE A RESTRIÇÃO DE RESERVA')
        # model.r_reserva = pyo.Constraint(expr=sum(self.geracao_candidata) >= reserva)

    def restricao_decisao(self):
        pass

    def restricao_combustivel(self, model, data, details=False):
        # Declarando Variáveis
        lim_combustivel = []
        combustivel_utilizado = []
        name_usi = []
        for usi in data:
            for uni in range(int(usi.loc['novas'])):
                name_usi.append(usi.loc['Tipo'][0])
                lim_combustivel.append(usi.loc['limite_comb'][0])
                combustivel_utilizado.append(float(usi.loc['consumo'][0]) * self.demanda_ponta)

        NVAR = len(name_usi)
        for g in range(NVAR):
            if combustivel_utilizado[g] > lim_combustivel[g]:
                edit.aviso(f'COMBUSTIVEL INSUFICIENTE PARA {name_usi[g]}')
            # model.r_limites_comb.add(expr=combustivel_utilizado[g] <= float(lim_combustivel[g]))

    def FOB(self, details):
        self.model.fob = pyo.Objective(expr=sum([self.list_candidatas[g + 1] * self.Pg[g] * float(self.uc_inv[g]) for g in range(self.NVAR)]))
        opt = SolverFactory('mindtpy')
        opt.solve(self.model, mip_solver='glpk', nlp_solver='ipopt')
        results = [pyo.value(self.Pg[g]) for g in range(self.NVAR)]
        construct = [pyo.value(self.list_candidatas[g]) for g in range(1, self.NVAR + 1)]
        self.geracao_candidata = results
        edit.relatorio_titulo('CUSTO OBJETIVO ')
        d = {'Usina': self.name_usi, 'Geração': np.array(results) * np.array(construct), 'Decisão': construct}
        resultado = pd.DataFrame(d)
        if details:
            self.model.pprint()
            edit.relatorio_titulo('CUSTO OBJETIVO ')
            edit.relatorio_item(resultado)
            edit.relatorio_end()
            print(f'DEMANDA ATENDIDA={sum(resultado.Geração)} / DEMANDA SOLICIDATDA = {self.demanda_ponta}')

    def solve(self, details=True):
        cinv = self.custo_investimento(self.data, details=details)
        ccomb = self.custo_combustivel(self.model, self.data, details=details)
        coem = self.custo_oem(self.model, self.data, details=True)
        cam = self.custo_ambiental(self.model, self.data, details=True)
        #rrc = self.restricao_reserva_confiabilidade(self.model, self.data, details=True)
        rcomb = self.restricao_combustivel(self.model, self.data, details=True)
        self.FOB(details=True)



if __name__ == '__main__':
    print(PlanGer_Estatico().solve())
