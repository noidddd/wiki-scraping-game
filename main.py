from bs4 import BeautifulSoup
import requests
from urllib.parse import quote, unquote
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from io import BytesIO

base_url = 'https://en.wikipedia.org/wiki/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
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

def get_article_img(article):

    url = base_url + quote(article.replace(" ", "_"))
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    infobox = soup.find("table", {"class": "infobox"})
    img_tag = infobox.find("img") if infobox else None

    if img_tag and img_tag.get("src"):

        img_url = "https:" + img_tag["src"]

    else:
        # placeholder img if doesn't exist
        img_url = "https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png"

    img_data = requests.get(img_url, headers=headers).content
    img = Image.open(BytesIO(img_data))
    img = img.resize((300, 400), Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def update_article(article):

    global current_article

    score_label.config(text=f"Score: {score}")
    current_article = article

    # Update UI
    title_label.config(text=current_article)
    img = get_article_img(current_article)
    img_label.config(image=img)
    img_label.image = img

def submit_guess():

    global current_article, score

    guess = guess_entry.get().strip()
    guess_entry.delete(0, tk.END)

    url = base_url + quote(current_article.replace(" ", "_"))

    if parse_links(url, headers, guess):
        score += 1
        update_article(guess)

    else:
        messagebox.showerror("Game Over", f"❌ Game over! Final Score: {score}")
        root.destroy()

def start_game():

    global current_article, score

    start_article = start_entry.get().strip()
    if not start_article:
        messagebox.showwarning("Invalid Input", "Please choose an existing article.")
        return

    score = 0
    update_article(start_article)

    # Hide start screen and show game screen
    start_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)

# --- TKinter GUI ---

root = tk.Tk()
root.title("The Wikipedia Game")
root.geometry('600x625')

# Start screen
start_frame = tk.Frame(root)
start_frame.pack(fill="both", expand=True)

welcome_label = tk.Label(start_frame, text="Choose an article to start with:", font=("Arial", 18, "bold"))
welcome_label.pack(pady=20)

start_entry = tk.Entry(start_frame, font=("Arial", 14))
start_entry.pack(pady=10)

start_button = tk.Button(start_frame, text="Start Game", font=("Arial", 14), command=start_game)
start_button.pack(pady=10)

# Game screen
game_frame = tk.Frame(root)

score = 0
score_label = tk.Label(game_frame, text=f"Score: {score}", font=("Arial", 14), anchor="e")
score_label.pack(side="top", anchor="ne", padx=10, pady=5)

title_label = tk.Label(game_frame, text="", font=("Arial", 18, "bold"))
title_label.pack()

img_label = tk.Label(game_frame)
img_label.pack(padx=50, pady=10)

guess_entry = tk.Entry(game_frame, font=("Arial", 14), justify="center")
guess_entry.pack(pady=10)

submit_btn = tk.Button(game_frame, text="Submit Guess", font=("Arial", 14), command=submit_guess)
submit_btn.pack(pady=5)


root.mainloop()
