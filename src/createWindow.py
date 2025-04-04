import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import Label

import launchGame

CARD_BACKGROUND = "Black"
CARD_BORDER = "#ff5404"
TEXT_COLOR = "white"
APP_BACKGROUND = "gray"

def createWindow(logins, player_data, config):
    root = tk.Tk()
    root.title("OW-Alt-Manager")
    root.configure(bg=APP_BACKGROUND)


    # Start in maximized mode
    root.state('zoomed')
    
    if(len(logins) <= 6):

        image_path = "images/assets/OWAltLogo.png"  
        img = Image.open(image_path)
        img = img.resize((700  ,440))  
        logo = ImageTk.PhotoImage(img)

        logo_label = tk.Label(root, image=logo, bg=APP_BACKGROUND)
        logo_label.image = logo  
        logo_label.pack(pady=(20, 10)) 

    # Create a frame to center the player cards
    container = tk.Frame(root, bg=APP_BACKGROUND)
    container.pack(expand=True)  # Expands to center in the window

    # Get screen width and calculate how many cards fit per row
    screen_width = root.winfo_screenwidth()
    card_width = 290  # Card width + padding
    cards_per_row = max(1, screen_width // card_width)

    for i, (login, data) in enumerate(zip(logins, player_data)):
        createPlayerButton(container, login, data, i, cards_per_row, config)
        

    root.mainloop()

def createPlayerButton(parent, login, account, index, cards_per_row, config):

    player_card = tk.Frame(
        parent, 
        width=290, 
        height=500, 
        bg=CARD_BACKGROUND, 
        cursor="hand2",
        highlightbackground=CARD_BORDER, 
        highlightthickness=4  
    )
    
    player_card.pack_propagate(False)
    


    row = index // cards_per_row
    col = index % cards_per_row

    # Create an empty column on the left to center the grid
    parent.grid_columnconfigure(tuple(range(cards_per_row)), weight=1)

    player_card.grid(row=row, column=col, padx=10, pady=10, sticky="n")

    bindClickEvent(player_card, login, config)
    

    ##################### Player Avatar #######################
    if(account == None):
        player_avatar_image = ImageTk.PhotoImage(Image.open("images/assets/DefualtAvatar.png")   .resize((100, 100)))
    else:
        player_avatar_image = fetch_image(account['avatar'], 100)
    
    player_avatar_label = Label(player_card, image=player_avatar_image, bg=CARD_BACKGROUND)
    player_avatar_label.pack(pady=20)
    player_avatar_label.image = player_avatar_image
    bindClickEvent(player_avatar_label, login, config)

    ##################### Username #######################
    player_username = Label(player_card, text=login['username'].split("-")[0], font=("Arial", 16, "bold"), fg=TEXT_COLOR, bg=player_card.cget("bg"))
    player_username.pack(pady=10)
    bindClickEvent(player_username, login, config)
    
    ####################### Role Icons ##########################
    tank_icon =    ImageTk.PhotoImage(Image.open("images/assets/Tank.png")   .resize((50, 50)))
    damage_icon =  ImageTk.PhotoImage(Image.open("images/assets/Damage.png") .resize((50, 50)))
    support_icon = ImageTk.PhotoImage(Image.open("images/assets/Support.png").resize((50, 50)))

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
    
    bindClickEvent(tank_icon_label, login, config)
    bindClickEvent(damage_icon_label, login, config)
    bindClickEvent(support_icon_label, login, config)
    
    bindClickEvent(icons, login, config)


    ####################### Rank Images ############################
    unranked_image = ImageTk.PhotoImage(Image.open("images/assets/unranked.png").resize((50, 50)))
    if(account == None or account['competitive'] == None):
        tank_rank_image     = unranked_image
        damage_rank_image   = unranked_image
        support_rank_image  = unranked_image
        
    else:
        comp_ranks = account['competitive']['pc']

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
    
    bindClickEvent(tank_rank_label, login, config)
    bindClickEvent(damage_rank_label, login, config)
    bindClickEvent(support_rank_label, login, config)
    
    bindClickEvent(ranks, login, config)
    
    ###################### Rank Tier ########################
    
    if(account == None or account['competitive'] == None):
        return 
    tank_tier     = comp_ranks['tank']['tier']    if comp_ranks['tank']    else ""
    damage_tier   = comp_ranks['damage']['tier']  if comp_ranks['damage']  else ""
    support_tier  = comp_ranks["support"]['tier'] if comp_ranks['support'] else ""    

    tiers = tk.Frame(player_card, bg=CARD_BACKGROUND)
    tiers.pack(pady=10)
    
    tank_tier_label = Label(tiers, text=tank_tier, font=("Arial", 16, "bold"), bg=CARD_BACKGROUND, fg=TEXT_COLOR)
    tank_tier_label.pack(side="left", padx=30)
    
    damage_tier_label = Label(tiers, text=damage_tier, font=("Arial", 16, "bold"), bg=CARD_BACKGROUND, fg=TEXT_COLOR)
    damage_tier_label.pack(side="left", padx=30)

    support_tier_label = Label(tiers, text=support_tier, font=("Arial", 16, "bold"), bg=CARD_BACKGROUND, fg=TEXT_COLOR)
    support_tier_label.pack(side="left", padx=30)
    
    bindClickEvent(tank_tier_label, login, config)
    bindClickEvent(damage_tier_label, login, config)
    bindClickEvent(support_tier_label, login, config)
    
    bindClickEvent(tiers, login, config)
    
#bind an object to the click event
def bindClickEvent(widget, login, config):
    """Bind the click event to a widget and change cursor."""
    widget.bind("<Button-1>", lambda event: launchGame.launchGame(login, config))
    
#fetch an image from a given url and resize it
def fetch_image(url, size):
    response = requests.get(url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    image = image.resize((size,size))  # Resize the small images if needed
    return ImageTk.PhotoImage(image)