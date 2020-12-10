import pickle
import pandas as pd

with open('possessions.pickle', 'rb') as pik:
        pos = pickle.load(pik)

master = {}

df = {'GameID': [] , 'Player': []}
for i in range(1, 12):
    df[i] = []

def push(lst, val):
    if len(lst) < 11:
        return [val] + lst
    else:
        return [val] + lst[:10]

for gameID in pos.keys():
    for player in pos[gameID].keys():
        df['Player'].append(player)
        df['GameID'].append(gameID)
        usg = pos[gameID][player]

        if player not in master.keys():
            master[player] = [usg]
            df[1].append(usg)
            for i in range(2, 12):
                df[i].append(0)
        else:
            master[player] = push(master[player], usg)
        
            for i in range(1, 12):
                try:
                    df[i].append(master[player][i - 1])
                except IndexError:
                    df[i].append(0)

df = pd.DataFrame(df).rename(columns={1:'Today'})
df.to_csv('USG.csv')

