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
    
    command = card.params[0]
    quantity = int(card.params[1].strip().split(" ")[1])
    
    whi = 0 #the location of the the current card in the list
    for x in range(len(list_items)):
        if card.c_id == list_items[x]["id"]:
            whi = x
            break

    if quantity == 0:
        card.destory()
        return

    c_start = whi - (quantity)
    c_end = whi
    cards_ir = list_items[c_start:c_end]

    if command == "delete":
        delete(cards_ir)
    if command == "label":
        label(cards_ir, card)
    #if command == "due":
    #    due(cards_ir, card)
    #if command == "me":
    #    me(cards_ir)

    card.destory()

def label(cards, card):
    all_labels = requests.get(
        f"https://api.trello.com/1/boards/{card.b_id}?actions=none&boardStars=none&cards=none&card_pluginData=false&checklists=none&customFields=false&fields=name%2Cdesc%2CdescData%2Cclosed%2CidOrganization%2Cpinned%2Curl%2CshortUrl%2Cprefs%2ClabelNames&labels=all&lists=none&members=none&memberships=none&membersInvited=none&membersInvited_fields=none&pluginData=false&organization=false&organization_pluginData=false&myPrefs=false&tags=false",
        params = {
            "key": os.getenv("API_KEY"),
            "token": os.getenv("API_TOKEN")
        }
    ).json()["labels"]
    labels = []
    q_label = card.params[2].strip()
    for label in all_labels:
        if label["name"].lower().startswith(q_label.lower()):
            labels.append(label)
    
    if len(labels) == 0:
        return

    for item in cards:
        c_id = item["id"]
        v = requests.get(
            f"https://api.trello.com/1/cards/{c_id}",
            params = {
                "fields": "idLabels",
                "key": os.getenv("API_KEY"),
                "token": os.getenv("API_TOKEN")                
            }
        )
        cur_labels = ','.join(v.json()["idLabels"])
        print(cur_labels)
        s = requests.put(
            f"https://api.trello.com/1/cards/{c_id}",
            params = {
                "idLabels": labels[0]["id"],
                "key": os.getenv("API_KEY"),
                "token": os.getenv("API_TOKEN")
            }
        )
    

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