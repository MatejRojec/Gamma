from pickle import FALSE
from pandas import *

def ce_or_de_ex(ceEx):
    if ceEx:
        return "CeEx"
    else:
        return "DeEx"

df = read_csv("podatki/raw/data_uporabniki.csv")
df = df[['CustomerId', 'Surname','Geography', 'Gender', 'Age']]
df.rename(columns={"CustomerId": "id_uporabnika", "Surname": "priimek", "Geography" : "drzava", "Gender": "spol", "Age": "starost"}, inplace=True)
#stoplci = df.columns.values.tolist()

uporabniki = read_csv("podatki/uporabniki/uporabnik.csv")
#print(uporabniki)


borza = read_csv("podatki/raw/exchanges.csv")
#borza = borza[['id', 'name','centralized', 'location']]
#borza.rename(columns={'id': "id_borze" , 'name' : "ime", 'location': "lokacija"}, inplace=True)
borza = borza[['id', 'name','centralized', 'location', 'website_url']]
borza.rename(columns={'id': "id_borze" , 'name' : "ime", 'location': "lokacija", 'website_url' : "povezava"}, inplace=True)


vrsta = borza['centralized'].apply(ce_or_de_ex)
borza['centralized'] = vrsta
borza.rename(columns={'centralized' : "vrsta"}, inplace=True)
print(borza)
#print(borza['id_borze'].value_counts()) #zani


#borza.to_csv("podatki/borze/borza.csv", encoding='utf-8', index=False)


