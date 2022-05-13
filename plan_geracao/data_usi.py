import pandas as pd

def gerate_data(path='tab_ex.xlsx'):
    usis_data = pd.read_excel(path, engine='openpyxl')
    usis = []
    for i in range(len(usis_data)):
        usi = dict()
        leitura = usis_data.iloc[i, :]
        usi[leitura['Tipo']] = dict()
        for key in leitura.keys():
            if key == 'Tipo':
                pass
            else:
                usi[leitura['Tipo']][key] = leitura[key]
        usis.append(usi)

    return usis

if __name__ == '__main__' :
    print(gerate_data())