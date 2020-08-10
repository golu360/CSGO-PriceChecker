import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.options.mode.chained_assignment = None

wears = {
    'ST-FN':1,
    'ST-MW':2,
    'ST-FT':3,
    'ST-WW':4,
    'ST-BS':5,
    'FN':6,
    'MW':7,
    'FT':8,
    'WW':9,
    'BS':10
    
}

data = pd.read_csv('prices.csv')
data['price']=data['price'].fillna(0)

print('[*]Fetching Prices..')

for i in range(len(data['link'])):
    
    
    if data['type'][i]=='sticker':
        
        print(data['type'][i])
        page = requests.get(data['link'][i])
        text = data['link'][i].split('/')
    
        text = text[5].replace('-'," ")


        soup = BeautifulSoup(page.content,'html.parser')

        result = soup.find_all("div",class_='btn-group btn-group-justified')


        price = result[0].find("span",class_='pull-right')
        link = result[0].find('a')['href']
    
        print(' {} :: {}\n'.format(text,price.text[0:4]))
    
        data.at[i,'price']=int(price.text[1:4])
        data['name'][i]=text
        
        
    if data['type'][i]=='skin':
        print(data['type'][i])
        text = data['link'][i].split('/')
        text = text[5].replace('-'," ")
        
        a= data.isnull()
        if a['wear'][i]:
            print('No wear specified for {}'.format(text))
            break
        
        
        
        index = data['wear'][i]
        index = wears[index]
        
        page = requests.get(data['link'][i])
        
        
        
        
        
        soup = BeautifulSoup(page.content,'html.parser')
        r = soup.find_all("div",class_='btn-group-sm btn-group-justified')
        

        price=r[index].find("span",class_='pull-right')
        price=price.text[1:].replace(',',"")
        
        
        print(' {} :: {}\n'.format(text,price))
    
        data.at[i,'price']=int(price)
        data['name'][i]=text
        
       
        
    
    
data.to_csv('prices.csv',index=False)
print("Total Price: "+str(sum(data['price'])))    
print('\n[*]Fetching Complete,please check CSV for more.')    