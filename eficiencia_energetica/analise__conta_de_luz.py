# from pprint import pprint
# import pandas as pd
# df = pd.read_excel('data_efi.xlsx', engine='openpyxl').to_dict()
# pprint(df)


def calculo_demanda(medido, contratado, tarifa):
  faturado = max(medido, contratado)
  valor = faturado*tarifa
  if faturado > 1.05*contratado:
    valor += (faturado-medido)*2*tarifa
  return valor

def calculo_energia(medido, tarifa):
  return medido*tarifa

def max_consumo(p, fp):
  return max([p, fp])

P_fp = 442000
Q_fp = 180000
P_p = 62000
Q_p = 20000

demanda_fp = 1160
demanda_ponta = 1140
energia_consumida_fp = P_fp
energia_consumida_ponta = P_p


tarifa_demanda_ponta = 44.90
tarifa_demanda_fp = 14.86
tarifa_consumo_ponta = 495.66/1000
tarifa_consumo_fp = 346.64/1000
tarifa_unica = 14.86
tarifa_verde_consumo_p = 1583.06/1000
tarifa_verde_consumo_fp = 346.64/1000
demanda_contratada_fp = 1400
demanda_contratada_p = 1400



data_hist = {'consumo_fora_ponta': {0: 442000,
                        1: 408000,
                        2: 434000,
                        3: 370000,
                        4: 386000,
                        5: 356000,
                        6: 372000,
                        7: 358000,
                        8: 346000,
                        9: 348000,
                        10: 350000,
                        11: 328000,
                        12: 346000},
 'consumo_ponta': {0: 62000,
                   1: 44000,
                   2: 48000,
                   3: 40000,
                   4: 38000,
                   5: 38000,
                   6: 38000,
                   7: 36000,
                   8: 36000,
                   9: 38000,
                   10: 38000,
                   11: 36000,
                   12: 36000},
 'demanda_fora_ponta': {0: 1160,
                        1: 1000,
                        2: 1060,
                        3: 900,
                        4: 880,
                        5: 840,
                        6: 860,
                        7: 680,
                        8: 680,
                        9: 680,
                        10: 620,
                        11: 600,
                        12: 620},
 'demanda_ponta': {0: 1140,
                   1: 1020,
                   2: 920,
                   3: 820,
                   4: 760,
                   5: 680,
                   6: 740,
                   7: 680,
                   8: 700,
                   9: 660,
                   10: 660,
                   11: 620,
                   12: 620},
 'mês': {0: 'MAR/19',
         1: 'FEV/19',
         2: 'JAN/19',
         3: 'DEZ/18',
         4: 'NOV/18',
         5: 'OUT/18',
         6: 'SET/18',
         7: 'AGO/18',
         8: 'JUL/18',
         9: 'JUN/18',
         10: 'MAI/18',
         11: 'ABR/18',
         12: 'MAR/18'}}

def make_hist(key, data=data_hist):
    hist = []
    keys = [key for key in data['mês'].keys()]
    for d in reversed(keys):
        hist.append(data[key][d])
    return hist
hist_demanda_p = make_hist('demanda_ponta')
hist_demanda_fp = make_hist('demanda_fora_ponta')
hist_consumo_p = make_hist('consumo_ponta')
hist_consumo_fp = make_hist('consumo_fora_ponta')

hist_dp_tarifa_azul = []
for registro in hist_demanda_p:
    hist_dp_tarifa_azul.append(calculo_demanda(registro, demanda_contratada_p, tarifa_demanda_ponta))
hist_dfp_tarifa_azul = []
for registro in hist_demanda_fp:
    hist_dfp_tarifa_azul.append(calculo_demanda(registro, demanda_contratada_fp, tarifa_demanda_fp))
hist_enep_tarifa_azul = []
for registro in hist_consumo_p:
    hist_enep_tarifa_azul.append(calculo_energia(registro, tarifa_consumo_ponta))
hist_enefp_tarifa_azul = []
for registro in hist_consumo_fp:
    hist_enefp_tarifa_azul.append(calculo_energia(registro, tarifa_consumo_fp))


print(hist_dp_tarifa_azul, hist_dfp_tarifa_azul, hist_enep_tarifa_azul, hist_enefp_tarifa_azul)

hist_dp_tarifa_verde = []
for registro in hist_demanda_p:
    hist_dp_tarifa_verde.append(registro)
hist_dfp_tarifa_verde = []
for registro in hist_demanda_fp:
    hist_dfp_tarifa_verde.append(registro)
hist_demanda_verde = []
for r in range(len(hist_dfp_tarifa_verde)):
  hist_demanda_verde.append(calculo_demanda(max_consumo(hist_dp_tarifa_verde[r],hist_dfp_tarifa_verde[r]), max_consumo(demanda_contratada_p, demanda_contratada_fp), tarifa_unica))
hist_enep_tarifa_verde = []
for registro in hist_consumo_p:
    hist_enep_tarifa_verde.append(calculo_energia(registro, tarifa_verde_consumo_p))
hist_enefp_tarifa_verde = []
for registro in hist_consumo_fp:
    hist_enefp_tarifa_verde.append(calculo_energia(registro, tarifa_verde_consumo_fp))

print(hist_demanda_verde, hist_enep_tarifa_verde, hist_enefp_tarifa_verde)