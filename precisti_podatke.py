from pickle import FALSE
from pandas import *

#crypo_file_names = ["coin_Aave.csv",
#                    "coin_BinanceCoin.csv",
#                    "coin_Bitcoin.csv",
#                    "coin_Cardano.csv",
#                    "coin_ChainLink.csv",
#                    "coin_Cosmos.csv",
#                    "coin_CryptocomCoin.csv",
#                    "coin_Dogecoin.csv",
#                    "coin_EOS.csv",
#                    "coin_Ethereum.csv",
#                    "coin_Iota.csv",
#                    "coin_Litecoin.csv",
#                    "coin_Monero.csv",
#                    "coin_NEM.csv",
#                    "coin_Polkadot.csv",
#                    "coin_Solana.csv",
#                    "coin_Stellar.csv",
#                    "coin_Tether.csv",
#                    "coin_Tron.csv",
#                    "coin_Uniswap.csv",
#                    "coin_USDCoin.csv",
#                    "coin_WrappedBitcoin.csv",
#                    "coin_XRP.csv"]

crypo_file_names = ["coin_BinanceCoin.csv",
                    "coin_Bitcoin.csv",
                    "coin_Cardano.csv",
                    "coin_Dogecoin.csv",
                    "coin_EOS.csv",
                    "coin_Ethereum.csv",
                    "coin_Polkadot.csv",
                    "coin_Stellar.csv",
                    "coin_Tether.csv"]    
       

def ce_or_de_ex(ceEx):
    if ceEx:
        return "CeEx"
    else:
        return "DeEx"

# UPORABNIKI -- demo -- morda za druge namene
df = read_csv("podatki/raw/data_uporabniki.csv")
df = df[['CustomerId', 'Surname','Geography', 'Gender', 'Age']]
df.rename(columns={"CustomerId": "id_uporabnika", "Surname": "priimek", "Geography" : "drzava", "Gender": "spol", "Age": "starost"}, inplace=True)
#stoplci = df.columns.values.tolist()

# UPORABNIKI
uporabniki = read_csv("podatki/uporabniki/uporabnik.csv")
#print(uporabniki)

# BORZE
borza = read_csv("podatki/raw/exchanges.csv")
#borza = borza[['id', 'name','centralized', 'location']]
#borza.rename(columns={'id': "id_borze" , 'name' : "ime", 'location': "lokacija"}, inplace=True)
borza = borza[['name','centralized', 'location', 'website_url']]
borza.rename(columns={'name' : "ime", 'location': "lokacija", 'website_url' : "povezava"}, inplace=True)
borza['id_borze'] = list(range(1, len(borza)+1))
borza = borza[['id_borze', 'ime', 'centralized' ,'lokacija', 'povezava']]



vrsta = borza['centralized'].apply(ce_or_de_ex)
borza['centralized'] = vrsta
borza.rename(columns={'centralized' : "vrsta"}, inplace=True)

#print(borza)
#print(borza['lokacija'].value_counts()) #zanimivo
#borza.to_csv("podatki/borze/borza.csv", encoding='utf-8', index=False)


# CRYPTO
#def precisti_crypto(list_files):
#    crypto = DataFrame({'Symbol':[], 'Close':[], 'Date':[]})
#    for file_name in list_files:
#        coin = read_csv("podatki/raw/{0}".format(file_name))
#        coin = coin[['Symbol', 'Close', 'Date']]
#        crypto = crypto.append(coin)
#    crypto.rename(columns={'Symbol': "osnovna_valuta" , 'Close' : "valutno_razmerje", 'Date': "datum_razmerja"}, inplace=True)
#    n = len(crypto)
#    crypto["kotirajoca_valuta"] = ["USD"]*n
#    crypto = crypto[["osnovna_valuta", "kotirajoca_valuta", "valutno_razmerje", "datum_razmerja"]]
#    crypto.to_csv("podatki/crypto/crypto.csv", encoding='utf-8', index=False)
#    print("Uspesno precistil crypto podatke!")
#precisti_crypto(crypo_file_names)

def to_future(datumi):
    novi = []
    for datum in datumi:
        y, m, d  = datum.split('-')
        leto = str(int(y) + 4)
        novi.append('-'.join([leto, m, d]))
    return novi

def precisti_crypto(list_files):
    crypto = DataFrame({'Symbol':[], 'Close':[], 'Date':[]})
    for file_name in list_files:
        coin = read_csv("podatki/raw/{0}".format(file_name))
        coin = coin[['Symbol', 'Close', 'Date']]
        crypto = crypto.append(coin)
    crypto.rename(columns={'Symbol': "osnovna_valuta" , 'Close' : "valutno_razmerje", 'Date': "datum_razmerja"}, inplace=True)
    n = len(crypto)
    crypto["kotirajoca_valuta"] = ["USD"]*n
    datumi = crypto['datum_razmerja'].tolist()
    crypto['datum_razmerja'] = to_future(datumi)
    crypto = crypto[["osnovna_valuta", "kotirajoca_valuta", "valutno_razmerje", "datum_razmerja"]]
    crypto.to_csv("podatki/crypto/crypto.csv", encoding='utf-8', index=False)
    print("Uspesno precistil crypto podatke!")

#precisti_crypto(crypo_file_names)













