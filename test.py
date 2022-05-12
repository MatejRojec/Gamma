


#data = [['BitStamp', 'DenarnicaBTC', 34],['BitStamp', 'DenarnicaETH', 12],['BitStamp', 'DenarnicaUSD', 23400],['Binance', 'DenarnicaBTC', 1],['Binance', 'DenarnicaADA', 12000], ['Binance', 'DenarnicaAgd', 120],['Coinbase', 'DenarnicaUSD', 100],['Coinbase', 'DenarnicaADA', 12000]]
data = [['BitStamp', 'DenarnicaBTC', 34],['Bi', 'DenarnicaBTC', 4828]]
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
        if  st == 0:
            print('Borza:',data[i][0])
            print(data[i][1], 'ima stanje:', data[i][2])
            st = 1
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









#if len(data) == 1:
#    print('Borza:',borza)
#    print(data[0][1], 'ima stanje:', data[0][2])
#    input("dodaj denarnico:")
#else:
#    while len(data) > 1:
#        if borza == data[0][0] and st == 0 and data[0][0] == data[1][0]:
#            print('Borza:',borza)
#            print(data[0][1], 'ima stanje:', data[0][2])
#            borza = data[0][0]
#            st = 1 
#            data = data[1:] if len(data) > 0 else []
#        elif borza == data[0][0]:
#            print(data[0][1], 'ima stanje:', data[0][2])
#            borza = data[0][0]
#            data = data[1:] if len(data) > 0 else []
#        else:
#            print('Borza:',data[0][0])
#            print(data[0][1], 'ima stanje:', data[0][2])
#            borza = data[0][0]
#            data = data[1:] if len(data) > 0 else []

#if len(data) == 0:
#else:
#    for i in range(len(data)):
#        if len(data) == 1


#Aum = {{aum}}
#% if len(data) == 0:
#{{''}}
#
#%st = 0
#%borza = data[0][0] if len(data) > 0 else []
#%while len(data) > 0:
#%   if borza == data[0][0] and st == 0:
#{{borza}}
#{{data[0][1]}} ima stanje: {{data[0][2]}}
#%       borza = data[0][0]
#%       st =1 
#%       data = data[1:] if len(data) > 0 else []
#%   elif borza == data[0][0]:
#{{data[0][1]}} ima stanje: {{data[0][2]}}
#%       borza = data[0][0]
#%       data = data[1:] if len(data) > 0 else []
#%   else:
#{{borza}}
#{{data[0][1]}} ima stanje: {{data[0][2]}}
#%       borza = data[0][0]
#%       data = data[1:] if len(data) > 0 else []
#%   end
#%end
