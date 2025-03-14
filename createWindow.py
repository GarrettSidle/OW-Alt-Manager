import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import Label

import launchGame

CARD_BACKGROUND = "black"
TEXT_COLOR = "white"
APP_BACKGROUND = "gray"

def createWindow(logins, login_data):
    root = tk.Tk()
    root.title("Basic Tkinter Window")
    root.configure(bg=APP_BACKGROUND)

    # Start in maximized mode
    root.state('zoomed')
    
    user_warning = Label(root, text="Make sure battlenet application opens onto your main moniter,\n and battlenet is closed when clicking an account", font=("Arial", 35))
    user_warning.pack(pady=10)

    # Create a frame to center the player cards
    container = tk.Frame(root, bg=APP_BACKGROUND)
    container.pack(expand=True)  # Expands to center in the window

    # Get screen width and calculate how many cards fit per row
    screen_width = root.winfo_screenwidth()
    card_width = 320  # Card width + padding
    cards_per_row = max(1, screen_width // card_width)

    for i, (login, data) in enumerate(zip(logins, login_data)):
        createPlayerButton(container, login, data, i, cards_per_row, True)
        

    root.mainloop()

def createPlayerButton(parent, login, account, index, cards_per_row, allowLogin):
    if account is None:
        return

    player_card = tk.Frame(parent, width=300, height=500, bg=CARD_BACKGROUND, cursor="hand2" if allowLogin else "hand1")
    player_card.pack_propagate(False)

    row = index // cards_per_row
    col = index % cards_per_row

    # Create an empty column on the left to center the grid
    parent.grid_columnconfigure(tuple(range(cards_per_row)), weight=1)

    player_card.grid(row=row, column=col, padx=10, pady=10, sticky="n")

    bindClickEvent(allowLogin, player_card, login)

    ##################### Player Avatar #######################
    player_avatar_image = fetch_image(account['avatar'], 100)  
    player_avatar_label = Label(player_card, image=player_avatar_image, bg=CARD_BACKGROUND)
    player_avatar_label.pack(pady=20)
    player_avatar_label.image = player_avatar_image
    bindClickEvent(allowLogin, player_avatar_label, login)

    ##################### Username #######################
    player_username = Label(player_card, text=account['username'], font=("Arial", 16), bg=CARD_BACKGROUND, fg=TEXT_COLOR)
    player_username.pack(pady=10)
    bindClickEvent(allowLogin, player_username, login)
    
    ####################### Role Icons ##########################
    tank_icon =    ImageTk.PhotoImage(Image.open("images/Tank.png")   .resize((50, 50)))
    damage_icon =  ImageTk.PhotoImage(Image.open("images/Damage.png") .resize((50, 50)))
    support_icon = ImageTk.PhotoImage(Image.open("images/Support.png").resize((50, 50)))

    icons = tk.Frame(player_card, bg=CARD_BACKGROUND)
    icons.pack(pady=10)

    tank_icon_label = Label(icons, image=tank_icon, bg=CARD_BACKGROUND)
    tank_icon_label.pack(side="left", padx=10)
    tank_icon_label.image = tank_icon

    damage_icon_label = Label(icons, image=damage_icon, bg=CARD_BACKGROUND)
    damage_icon_label.pack(side="left", padx=10)
    damage_icon_label.image = damage_icon
    
    support_icon_label = Label(icons, image=support_icon, bg=CARD_BACKGROUND)
    support_icon_label.pack(side="left", padx=10)
    support_icon_label.image = support_icon
    
    bindClickEvent(allowLogin, tank_icon_label, login)
    bindClickEvent(allowLogin, damage_icon_label, login)
    bindClickEvent(allowLogin, support_icon_label, login)
    
    bindClickEvent(allowLogin, icons, login)


    ####################### Rank Images ############################
    comp_ranks = account['competitive']['pc']
    unranked_image = ImageTk.PhotoImage(Image.open("images/unranked.png").resize((50, 50)))

    tank_rank_image     = fetch_image(comp_ranks['tank']['rank_icon'], 50)    if comp_ranks['tank']    else unranked_image
    damage_rank_image   = fetch_image(comp_ranks['damage']['rank_icon'], 50)  if comp_ranks['damage']  else unranked_image
    support_rank_image  = fetch_image(comp_ranks["support"]['rank_icon'], 50) if comp_ranks['support'] else unranked_image

    ranks = tk.Frame(player_card, bg=CARD_BACKGROUND)
    ranks.pack(pady=10)
    
    tank_rank_label = Label(ranks, image=tank_rank_image, bg=CARD_BACKGROUND)
    tank_rank_label.pack(side="left", padx=10)
    tank_rank_label.image = tank_rank_image

    damage_rank_label = Label(ranks, image=damage_rank_image, bg=CARD_BACKGROUND)
    damage_rank_label.pack(side="left", padx=10)
    damage_rank_label.image = damage_rank_image
    
    support_rank_label = Label(ranks, image=support_rank_image, bg=CARD_BACKGROUND)
    support_rank_label.pack(side="left", padx=10)
    support_rank_label.image = support_rank_image
    
    bindClickEvent(allowLogin, tank_rank_label, login)
    bindClickEvent(allowLogin, damage_rank_label, login)
    bindClickEvent(allowLogin, support_rank_label, login)
    
    bindClickEvent(allowLogin, ranks, login)
    
    ###################### Rank Tier ########################
    tank_tier     = comp_ranks['tank']['tier']    if comp_ranks['tank']    else ""
    damage_tier   = comp_ranks['damage']['tier']  if comp_ranks['damage']  else ""
    support_tier  = comp_ranks["support"]['tier'] if comp_ranks['support'] else ""    

    tiers = tk.Frame(player_card, bg=CARD_BACKGROUND)
    tiers.pack(pady=10)
    
    tank_tier_label = Label(tiers, text=tank_tier, font=("Arial", 16), bg=CARD_BACKGROUND, fg=TEXT_COLOR)
    tank_tier_label.pack(side="left", padx=30)
    
    damage_tier_label = Label(tiers, text=damage_tier, font=("Arial", 16), bg=CARD_BACKGROUND, fg=TEXT_COLOR)
    damage_tier_label.pack(side="left", padx=30)

    support_tier_label = Label(tiers, text=support_tier, font=("Arial", 16), bg=CARD_BACKGROUND, fg=TEXT_COLOR)
    support_tier_label.pack(side="left", padx=30)
    
    bindClickEvent(allowLogin, tank_tier_label, login)
    bindClickEvent(allowLogin, damage_tier_label, login)
    bindClickEvent(allowLogin, support_tier_label, login)
    
    bindClickEvent(allowLogin, tiers, login)
    
#bind an object to the click event
def bindClickEvent(allowLogin, widget, login):
    if(not allowLogin):
        return 
    """Bind the click event to a widget and change cursor."""
    widget.bind("<Button-1>", lambda event: launchGame.launchGame(login))
    
#fetch an image from a given url and resize it
def fetch_image(url, size):
    response = requests.get(url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    image = image.resize((size,size))  # Resize the small images if needed
    return ImageTk.PhotoImage(image)