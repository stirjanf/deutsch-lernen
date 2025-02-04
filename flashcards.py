import pandas as pd
from colorama import Fore, Style
import random
import os

def select():
    os.system('cls')
    while True:
        n = input(f"How many words do you want to practice? > ").strip()
        if n == "q":
            exit()
        if n:
           break   
    os.system('cls')
    print(f"[1] - Glagoli\n[2] - Imenice\n[3] - Pridjevi\n[4] - Prijedlozi i ostalo\n[5] - Sve\n[Q] - Quit")
    while True:
        opt = input(f"What do you want to practice? > ").strip()
        if opt == "q":
            exit()
        if opt:
            return int(n),int(opt)

def play(obj):
    os.system('cls')
    unused = obj
    n = len(obj)
    used = []
    while unused:
        entry = random.choice(unused)
        used.append(entry)
        inpt = input(f"\n{Fore.GREEN}Riječ {len(used)}/{n}: {Fore.BLUE}{entry[-1]} {Style.RESET_ALL}> ")
        if inpt == "q":
            break    
        strng = " - ".join(map(str, entry[1:-1])) 
        print(f"{Fore.YELLOW}{strng}{Style.RESET_ALL}")
        unused.remove(entry)
        if not unused:
            break

data = []
print(f"Fetching data...")
for sheet in ["Glagoli", "Imenice", "Pridjevi", "Prilozi"]:
    df = pd.read_excel(r"C:\Users\User\OneDrive\Belgeler\deutsch.xlsx", sheet_name=sheet, header=1)
    words = []
    for index,row in df.iterrows():
        temp = []
        for column_name, value in row.items():
            if "Unnamed" not in column_name:
                if value == "sl":
                    break
                temp.append(str(value).strip())
        if temp:
            words.append(temp)
    data.append(words)

while True:
    nwords,opt = select()
    if opt == 5:
        words = []
        for i in range(len(data)):
            words.append((data[i])[:nwords])
        play([item for sublist in words for item in sublist])
    else:
        play(data[opt-1][:nwords])