import json
import os

VAULT_FILE = "vault.json"


def load_vault():
    if not os.path.exists(VAULT_FILE):
        return {}

    with open(VAULT_FILE, "r") as file:
        return json.load(file)


def save_vault(data):
    with open(VAULT_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_entry(site, username, encrypted_password):
    data = load_vault()

    data[site] = {
        "username": username,
        "password": encrypted_password
    }

    save_vault(data)


def get_entry(site):
    data = load_vault()
    return data.get(site)


def delete_entry(site):
    data = load_vault()

    if site in data:
        del data[site]
        save_vault(data)