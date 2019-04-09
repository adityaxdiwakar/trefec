import requests
import os

def handler(card):
    list_items = requests.get(
        f"https://api.trello.com/1/lists/{card.l_id}/cards",
        params = {
            "key": os.getenv("API_KEY"),
            "token": os.getenv("API_TOKEN")
        }
    ).json()
    
    direction = card.params[0]
    quantity = int(card.params[1].strip().split(" ")[1])
    
    whi = 0 #the location of the the current card in the list
    for x in range(len(list_items)):
        if card.c_id == list_items[x]["id"]:
            whi = x
            break

    if quantity == 0:
        return "", 204

    c_start = whi - (quantity)
    c_end = whi
    print(c_start, c_end)
    cards_ir = list_items[c_start:c_end]
    delete(cards_ir)

def delete(cards):
    for card in cards:
        c_id = card["id"]
        s = requests.delete(
            f"https://api.trello.com/1/cards/{c_id}",
            params = {
                "key": os.getenv("API_KEY"),
                "token": os.getenv("API_TOKEN")
            }
        )
        print(s.text)