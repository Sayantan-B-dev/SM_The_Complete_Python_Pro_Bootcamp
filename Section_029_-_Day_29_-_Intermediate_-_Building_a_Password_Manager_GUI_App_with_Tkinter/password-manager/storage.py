import json

DATA_FILE = "data/passwords.json"

def save_credentials(website, username, password):
    new_data = {
        website: {
            "username": username,
            "password": password
        }
    }

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        # File does not exist
        data = {}

    except json.JSONDecodeError:
        # File exists but is empty or corrupted
        data = {}

    data.update(new_data)

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def find_password(website):
    """
    Finds password for the given website.
    Returns password if found, None otherwise.
    """
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            if website in data:
                email = data[website]["username"]
                password = data[website]["password"]
                return email, password
            else:
                return None, None
    except FileNotFoundError:
        return None, None
    except json.JSONDecodeError:
        return None, None
