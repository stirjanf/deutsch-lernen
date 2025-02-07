import pandas as pd
from colorama import Fore, Style
import random
import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def select(sheets):
    os.system('cls')
    while True:
        n = input(f"How many words do you want to practice? (x = all)> ").strip()
        if n == "q":
            exit()
        if n:
           break   
    os.system('cls')
    for sheet,i in zip(sheets,range(len(sheets))):
        print(f"[{i+1}] - {sheet}")
    print(f"[5] - All\n[Q] - Quit")
    while True:
        opt = input(f"What do you want to practice? > ").strip()
        if opt == "q":
            exit()
        if opt and n == "x":
            return n,int(opt)
        if opt:
            return int(n),int(opt)


def play(obj):
    os.system('cls')
    unused = obj
    n = len(obj)
    used = []
    to_learn = []
    while unused:
        entry = random.choice(unused)
        used.append(entry)
        inpt = input(f"\n{Fore.GREEN}Riječ {len(used)}/{n}: {Fore.BLUE}{entry[-1]} {Style.RESET_ALL}> ")
        if inpt == "q":
            break    
        if inpt != "da":
            to_learn.append(entry)
        strng = " - ".join(map(str, entry[1:-1])) 
        print(f"{Fore.YELLOW}{strng}{Style.RESET_ALL}")
        unused.remove(entry)
        if not unused:
            pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
            score = n-len(to_learn)
            print(f"{Fore.YELLOW}Score: {score}/{n} ({(score/n)*100})%{Style.RESET_ALL}")
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                c = canvas.Canvas(tmp.name, pagesize=letter)
                c.setFont("Arial", 12)
                y = 750
                for item in to_learn:
                    item = str(item)
                    c.drawString(100,y,item)
                    y -= 20
                c.save()
            os.startfile(tmp.name)
            input(f"Press enter to leave...")
            break

data = []
filename = r"C:\Users\User\OneDrive\Belgeler\deutsch.xlsx"
file = pd.ExcelFile(filename)
sheets = file.sheet_names
print(f"Fetching data...")
for sheet in sheets:
    df = pd.read_excel(filename, sheet_name=sheet, header=1)
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
    nwords,opt = select(sheets)
    if opt == 5:
        words = []
        if nwords == "x":
            for i in range(len(data)):
                words.append((data[i]))
        else: 
            for i in range(len(data)):
                words.append((data[i])[:nwords])
        play([item for sublist in words for item in sublist])
    else:
        if nwords == "x":
            play(data[opt-1])
        else:
            play(data[opt-1][:nwords])