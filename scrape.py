import requests
from bs4 import BeautifulSoup
import pdfkit

alphabet = ['a', 'b', 'c', 'č', 'ć', 'd', 'dž', 'đ', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'lj', 'm', 'n', 'nj', 'o', 'p', 'r', 's', 'š', 't', 'u', 'v', 'z', 'ž']

def scrape_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        word_table = soup.find('table', class_='table word-table')
        entries = []
        if word_table:
            for row in word_table.find_all('tr'):
                word_tag = row.find('span', class_='word')
                definition_tag = row.find('td')
                if word_tag and definition_tag:
                    word = word_tag.get_text(strip=True)
                    definition = definition_tag.get_text(separator=" ").strip()
                    if word and definition and f"{word}: {definition}" not in entries:
                        entries.append(f"<p>{word}</p>")
        return "\n".join(entries)
    return ""

all_text = ""

for letter in alphabet:
    page = 1
    url = ""
    print(f"Found letter: {letter}...")
    all_text += f"<hr><h3>Letter {letter}</h3>"
    while True:
        url = f"https://rjecnik.hr/?letter={letter}&page={page}"
        print(f"Scraping page {page}...")
        page_text = scrape_page(url)
        if not page_text.strip():
            break
        all_text += page_text
        page = page + 1
    print(f"\n")

html_content = f"""
<html>
<head>
    <meta charset="UTF-8">
    <title>Scraped Text</title>
</head>
<body>
    {all_text}
</body>
</html>
"""

try:
    pdfkit.from_string(html_content, 'scraped_text.pdf', options={ 'encoding': 'UTF-8' })
    print("PDF saved successfully!")
except Exception as e:
    print(f"Error saving PDF: {e}")

print("Scraping complete!")
