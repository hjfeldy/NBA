import requests, bs4, os, re, pickle
import pandas as pd
os.chdir('/home/harry/Repos/Nbav2/Important_CSVs')

df = pd.read_csv('1998_2019_raw.csv')

players = list(df['Starters'].unique())

del df

print(len(players))
pdict = {}

i = 0
for player in players:
    i += 1
    print(i, 'out of 2055')
    url = 'https://www.basketball-reference.com/players/' + player[0] + '/' + player + '.html'
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
   
    for strong in soup.find_all('strong'):
        if 'Born' in strong.text:
            pdict[player] = re.compile('\d\d\d\d').search(strong.parent.text).group(0)


with open('ages.pickle', 'wb') as pik:
    pickle.dump(pdict, pik)
        