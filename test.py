


data = [['BitStamp', 'DenarnicaBTC', 34],['BitStamp', 'DenarnicaETH', 12],['BitStamp', 'DenarnicaUSD', 23400],['Binance', 'DenarnicaBTC', 1],['Binance', 'DenarnicaADA', 12000], ['Coinbase', 'DenarnicaUSD', 100]]
st = 0
borza = data[0][0] if len(data) > 0 else []
while len(data) > 0:
    if borza == data[0][0] and st == 0:
        print('Borza:',borza)
        print(data[0][1], 'ima stanje:', data[0][2])
        borza = data[0][0]
        st = 1 
        data = data[1:] if len(data) > 0 else []
    elif borza == data[0][0]:
        print(data[0][1], 'ima stanje:', data[0][2])
        borza = data[0][0]
        data = data[1:] if len(data) > 0 else []
    else:
        print('Borza:',borza)
        print(data[0][1], 'ima stanje:', data[0][2])
        borza = data[0][0]
        data = data[1:] if len(data) > 0 else []

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
