#data = [['BitStamp', 'DenarnicaBTC', 34],['BitStamp', 'DenarnicaETH', 12],['BitStamp', 'DenarnicaUSD', 23400],['Binance', 'DenarnicaBTC', 1],['Binance', 'DenarnicaADA', 12000], ['Binance', 'DenarnicaAgd', 120],['Coinbase', 'DenarnicaUSD', 100],['Coinbase', 'DenarnicaADA', 12000]]
data = [['BitStamp', 'DenarnicaBTC', 34],['Bi', 'DenarnicaBTC', 4828]]
data = [['BitStamp', 'DenarnicaBTC', 34],['Bi', 'DenarnicaBTC', 4828], ['Ba', 'DenarnicaBTC', 28]]
data = [['BitStamp', 'DenarnicaBTC', 34]]
data = [['Binance', 'ADA', 50.0], ['Binance', 'USD', 660.0], ['Bitstamp', 'USD', 100.0], ['FTX', 'ETH', 1.0], ['FTX', 'USD', 200.0]]

st = 0
borza = data[0][0] if len(data) > 0 else []

n= len(data)
if n == 0:
    print("")
elif n == 1:
    print('Borza:',data[0][0])
    print(data[0][1], 'ima stanje:', data[0][2])
    input("dodaj denarnico:")
else:
    st = 0
    for i in range(n-1):
        if  st == 0 and data[i][0] == data[i+1][0]:
            print('Borza:',data[i][0])
            print(data[i][1], 'ima stanje:', data[i][2])
            st = 1
        elif st == 0 and data[i][0] != data[i+1][0]:
            print('Borza:',data[i][0])
            print(data[i][1], 'ima stanje:', data[i][2])
            input("dodaj denarnico:")
            st = 0
        elif data[i][0] == data[i+1][0]:
            print(data[i][1], 'ima stanje:', data[i][2])
        elif data[i][0] != data[i+1][0]:
            print(data[i][1], 'ima stanje:', data[i][2])
            input("dodaj denarnico:")
            st = 0    
    if data[n-2][0]!= data[n-1][0]:
        print('Borza:',data[n-1][0])
        print(data[n-1][1], 'ima stanje:', data[n-1][2])
        input("dodaj denarnico:")
    else:
        print(data[n-1][1], 'ima stanje:', data[n-1][2])
        input("dodaj denarnico:")

