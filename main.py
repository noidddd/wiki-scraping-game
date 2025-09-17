from bs4 import BeautifulSoup
import requests
from urllib.parse import quote, unquote

# Target URL
article = 'Stardew Valley'
base_url = 'https://en.wikipedia.org/wiki/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  #"AppleWebKit/537.36 (KHTML, like Gecko) "
                  #"Chrome/120.0.0.0 Safari/537.36"
}

def parse_links(url, headers, target):

    # HTTP GET request
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.find("div", {"id": "mw-content-text"})
    if not content:
        return False

    for anchor in content.find_all("a"):
        link = anchor.get("href", "/")

        # only other wiki links
        if link.startswith('/wiki/') and not link.startswith('/wiki/Special:'):

            clean_link = unquote(link.replace("_", " "))
            
            if clean_link.lower() == f'/wiki/{target.lower()}':
                return True
    
    return False

def run_game(start_article):

    score = 0
    current_article = start_article

    print(f"\n--- The Wikipedia Game ---\n")
    print(f"Starting article: {current_article}")

    while True:

        guess = input("Enter your guess: ").strip()
        url = base_url + quote(current_article.replace(" ", "_"))

        if parse_links(url, headers, guess):

            score += 1
            print(f"✅ Correct! Score: {score}\n")

            # next article
            current_article = guess
            print(f"Current article: {current_article}")

        else:

            print(f"❌ Game over. Final Score: {score}")
            break


run_game(article)

