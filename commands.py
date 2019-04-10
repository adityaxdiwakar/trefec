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

    if quantity > len(list_items):
        quantity = len(list_items) - 1

    c_start = whi - (quantity)
    c_end = whi
    print(c_start, c_end)
    cards_ir = list_items[c_start:c_end]

    if command == "delete":
        delete(cards_ir)
    if command == "label":
        label(cards_ir, card)
    #if command == "due":
    #    due(cards_ir, card)
    if command == "me":
        me(cards_ir, card.c_author["id"])

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
        arr_labels = v.json()["idLabels"]
        arr_labels.append(labels[0]["id"])
        n_labels = ','.join(arr_labels)
        s = requests.put(
            f"https://api.trello.com/1/cards/{c_id}",
            params = {
                "idLabels": n_labels,
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


def me(cards, me):
    for card in cards:
        c_id = card["id"]
        v = requests.get(
            f"https://api.trello.com/1/cards/{c_id}",
            params = {
                "fields": "idMembers",
                "key": os.getenv("API_KEY"),
                "token": os.getenv("API_TOKEN")                
            }
        )
        members = v.json()["idMembers"]
        members.append(me)
        n_members = ','.join(members)
        s = requests.put(
            f"https://api.trello.com/1/cards/{c_id}",
            params = {
                "idMembers": n_members,
                "key": os.getenv("API_KEY"),
                "token": os.getenv("API_TOKEN")
            }
        )
