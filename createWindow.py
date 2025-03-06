import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import Label

import launchGame

def createWindow(logins, account_data):
    root = tk.Tk()
    root.title("Basic Tkinter Window")
    root.configure(bg="gray")

    # Start in maximized mode
    root.state('zoomed')

    # Create a frame to center the player cards
    container = tk.Frame(root, bg="gray")
    container.pack(expand=True)  # Expands to center in the window

    # Get screen width and calculate how many cards fit per row
    screen_width = root.winfo_screenwidth()
    card_width = 320  # Card width + padding
    cards_per_row = max(1, screen_width // card_width)

    for i, (login, account) in enumerate(zip(logins, account_data)):
        createPlayerButton(container, login, account, i, cards_per_row)

    root.mainloop()

def createPlayerButton(parent, login, account, index, cards_per_row):
    if account is None:
        return

    player_card = tk.Frame(parent, width=300, height=500, bg="Black", cursor="hand2")
    player_card.pack_propagate(False)

    row = index // cards_per_row
    col = index % cards_per_row

    # Create an empty column on the left to center the grid
    parent.grid_columnconfigure(tuple(range(cards_per_row)), weight=1)

    player_card.grid(row=row, column=col, padx=10, pady=10, sticky="n")

    bindClickEvent(player_card, login)

    ##################### Player Avatar #######################
    player_avatar_image = fetch_image(account['avatar'], 100)  
    player_avatar_label = Label(player_card, image=player_avatar_image, bg="Black")
    player_avatar_label.pack(pady=20)
    player_avatar_label.image = player_avatar_image
    bindClickEvent(player_avatar_label, login)

    ##################### Username #######################
    player_username = Label(player_card, text=account['username'], font=("Arial", 16), bg="Black", fg="white")
    player_username.pack(pady=10)
    bindClickEvent(player_username, login)
    
    ####################### Role Icons ##########################
    tank_icon =    ImageTk.PhotoImage(Image.open("images/Tank.png")   .resize((50, 50)))
    damage_icon =  ImageTk.PhotoImage(Image.open("images/Damage.png") .resize((50, 50)))
    support_icon = ImageTk.PhotoImage(Image.open("images/Support.png").resize((50, 50)))

    icons = tk.Frame(player_card, bg="Black")
    icons.pack(pady=10)

    # Place the small images side by side
    tank_icon_label = Label(icons, image=tank_icon, bg="Black")
    tank_icon_label.pack(side="left", padx=10)
    tank_icon_label.image = tank_icon

    damage_icon_label = Label(icons, image=damage_icon, bg="Black")
    damage_icon_label.pack(side="left", padx=10)
    damage_icon_label.image = damage_icon
    
    support_icon_label = Label(icons, image=support_icon, bg="Black")
    support_icon_label.pack(side="left", padx=10)
    support_icon_label.image = support_icon
    
    bindClickEvent(tank_icon_label, login)
    bindClickEvent(damage_icon_label, login)
    bindClickEvent(support_icon_label, login)
    
    bindClickEvent(icons, login)


    ####################### Rank Images ############################
    comp_ranks = account['competitive']['pc']
    unranked_image = ImageTk.PhotoImage(Image.open("images/unranked.png").resize((50, 50)))

    tank_rank_image     = fetch_image(comp_ranks['tank']['rank_icon'], 50)    if comp_ranks['tank']    else unranked_image
    damage_rank_image   = fetch_image(comp_ranks['damage']['rank_icon'], 50)  if comp_ranks['damage']  else unranked_image
    support_rank_image  = fetch_image(comp_ranks["support"]['rank_icon'], 50) if comp_ranks['support'] else unranked_image

    ranks = tk.Frame(player_card, bg="Black")
    ranks.pack(pady=10)
    
    # Place the small images side by side
    tank_rank_label = Label(ranks, image=tank_rank_image, bg="Black")
    tank_rank_label.pack(side="left", padx=10)
    tank_rank_label.image = tank_rank_image

    damage_rank_label = Label(ranks, image=damage_rank_image, bg="Black")
    damage_rank_label.pack(side="left", padx=10)
    damage_rank_label.image = damage_rank_image
    
    support_rank_label = Label(ranks, image=support_rank_image, bg="Black")
    support_rank_label.pack(side="left", padx=10)
    support_rank_label.image = support_rank_image
    
    bindClickEvent(tank_rank_label, login)
    bindClickEvent(damage_rank_label, login)
    bindClickEvent(support_rank_label, login)
    
    bindClickEvent(ranks, login)
    
    ###################### Rank Tier ########################
    tank_tier     = comp_ranks['tank']['tier']    if comp_ranks['tank']    else ""
    damage_tier   = comp_ranks['damage']['tier']  if comp_ranks['damage']  else ""
    support_tier  = comp_ranks["support"]['tier'] if comp_ranks['support'] else ""    

    tiers = tk.Frame(player_card, bg="Black")
    tiers.pack(pady=10)
    
    tank_tier_label = Label(tiers, text=tank_tier, font=("Arial", 16), bg="Black", fg="white")
    tank_tier_label.pack(side="left", padx=30)
    
    damage_tier_label = Label(tiers, text=damage_tier, font=("Arial", 16), bg="Black", fg="white")
    damage_tier_label.pack(side="left", padx=30)

    support_tier_label = Label(tiers, text=support_tier, font=("Arial", 16), bg="Black", fg="white")
    support_tier_label.pack(side="left", padx=30)
    
    bindClickEvent(tank_tier_label, login)
    bindClickEvent(damage_tier_label, login)
    bindClickEvent(support_tier_label, login)
    
    bindClickEvent(tiers, login)
    
def bindClickEvent(widget, login):
    """Bind the click event to a widget and change cursor."""
    widget.bind("<Button-1>", lambda event: launchGame.launchGame(login))
    

def fetch_image(url, size):
    response = requests.get(url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    image = image.resize((size,size))  # Resize the small images if needed
    return ImageTk.PhotoImage(image)