DATA_FILE = "data/passwords.txt"

def save_credentials(website, username, password):
    """
    Appends credentials to a local text file.
    """

    with open(DATA_FILE, "a") as file:
        file.write(f"{website} | {username} | {password}\n")
