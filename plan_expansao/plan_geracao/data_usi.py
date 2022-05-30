import pandas as pd

def gerate_data(path='tab_ex.xlsx'):
    usis_data = pd.read_excel(path, engine='openpyxl')
    usis = []
    #TODO melhorar leitura dos dados
    for i in range(len(usis_data)):
        usi = dict()
        leitura = usis_data.iloc[i, :]
        usi[leitura['Tipo']] = dict()
        for key in leitura.keys():
            usi[leitura['Tipo']][key] = leitura[key]
        usi = pd.DataFrame(usi)
        usis.append(usi)

    return usis

if __name__ == '__main__' :
    print(gerate_data())