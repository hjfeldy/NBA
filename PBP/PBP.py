import requests, bs4, re, pickle, datetime, os, re
import pandas as pd

reg = re.compile(r'\w\. \S+')
year1 = 1998
year2 = 2019


def month_id(website):   # returns a list of all the months in which games were played (stopping in April because idgaf about playoffs)
                            #Necessary because ther are lockout / pandemic seasons and each month has its own URL, so if I try to go to the november 2011 url and it doesnt exist...
    res = requests.get(website)
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    month_pattern = re.compile(r'October|November|December|January|February|March|April')
    months = {}
    for div in soup.find_all('div'):
        for a in div.find_all('a'): #Scans all links on the page for a month-match
            if month_pattern.search(a.text) != None:
                months[a.text] = 0
    
    return list(months.keys())

urls = []
url1 = 'https://www.basketball-reference.com/leagues/NBA_'
url2 = '_games-'
url3 = '.html'

for year in range(year1, year2 + 1):
    
    url = url1 + str(year) + '_games.html'
    for month in month_id(url):
        urls.append(url1 + str(year) + url2 + month.lower() + url3)

bs_links = [] #bs = "BoxScore"
i = 0
for url in urls: #loop thru the months to scrape every individual game's link
    i += 1
    print('Scraping Link', i, 'out of', len(urls))
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    table = soup.find('table',attrs = {'id':'schedule'})
    body = table.tbody
    for tr in body.find_all('tr'):
        td = tr.find('td', attrs = {'data-stat':'box_score_text'})
        
        if tr.th.text == 'Playoffs':
            break
        bs_links.append(td.a['href'])


urls = []#Convert the gameIDs to gettable links
for a in bs_links:
    urls.append(r'https://www.basketball-reference.com' + a[:11] + 'pbp/' + a[11:])

def getDate(string):
    year = int(string[51:55])
    month = int(string[55:57])
    day = int(string[57:59])
    return datetime.date(year, month, day)
def gameID(string):
    team = string[59:63]
    return str(getDate(string)) + team

def nameFix(name):
    return name.split('/')[-1][:-5]
def playFix(names, fixedNames, string):
    dex1 = string.find(names[0])
    len1 = len(names[0])

    if len(names) > 1:
        dex2 = string.find(names[1])
        len2 = string.find(names[1])

        return string[:dex1] + fixedNames[0] + string[dex1 + len1:dex2] + fixedNames[1] + string[dex2 + len2:]
    return string[:dex1] + fixedNames[0] + string[dex1 + len1:]

df = pd.DataFrame({ 'GameID': [], 'Time': [], 'Away': [], 'Score': [], 'Home': []})
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

        
        if len(list(row.find_all('td'))) != 6:
                
            continue
          
            
        i = 0
        
        for td in row.find_all('td'):
            txt = td.text
            if td.find('a') != None:
                fixedNames = []
                names = []
                for a in td.find_all('a'):
                    fixedNames.append(nameFix(a['href']))
                    names.append(a.text)
                
                txt = playFix(names, fixedNames, td.text)

            frame[columns[i]].append(txt)
            i += 1
            if i > 5:
                i = 0

    
    frame = pd.DataFrame(frame)
    del frame['Blank']
    del frame['Blank2']
    frame['GameID'] = [gid for _ in range(frame.shape[0])]
    df = pd.concat([df, frame])


count = 0
i = 0 
errors = open('errors.txt', 'w')
for url in urls:
    i += 1
    
    print(i, 'out of', len(urls))
    try:
        scrape(url)
    except Exception as e:
        errors.write(url + '\n')
    if i % 1000 == 0:
        count += 1 
        filename = 'pbp_raw' + str(count) + '.csv'
        df.to_csv(filename)
        df = pd.DataFrame({ 'GameID': [], 'Time': [], 'Away': [], 'Score': [], 'Home': []})

    
count += 1

filename = 'pbp_raw' + str(count) + '.csv'
errors.close()