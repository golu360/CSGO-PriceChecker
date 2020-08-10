import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.options.mode.chained_assignment = None
data = pd.read_csv('prices.csv')

print('[*]Fetching Prices..')

for i in range(len(data['link'])):
    page = requests.get(data['link'][i])
    text = data['link'][i].split('/')
    text = text[5].replace('-'," ")


    soup = BeautifulSoup(page.content,'html.parser')

    result = soup.find_all("div",class_='btn-group btn-group-justified')
#price = result.find_all('span', class_='market_commodity_orders_header_promote')

    price = result[0].find("span",class_='pull-right')
    link = result[0].find('a')['href']
    
    print(' {} :: {}\n'.format(text,price.text[0:4]))
    
    data.at[i,'price']=int(price.text[1:4])
    data['name'][i]=text
    data.to_csv('prices.csv',index=False) 

print("Total Price: "+str(sum(data['price'])))    
print('\n[*]Fetching Complete,please check CSV for more.')    