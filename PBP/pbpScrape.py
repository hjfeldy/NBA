import requests, bs4, datetime
import pandas as pd

def getDate(string):
    year = int(string[51:55])
    month = int(string[55:57])
    day = int(string[57:59])
    return datetime.date(year, month, day)
def gameID(string):
    team = string[59:62]
    return str(getDate(string)) + team

df = pd.DataFrame({ 'Time': [], 'Away': [], 'Score': [], 'Home': []})
def scrape(url):
    global df
    gid = gameID(url) 
    res = requests.get(url)

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    pbp = soup.find(attrs={'id':'pbp'})

    frame = { 'Time': [], 'Away': [], 'Blank': [], 'Score': [], 'Blank2': [], 'Home': [] }
    columns = list(frame.keys())
    i = 0
    for row in pbp.find_all('tr'):

        try:
            if len(list(row.find_all('td'))) != 6:
                print(row.find_all('td'))
                continue
        except Exception as e:
          
            print(len(list(row.find_all('td'))))
            continue
        i = 0
        
        for td in row.find_all('td'):
            frame[columns[i]].append(td.text)
            i += 1
            if i > 5:
                i = 0

    
    frame = pd.DataFrame(frame)
    del frame['Blank']
    del frame['Blank2']

    df = pd.concat([df, frame])
    # return frame


urls = ['https://www.basketball-reference.com/boxscores/pbp/201910220LAC.html', 'https://www.basketball-reference.com/boxscores/pbp/201910240GSW.html']

for u in urls:
    scrape(u)

print(df)

