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
    
    if not quantity:
        return card.destory()

    whi = list_items.index(
        [x for x in list_items if x["id"] == card.c_id][0]
    )

    quantity = min(quantity, len(list_items) - 1)
    cards_ir = list_items[whi-quantity:whi]

    if command == "delete":
        delete(cards_ir)
    if command == "label":
        label(cards_ir, card)
    if command == "me":
        me(cards_ir, card.c_author["id"])

    card.destory()

def label(cards, card):
    fields = ["name", "desc", "descData", "closed", "idOrganization",
              "pinned", "url", "shortUrl", "prefs", "labelNames"]
    all_labels = requests.get(
        f"https://api.trello.com/1/boards/{card.b_id}",
        params = {
            "key": os.getenv("API_KEY"),
            "token": os.getenv("API_TOKEN"),
            "actions": "none",
            "boardStars": "none",
            "cards": "none",
            "card_pluginData": "false",
            "checklists": "none",
            "customFields": "false",
            "fields": "%2C".join(fields),
            "tags": "false",
            "labels": "all",
            "lists": "none",
            "members": "none",
            "memberships": "none",
            "membersInvisted": "none",
            "membersInvited_fields": "none",
            "pluginData": "false",
            "organization": "false",
            "organizaton_pluginData": "false",
            "myPrefs": "false"
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
