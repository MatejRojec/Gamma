from pandas import *

def ce_or_de_ex(ceEx):
    if ceEx:
        return "CeEx"
    else:
        return "DeEx"

df = read_csv("podatki/uporabniki/data_uporabniki.csv")
df = df[['CustomerId', 'Surname','Geography', 'Gender', 'Age']]
df.rename(columns={"CustomerId": "id_uporabnika", "Surname": "priimek", "Geography" : "drzava", "Gender": "spol", "Age": "starost"}, inplace=True)
#stoplci = df.columns.values.tolist()

uporabniki = read_csv("podatki/uporabniki/uporabnik.csv")
print(uporabniki)


borza = read_csv("podatki/borze/exchanges.csv")
borza = borza[['id', 'name','1d.volume','centralized', 'location', 'website_url']]
borza.rename(columns={'id': "id_boze" , 'name' : "ime",'1d.volume' : "volumen", 'location': "lokacija", 'website_url' : "povezava"}, inplace=True)

vrsta = borza['centralized'].apply(ce_or_de_ex)
borza['centralized'] = vrsta
borza.rename(columns={'centralized' : "vrsta"}, inplace=True)
print(borza)
#print(borza['lokacija'].value_counts()) #zani