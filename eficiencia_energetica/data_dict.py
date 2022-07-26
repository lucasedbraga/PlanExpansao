from pprint import pprint
import pandas as pd
df = pd.read_excel('data_efi.xlsx', engine='openpyxl').to_dict()
pprint(df)